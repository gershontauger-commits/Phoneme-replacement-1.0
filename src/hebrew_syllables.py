"""
Hebrew syllable database and utilities
Contains the 100 most common Hebrew syllables
"""

# Hebrew phoneme categories
HEBREW_CONSONANTS = [
    'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 
    'כ', 'ך', 'ל', 'מ', 'ם', 'נ', 'ן', 'ס', 'ע', 'פ',
    'ף', 'צ', 'ץ', 'ק', 'ר', 'ש', 'ת'
]

HEBREW_VOWELS = [
    'ַ',  # Patach
    'ָ',  # Kamatz
    'ֶ',  # Segol
    'ֵ',  # Tzere
    'ִ',  # Hiriq
    'ֹ',  # Holam
    'ֻ',  # Kubutz
    'ְ',  # Shva
]

# 100 Most common Hebrew syllables (approximate - can be refined with actual linguistic data)
COMMON_HEBREW_SYLLABLES = [
    # Simple CV (Consonant-Vowel) patterns
    'בְּ', 'לְ', 'שֶׁ', 'הַ', 'מֵ', 'כָּ', 'תִּ', 'וְ', 'יְ', 'נִ',
    'רַ', 'סֵ', 'עַ', 'פָּ', 'צְ', 'קֹ', 'דָ', 'גַ', 'זֶ', 'חֹ',
    
    # Common syllables from frequent words
    'לֹא', 'מַה', 'אֶת', 'זֶה', 'הוּא', 'הִיא', 'אֲנִי', 'אַתָּה', 'אַתְּ', 'הֵם',
    'שֶׁל', 'עַל', 'אֵל', 'בֵּין', 'עִם', 'כְּמֹו', 'גַּם', 'רַק', 'אוֹ', 'אִם',
    
    # Common word beginnings
    'מִ', 'בִּ', 'לִ', 'כְּ', 'שְׁ', 'הָ', 'וּ', 'יִ', 'תְּ', 'נְ',
    
    # Common word endings
    'תִי', 'תָּ', 'נוּ', 'תֶּם', 'הֶן', 'ךָ', 'כֶם', 'הָה', 'וֹת', 'תִּי',
    
    # Additional high-frequency syllables
    'רָה', 'לָה', 'יָה', 'נָה', 'מָה', 'בָּה', 'שָׁה', 'דָה', 'כָה', 'סָה',
    'רִי', 'לִי', 'יִי', 'נִי', 'מִי', 'בִּי', 'שִׁי', 'דִי', 'כִּי', 'סִי',
    'רוּ', 'לוּ', 'יוּ', 'נוּ', 'מוּ', 'בּוּ', 'שׁוּ', 'דוּ', 'כּוּ', 'סוּ',
    'רֶם', 'לֶם', 'יֶם', 'נֶם', 'מֶם', 'בֶּם', 'שֶׁם', 'דֶם', 'כֶּם', 'סֶם'
]

# Ensure we have exactly 100 syllables
assert len(COMMON_HEBREW_SYLLABLES) == 100, f"Expected 100 syllables, got {len(COMMON_HEBREW_SYLLABLES)}"

# Transliteration map for pronunciation guidance
SYLLABLE_PRONUNCIATION = {
    'בְּ': 'be', 'לְ': 'le', 'שֶׁ': 'she', 'הַ': 'ha', 'מֵ': 'me', 'כָּ': 'ka', 'תִּ': 'ti', 'וְ': 've', 'יְ': 'ye', 'נִ': 'ni',
    'רַ': 'ra', 'סֵ': 'se', 'עַ': 'a', 'פָּ': 'pa', 'צְ': 'tse', 'קֹ': 'ko', 'דָ': 'da', 'גַ': 'ga', 'זֶ': 'ze', 'חֹ': 'cho',
    'לֹא': 'lo', 'מַה': 'ma', 'אֶת': 'et', 'זֶה': 'ze', 'הוּא': 'hu', 'הִיא': 'hi', 'אֲנִי': 'ani', 'אַתָּה': 'ata', 'אַתְּ': 'at', 'הֵם': 'hem',
    'שֶׁל': 'shel', 'עַל': 'al', 'אֵל': 'el', 'בֵּין': 'bein', 'עִם': 'im', 'כְּמֹו': 'kemo', 'גַּם': 'gam', 'רַק': 'rak', 'אוֹ': 'o', 'אִם': 'im',
    'מִ': 'mi', 'בִּ': 'bi', 'לִ': 'li', 'כְּ': 'ke', 'שְׁ': 'she', 'הָ': 'ha', 'וּ': 'u', 'יִ': 'yi', 'תְּ': 'te', 'נְ': 'ne',
    'תִי': 'ti', 'תָּ': 'ta', 'נוּ': 'nu', 'תֶּם': 'tem', 'הֶן': 'hen', 'ךָ': 'kha', 'כֶם': 'khem', 'הָה': 'ha', 'וֹת': 'ot', 'תִּי': 'ti',
    'רָה': 'ra', 'לָה': 'la', 'יָה': 'ya', 'נָה': 'na', 'מָה': 'ma', 'בָּה': 'ba', 'שָׁה': 'sha', 'דָה': 'da', 'כָה': 'kha', 'סָה': 'sa',
    'רִי': 'ri', 'לִי': 'li', 'יִי': 'yi', 'נִי': 'ni', 'מִי': 'mi', 'בִּי': 'bi', 'שִׁי': 'shi', 'דִי': 'di', 'כִּי': 'ki', 'סִי': 'si',
    'רוּ': 'ru', 'לוּ': 'lu', 'יוּ': 'yu', 'נוּ': 'nu', 'מוּ': 'mu', 'בּוּ': 'bu', 'שׁוּ': 'shu', 'דוּ': 'du', 'כּוּ': 'ku', 'סוּ': 'su',
    'רֶם': 'rem', 'לֶם': 'lem', 'יֶם': 'yem', 'נֶם': 'nem', 'מֶם': 'mem', 'בֶּם': 'bem', 'שֶׁם': 'shem', 'דֶם': 'dem', 'כֶּם': 'kem', 'סֶם': 'sem'
}

def get_syllable_pronunciation(syllable):
    """Get pronunciation guide for a syllable"""
    return SYLLABLE_PRONUNCIATION.get(syllable, syllable)


def get_syllable_list():
    """Return the list of 100 most common Hebrew syllables"""
    return COMMON_HEBREW_SYLLABLES.copy()


def get_syllable_category(syllable):
    """Categorize a syllable by its structure"""
    if len(syllable) == 0:
        return "empty"
    
    has_consonant = any(c in HEBREW_CONSONANTS for c in syllable)
    has_vowel = any(c in HEBREW_VOWELS for c in syllable)
    
    if has_consonant and has_vowel:
        return "CV"  # Consonant-Vowel
    elif has_consonant:
        return "C"   # Consonant only
    elif has_vowel:
        return "V"   # Vowel only
    else:
        return "other"


def syllable_to_phonetic(syllable):
    """
    Convert Hebrew syllable to phonetic representation
    This is a simplified version - can be enhanced with proper Hebrew phonetic rules
    """
    # This would need proper Hebrew phonetic processing
    # For now, return the syllable as-is
    return syllable


if __name__ == "__main__":
    print(f"Total Hebrew syllables in database: {len(COMMON_HEBREW_SYLLABLES)}")
    print("\nFirst 10 syllables:")
    for i, syl in enumerate(COMMON_HEBREW_SYLLABLES[:10], 1):
        print(f"{i}. {syl} - Category: {get_syllable_category(syl)}")
