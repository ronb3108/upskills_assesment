import os
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import accuracy_score

from language_detection import detect_language
from load_dictionary import load_dictionaries


def process_row(row, language_freqs, char_freqs):
    language = detect_language(row['text'], language_freqs, char_freqs)
    return language


def compute_accuracy(df, language_freqs, char_freqs):
    df_copy = df.copy()
    tqdm.pandas()

    def detection():
        return lambda row: process_row(row, language_freqs, char_freqs)

    df_copy['detected_labels'] = df_copy.progress_apply(detection(), axis=1)
    accuracy = accuracy_score(df_copy['labels'], df_copy['detected_labels'])
    print(f'Accuracy: {accuracy * 100:.2f}%')
    return accuracy


if __name__ == "__main__":

    # TO CHANGE
    output_folder = "C://Users//ronb3//Documents//data_upskills"
    test_folder_path = "C://Users//ronb3//Documents//data_upskills"

    language_freqs, char_freqs = load_dictionaries(output_folder)

    # Construct the full path to the train.csv file
    test_csv_path = os.path.join(test_folder_path, "test.csv")
    df_test = pd.read_csv(test_csv_path)

    accuracy = compute_accuracy(df_test, language_freqs, char_freqs)
