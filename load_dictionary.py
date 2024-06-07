import os
import json
from collections import defaultdict, Counter
from tqdm import tqdm
import pandas as pd
import re


def get_character_pattern(alphabets=None):
    """
    Returns a compiled regular expression pattern for filtering characters
    based on the given alphabets.
    If no alphabets are provided, it defaults to including all Unicode ranges.

    Parameters:
    alphabets (str): A string containing the alphabets to include in the
    pattern.

    Returns:
    re.Pattern: A compiled regular expression pattern.
    """
    # Unicode ranges for different alphabets
    unicode_ranges = {
        'latin': r'a-zA-Z',
        'hiragana': r'\u3040-\u309F',
        'katakana': r'\u30A0-\u30FF',
        'cjk': r'\u4E00-\u9FAF',
        'arabic': r'\u0600-\u06FF\u0750-\u077F',
        'cyrillic': r'\u0400-\u04FF',
        'greek': r'\u0370-\u03FF',
        'thai': r'\u0E00-\u0E7F',
        'extended_latin': r'\u0100-\u017F'
    }

    # Construct pattern based on provided alphabets or include all Unicode
    # ranges
    if alphabets is None:
        pattern = ''.join(unicode_ranges.values())
    else:
        pattern = ''
        for alphabet in alphabets.split(','):
            pattern += unicode_ranges.get(alphabet.strip(), '')

    pattern = f'[^{pattern}]'
    return re.compile(pattern)


def constitute_dictionaries(data_frame, mode='word',
                            frequency_threshold=0.0002,
                            included_alphabets=None,
                            particular_languages=['ja', 'ar', 'th', 'zh',
                                                  'ur', 'ru']):
    """
    Constructs frequency dictionaries for words or characters from the
    given DataFrame.

    Parameters:
    data_frame (DataFrame): The input DataFrame with columns 'labels'
    and 'text'.
    mode (str): The mode for frequency calculation - 'word' or 'character'.
    frequency_threshold (float): The frequency threshold below which items
    are excluded (only applicable for 'word' mode).
    included_alphabets (str): A string containing the alphabets to include
    in the character pattern.

    Returns:
    dict: A dictionary with normalized frequency distributions.
    """
    frequency_dict = defaultdict(list)
    character_pattern = get_character_pattern(included_alphabets)

    # Populate frequencies based on the mode
    for index in tqdm(range(len(data_frame))):
        row = data_frame.iloc[index]
        language = row['labels']
        text = row['text'].lower()

        if mode == 'word':
            if language not in particular_languages:
                tokens = text.split()
                frequency_dict[language].extend(tokens)
        elif mode == 'character':
            filtered_text = character_pattern.sub('', text)
            frequency_dict[language].extend(filtered_text)
        else:
            raise ValueError("Invalid mode. Choose 'word' or 'character'.")

    # Normalize frequencies
    normalized_frequency_dict = {}
    for language, items in frequency_dict.items():
        item_counts = Counter(items)
        total_count = sum(item_counts.values())

        if mode == 'word' and frequency_threshold:
            filtered_counts = {item: count for item, count
                               in item_counts.items()
                               if count / total_count >= frequency_threshold}
        else:
            filtered_counts = item_counts

        total_filtered_count = sum(filtered_counts.values())
        normalized_frequency_dict[language] = {item:
                                               count / total_filtered_count
                                               for item, count
                                               in filtered_counts.items()}
    return normalized_frequency_dict


if __name__ == "__main__":
    # Check if TRAIN_FOLDER_PATH environment variable is set
    train_folder_path = "C://Users//ronb3//Documents//data_upskills"
    # os.getenv("TRAIN_FOLDER_PATH")
    if train_folder_path is None:
        raise ValueError("TRAIN_FOLDER_PATH environment variable is not set.")

    # Construct the full path to the train.csv file
    train_csv_path = os.path.join(train_folder_path, "train.csv")

    # Load data frame from the specified path
    df_train = pd.read_csv(train_csv_path)

    # Check if OUTPUT_FILE_PREFIX environment variable is set, use default
    # if not set
    output_folder = "C://Users//ronb3//Documents//data_upskills"
    # os.getenv("OUTPUT_FOLDER", "frequency_dict_")
    if output_folder is None:
        raise ValueError("OUTPUT_FOLDER environment variable is not set.")

    # Iterate over modes (word, character) and create dictionaries
    for mode in ['word', 'character']:
        # Construct output file name
        output_file = os.path.join(output_folder, f"{'dict'}_{mode}.json")

        # Generate normalized frequency dictionary
        normalized_frequency_dict = constitute_dictionaries(df_train,
                                                            mode=mode)

        # Write the dictionary to a JSON file
        with open(output_file, "w", encoding='utf-8') as file:
            json_object = json.dumps(normalized_frequency_dict)
            file.write(json_object)
