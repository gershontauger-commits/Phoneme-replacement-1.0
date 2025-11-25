# Phoneme Replacement 1.0

A solution designed to help aphasia patients with speech therapy through phoneme replacement analysis.

## Project Overview

This application helps speech therapists and aphasia patients by:
- Displaying common phonemes and their characteristics
- Showing possible phoneme substitutions that patients might make
- Demonstrating common phonological processes in speech therapy

## Prerequisites

To recreate and run this project, you need:

1. **Visual Studio 2022** (or later) with the following workloads:
   - .NET desktop development
   - Or any .NET 8.0+ compatible IDE (Visual Studio Code, Rider, etc.)

2. **.NET 8.0 SDK** (or later)
   - Download from: https://dotnet.microsoft.com/download

## How to Recreate the Project

### Option 1: Open in Visual Studio

1. Clone this repository:
   ```bash
   git clone https://github.com/gershontauger-commits/Phoneme-replacement-1.0.git
   ```

2. Open the solution file in Visual Studio:
   - Double-click `PhonemeReplacement.sln` in the repository root
   - Or use File → Open → Project/Solution in Visual Studio

3. Build the solution:
   - Press `Ctrl+Shift+B` or use Build → Build Solution

4. Run the application:
   - Press `F5` to run with debugging
   - Or press `Ctrl+F5` to run without debugging

### Option 2: Using Command Line

1. Clone the repository:
   ```bash
   git clone https://github.com/gershontauger-commits/Phoneme-replacement-1.0.git
   cd Phoneme-replacement-1.0
   ```

2. Restore dependencies:
   ```bash
   dotnet restore
   ```

3. Build the solution:
   ```bash
   dotnet build PhonemeReplacement.sln
   ```

4. Run the application:
   ```bash
   dotnet run --project src/PhonemeReplacement/PhonemeReplacement.csproj
   ```

### Option 3: Using Visual Studio Code

1. Clone the repository and open in VS Code
2. Install the C# extension
3. Open the terminal and run:
   ```bash
   dotnet restore
   dotnet build
   dotnet run --project src/PhonemeReplacement/PhonemeReplacement.csproj
   ```

## Project Structure

```
Phoneme-replacement-1.0/
├── PhonemeReplacement.sln          # Visual Studio Solution file
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
└── src/
    └── PhonemeReplacement/
        ├── PhonemeReplacement.csproj   # Project file
        ├── Program.cs                  # Main entry point
        ├── Data/
        │   ├── phonemes.json           # Phoneme definitions
        │   └── replacement_rules.json  # Replacement rules
        ├── Models/
        │   ├── Phoneme.cs              # Phoneme data model
        │   └── ReplacementRule.cs      # Rule data model
        └── Services/
            └── PhonemeService.cs       # Core phoneme logic
```

## Data Files

### phonemes.json
Contains definitions of phonemes including:
- Symbol (IPA representation)
- Description
- Example words
- Possible replacement sounds

### replacement_rules.json
Contains common phonological processes:
- **Voicing Substitution**: voiced → voiceless (b→p, d→t, g→k)
- **Fronting Substitution**: back → front sounds (k→t, g→d)
- **Gliding Substitution**: liquids → glides (l→w, r→w)
- **Stopping Substitution**: fricatives → stops (f→p, s→t)
- **Final Consonant Deletion**: removing word-final consonants

## Usage

When you run the application:

1. It displays all available phonemes with their descriptions
2. You can enter words to see possible phoneme replacements
3. Type 'exit' to quit the application

## Example Output

```
Enter a word to see possible phoneme replacements (or 'exit' to quit):

> ball
Possible replacements for 'ball':
  - Voicing: pall
  - Gliding: baww
  - Final deletion: bal
```

## Extending the Project

### Adding New Phonemes
Edit `src/PhonemeReplacement/Data/phonemes.json` to add new phoneme entries.

### Adding New Rules
Edit `src/PhonemeReplacement/Data/replacement_rules.json` to add new replacement rules.

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## License

This project is designed for educational and therapeutic purposes.

## Support

For questions or support, please open an issue in the GitHub repository.
