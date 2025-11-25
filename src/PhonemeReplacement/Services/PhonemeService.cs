using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using PhonemeReplacement.Models;

namespace PhonemeReplacement.Services
{
    /// <summary>
    /// Service for loading and processing phoneme data
    /// </summary>
    public class PhonemeService
    {
        private static readonly string Consonants = "bcdfghjklmnpqrstvwxz";
        
        private readonly PhonemeData _phonemeData;
        private readonly ReplacementRulesData _rulesData;
        private readonly Dictionary<string, ReplacementRule> _rulesByName;

        public PhonemeService(string dataPath)
        {
            // Load phonemes
            var phonemesFile = Path.Combine(dataPath, "phonemes.json");
            if (File.Exists(phonemesFile))
            {
                var phonemesJson = File.ReadAllText(phonemesFile);
                _phonemeData = JsonSerializer.Deserialize<PhonemeData>(phonemesJson) ?? new PhonemeData();
            }
            else
            {
                _phonemeData = new PhonemeData();
            }

            // Load replacement rules
            var rulesFile = Path.Combine(dataPath, "replacement_rules.json");
            if (File.Exists(rulesFile))
            {
                var rulesJson = File.ReadAllText(rulesFile);
                _rulesData = JsonSerializer.Deserialize<ReplacementRulesData>(rulesJson) ?? new ReplacementRulesData();
            }
            else
            {
                _rulesData = new ReplacementRulesData();
            }
            
            // Create dictionary lookup for rules by name
            _rulesByName = _rulesData.ReplacementRules.ToDictionary(r => r.Name, r => r);
        }

        /// <summary>
        /// Display all loaded phonemes
        /// </summary>
        public void DisplayPhonemes()
        {
            Console.WriteLine("Available Phonemes:");
            Console.WriteLine("-------------------");
            
            foreach (var phoneme in _phonemeData.Phonemes)
            {
                Console.WriteLine($"  [{phoneme.Symbol}] {phoneme.Description}");
                Console.WriteLine($"      Examples: {string.Join(", ", phoneme.Examples)}");
                if (phoneme.Replacements.Any())
                {
                    Console.WriteLine($"      Possible replacements: {string.Join(", ", phoneme.Replacements)}");
                }
            }
        }

        /// <summary>
        /// Get possible replacements for a word
        /// </summary>
        public List<string> GetReplacements(string word)
        {
            var replacements = new List<string>();
            
            if (string.IsNullOrEmpty(word))
            {
                return replacements;
            }

            // Apply voicing substitution
            if (_rulesByName.TryGetValue("VoicingSubstitution", out var voicingRule) && voicingRule.Mapping != null)
            {
                var voicingReplacement = ApplyMapping(word, voicingRule.Mapping);
                if (voicingReplacement != word)
                {
                    replacements.Add($"Voicing: {voicingReplacement}");
                }
            }

            // Apply fronting substitution
            if (_rulesByName.TryGetValue("FrontingSubstitution", out var frontingRule) && frontingRule.Mapping != null)
            {
                var frontingReplacement = ApplyMapping(word, frontingRule.Mapping);
                if (frontingReplacement != word)
                {
                    replacements.Add($"Fronting: {frontingReplacement}");
                }
            }

            // Apply gliding substitution
            if (_rulesByName.TryGetValue("GlidingSubstitution", out var glidingRule) && glidingRule.Mapping != null)
            {
                var glidingReplacement = ApplyMapping(word, glidingRule.Mapping);
                if (glidingReplacement != word)
                {
                    replacements.Add($"Gliding: {glidingReplacement}");
                }
            }

            // Apply stopping substitution
            if (_rulesByName.TryGetValue("StoppingSubstitution", out var stoppingRule) && stoppingRule.Mapping != null)
            {
                var stoppingReplacement = ApplyMapping(word, stoppingRule.Mapping);
                if (stoppingReplacement != word)
                {
                    replacements.Add($"Stopping: {stoppingReplacement}");
                }
            }

            // Final consonant deletion
            if (word.Length > 1 && Consonants.Contains(word[word.Length - 1]))
            {
                replacements.Add($"Final deletion: {word.Substring(0, word.Length - 1)}");
            }

            if (!replacements.Any())
            {
                replacements.Add("No common replacements found");
            }

            return replacements;
        }

        private string ApplyMapping(string word, Dictionary<string, string> mapping)
        {
            var result = word;
            foreach (var kvp in mapping)
            {
                result = result.Replace(kvp.Key, kvp.Value);
            }
            return result;
        }
    }
}
