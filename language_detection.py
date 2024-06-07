import numpy as np
import math
import re
from collections import Counter
from load_dictionary import get_character_pattern


def kl_divergence(p, q):
    epsilon = 1e-16
    p = np.asarray(p, dtype=np.float32)
    q = np.asarray(q, dtype=np.float32)

    # Adding a small value to avoid division by zero
    p = np.where(p == 0, epsilon, p)
    q = np.where(q == 0, epsilon, q)

    return np.sum(p * np.log(p / q))


def calculate_freq(text, mode='word', alphabets=None):
    """
    Calculate the frequency of tokens in the given text.

    Parameters:
    text (str): The input text.
    mode (str): The mode for frequency calculation - 'word' or 'character'.
    Defaults to 'word'.
    alphabets (str): A string containing the alphabets to include in the
    character pattern.

    Returns:
    dict: A dictionary containing the token frequencies.
    """
    if mode == 'word':
        tokens = text.lower().split()
    elif mode == 'character':
        pattern = get_character_pattern(alphabets=None)
        tokens = pattern.sub('', text)
    else:
        raise ValueError("Invalid mode. Choose either 'word' or 'character'.")

    token_counts = Counter(tokens)
    total_tokens = sum(token_counts.values())
    token_freq = {token: count / total_tokens for token, count in
                  token_counts.items()}
    return token_freq


def find_unique(char_freqs):
    """
    Finds unique characters for each language in the given character
    frequency dictionary.

    Parameters:
    char_freqs (dict): A dictionary where keys are language codes and values
    are dictionaries of character frequencies.

    Returns:
    dict: A dictionary where keys are language codes and values are sets
    of unique characters.
    """
    # Initialize a dictionary to store unique characters for each language
    unique_characters = {language: set(freqs.keys()) for language, freqs in
                         char_freqs.items()}

    # Iterate through each language
    for lang1 in char_freqs:
        for lang2 in char_freqs:
            if lang1 != lang2:
                # Remove characters from lang1 that are also in lang2
                unique_characters[lang1] -= set(char_freqs[lang2].keys())

    return unique_characters


def detect_language(text, language_freqs=None, char_freqs=None):
    """
    Detects the language of the given text using character and word
    frequencies.
    Parameters:
    text (str): The input text to detect the language for.
    language_freqs (dict): Dictionary of word frequencies
    for different languages.
    char_freqs (dict): Dictionary of character frequencies for
    different languages.

    Returns:
    str: The detected language.
    """
    # Calculate frequencies for text characters and words
    word_freqs = calculate_freq(text)

    # Find unique characters in each language
    unique_char_freqs = find_unique(char_freqs)

    # Filter out non-Latin characters from the text
    non_latin_pattern = re.compile(r'[a-z]')
    filtered_text = non_latin_pattern.sub('', text)
    filtered_char_freqs = calculate_freq(filtered_text, mode='character')

    # Check for unique characters in the text for early detection
    for language, unique_chars in unique_char_freqs.items():
        if len(set(filtered_char_freqs.keys()).intersection(unique_chars)) > 0:
            return language

    # Calculate KL divergence for each language
    kl_divergences = {}
    for language, freq_dist in language_freqs.items():
        common_tokens = set(word_freqs).union(freq_dist)
        p = [word_freqs.get(token, 0) for token in common_tokens]
        q = [freq_dist.get(token, 0) for token in common_tokens]

        if not any(p):
            kl_divergences[language] = math.inf
        else:
            kl_divergences[language] = kl_divergence(p, q)

    # Find the language with the minimum KL divergence
    detected_language = min(kl_divergences, key=kl_divergences.get)
    return detected_language
