using System.Text.Json.Serialization;

namespace PhonemeReplacement.Models
{
    /// <summary>
    /// Represents a phoneme with its properties and possible replacements
    /// </summary>
    public class Phoneme
    {
        [JsonPropertyName("symbol")]
        public string Symbol { get; set; } = string.Empty;

        [JsonPropertyName("description")]
        public string Description { get; set; } = string.Empty;

        [JsonPropertyName("examples")]
        public List<string> Examples { get; set; } = new List<string>();

        [JsonPropertyName("replacements")]
        public List<string> Replacements { get; set; } = new List<string>();
    }

    /// <summary>
    /// Container for phoneme data loaded from JSON
    /// </summary>
    public class PhonemeData
    {
        [JsonPropertyName("phonemes")]
        public List<Phoneme> Phonemes { get; set; } = new List<Phoneme>();
    }
}
