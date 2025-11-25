using System;
using System.IO;
using System.Text.Json;
using PhonemeReplacement.Models;
using PhonemeReplacement.Services;

namespace PhonemeReplacement
{
    /// <summary>
    /// Phoneme Replacement Application
    /// A solution designed to help aphasia patients with speech therapy
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("===========================================");
            Console.WriteLine("  Phoneme Replacement - Aphasia Therapy");
            Console.WriteLine("===========================================");
            Console.WriteLine();

            try
            {
                // Load phoneme data
                var dataPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data");
                var phonemeService = new PhonemeService(dataPath);
                
                Console.WriteLine("Loaded phoneme data successfully!");
                Console.WriteLine();
                
                // Display available phonemes
                phonemeService.DisplayPhonemes();
                
                // Interactive mode
                Console.WriteLine("\nEnter a word to see possible phoneme replacements (or 'exit' to quit):");
                
                while (true)
                {
                    Console.Write("\n> ");
                    var input = Console.ReadLine()?.Trim().ToLower();
                    
                    if (string.IsNullOrEmpty(input) || input == "exit")
                    {
                        break;
                    }
                    
                    var replacements = phonemeService.GetReplacements(input);
                    
                    Console.WriteLine($"Possible replacements for '{input}':");
                    foreach (var replacement in replacements)
                    {
                        Console.WriteLine($"  - {replacement}");
                    }
                }
                
                Console.WriteLine("\nThank you for using Phoneme Replacement!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine("Please ensure the Data folder is in the correct location.");
            }
        }
    }
}
