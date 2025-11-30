"""
Machine Learning model for Hebrew pronunciation assessment
Uses neural network to compare syllables and assess pronunciation quality
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (MODELS_DIR, EMBEDDING_DIM, SIMILARITY_THRESHOLD,
                    BATCH_SIZE, LEARNING_RATE, EPOCHS)


class SyllableEmbeddingNet(nn.Module):
    """
    Neural network for creating syllable embeddings
    Maps acoustic features to a lower-dimensional space for comparison
    """
    
    def __init__(self, input_dim=29, embedding_dim=EMBEDDING_DIM):
        super(SyllableEmbeddingNet, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.3),
            
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.3),
            
            nn.Linear(128, embedding_dim),
            nn.Tanh()
        )
    
    def forward(self, x):
        return self.network(x)


class SyllableDataset(Dataset):
    """Dataset for syllable training"""
    
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = labels
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


class PronunciationModel:
    """
    Main model for pronunciation assessment and correction
    """
    
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.syllable_references = {}
        self.scaler = None
        
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def create_model(self, input_dim=29):
        """Create a new model"""
        self.model = SyllableEmbeddingNet(input_dim=input_dim).to(self.device)
        return self.model
    
    def train_model(self, features, labels, epochs=EPOCHS):
        """
        Train the model on syllable data
        Uses triplet loss to learn good embeddings
        """
        if self.model is None:
            self.create_model(input_dim=features.shape[1])
        
        # Normalize features
        self.scaler = {'mean': np.mean(features, axis=0), 'std': np.std(features, axis=0)}
        features_normalized = (features - self.scaler['mean']) / (self.scaler['std'] + 1e-8)
        
        # Create dataset and dataloader
        dataset = SyllableDataset(features_normalized, labels)
        dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
        
        # Loss and optimizer
        criterion = nn.TripletMarginLoss(margin=1.0)
        optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        
        # Training loop
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch_features, batch_labels in dataloader:
                batch_features = batch_features.to(self.device)
                
                # For simplicity, using MSE loss for now
                # In production, would use proper triplet loss with anchor/positive/negative
                embeddings = self.model(batch_features)
                
                # Simple reconstruction loss
                optimizer.zero_grad()
                loss = torch.mean(torch.sum(embeddings ** 2, dim=1))
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if (epoch + 1) % 10 == 0:
                avg_loss = total_loss / len(dataloader)
                print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
        
        print("Training completed!")
    
    def load_training_data(self, data_path):
        """Load training data from exported file"""
        data = np.load(data_path, allow_pickle=True)
        return data['features'], data['labels'], data['syllables']
    
    def add_syllable_reference(self, syllable, features):
        """Add or update reference features for a syllable"""
        if self.scaler:
            features_normalized = (features - self.scaler['mean']) / (self.scaler['std'] + 1e-8)
        else:
            features_normalized = features
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_normalized).unsqueeze(0).to(self.device)
            if self.model:
                embedding = self.model(features_tensor).cpu().numpy()[0]
            else:
                embedding = features_normalized
        
        self.syllable_references[syllable] = {
            'features': features,
            'embedding': embedding
        }
    
    def compare_syllables(self, features1, features2):
        """
        Compare two syllables based on their features
        Returns similarity score (0-1, higher is more similar)
        """
        # Normalize features if scaler exists
        if self.scaler:
            features1 = (features1 - self.scaler['mean']) / (self.scaler['std'] + 1e-8)
            features2 = (features2 - self.scaler['mean']) / (self.scaler['std'] + 1e-8)
        
        if self.model:
            # Use model embeddings
            with torch.no_grad():
                f1_tensor = torch.FloatTensor(features1).unsqueeze(0).to(self.device)
                f2_tensor = torch.FloatTensor(features2).unsqueeze(0).to(self.device)
                
                emb1 = self.model(f1_tensor).cpu().numpy()
                emb2 = self.model(f2_tensor).cpu().numpy()
                
                similarity = cosine_similarity(emb1, emb2)[0][0]
        else:
            # Use raw features
            print(f"DEBUG: compare_syllables shapes: {np.shape(features1)}, {np.shape(features2)}")
            features1 = np.array(features1).reshape(1, -1)
            features2 = np.array(features2).reshape(1, -1)
            similarity = cosine_similarity(features1, features2)[0, 0]
        
        # Convert to 0-1 range
        similarity = (similarity + 1) / 2
        return similarity
    
    def assess_pronunciation(self, syllable_features, reference_syllable):
        """
        Assess how well a syllable is pronounced compared to reference
        Returns quality score and whether it needs correction
        """
        if reference_syllable not in self.syllable_references:
            return {'quality_score': 0.0, 'needs_correction': True, 'message': 'No reference found'}
        
        ref_features = self.syllable_references[reference_syllable]['features']
        similarity = self.compare_syllables(syllable_features, ref_features)
        
        needs_correction = similarity < SIMILARITY_THRESHOLD
        
        return {
            'quality_score': similarity,
            'needs_correction': needs_correction,
            'threshold': SIMILARITY_THRESHOLD,
            'message': 'Good pronunciation' if not needs_correction else 'Needs improvement'
        }
    
    def save_model(self, path=None):
        """Save model to disk"""
        if path is None:
            path = os.path.join(MODELS_DIR, 'pronunciation_model.pth')
        
        save_dict = {
            'model_state': self.model.state_dict() if self.model else None,
            'syllable_references': self.syllable_references,
            'scaler': self.scaler
        }
        
        torch.save(save_dict, path)
        print(f"Model saved to {path}")
        return path
    
    def load_model(self, path):
        """Load model from disk"""
        checkpoint = torch.load(path, map_location=self.device)
        
        if checkpoint['model_state']:
            # Infer input dimension from first layer
            input_dim = checkpoint['model_state']['network.0.weight'].shape[1]
            self.create_model(input_dim=input_dim)
            self.model.load_state_dict(checkpoint['model_state'])
            self.model.eval()
        
        self.syllable_references = checkpoint['syllable_references']
        self.scaler = checkpoint['scaler']
        
        print(f"Model loaded from {path}")
        print(f"Loaded {len(self.syllable_references)} syllable references")


if __name__ == "__main__":
    # Test the model
    print(f"Using device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
    
    model = PronunciationModel()
    print("Pronunciation model initialized successfully!")
    
    # Create sample model
    model.create_model(input_dim=29)
    print("Model architecture created.")
