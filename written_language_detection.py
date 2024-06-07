from language_detection import detect_language
from load_dictionary import load_dictionaries


def main():

    # TO CHANGE BY THE USER
    output_folder = "C://Users//ronb3//Documents//data_upskills"
    language_freqs, char_freqs = load_dictionaries(output_folder)

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
