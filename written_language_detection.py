import os
import json
from language_detecion import detect_language


def main():
    output_folder = "C://Users//ronb3//Documents//data_upskills"
    # os.getenv("OUTPUT_FOLDER", "frequency_dict_")
    if output_folder is None:
        raise ValueError("OUTPUT_FOLDER environment variable is not set.")

    for mode in ['word', 'character']:
        # Construct output file name
        output_file = os.path.join(output_folder, f"{'dict'}_{mode}.json")
        with open(output_file, "r") as file:
            if mode == 'word':
                language_freqs = json.load(file)
            if mode == 'character':
                char_freqs = json.load(file)

    print("Welcome to Language Detection!")
    print("Please enter a sentence:")
    sentence = input("> ")
    try:
        language = detect_language(sentence, language_freqs, char_freqs)
        print(f"The language of the sentence is: {language}")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
