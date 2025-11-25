using System.Text.Json.Serialization;

namespace PhonemeReplacement.Models
{
    /// <summary>
    /// Represents a phoneme replacement rule
    /// </summary>
    public class ReplacementRule
    {
        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;

        [JsonPropertyName("description")]
        public string Description { get; set; } = string.Empty;

        [JsonPropertyName("pattern")]
        public string? Pattern { get; set; }

        [JsonPropertyName("mapping")]
        public Dictionary<string, string>? Mapping { get; set; }

        [JsonPropertyName("examples")]
        public List<ReplacementExample>? Examples { get; set; }
    }

    /// <summary>
    /// Example of a replacement rule application
    /// </summary>
    public class ReplacementExample
    {
        [JsonPropertyName("input")]
        public string Input { get; set; } = string.Empty;

        [JsonPropertyName("output")]
        public string Output { get; set; } = string.Empty;
    }

    /// <summary>
    /// Container for replacement rules loaded from JSON
    /// </summary>
    public class ReplacementRulesData
    {
        [JsonPropertyName("replacementRules")]
        public List<ReplacementRule> ReplacementRules { get; set; } = new List<ReplacementRule>();
    }
}
