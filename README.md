# Upskills Assessment

## Thought Process

This assessment took me roughly 6 hours to complete.

1. **Initial Exploration**: I started by examining the data in a Jupyter notebook to understand its structure and characteristics. Therefore I decided to wee wich language where considered, the lenght of each sample...
2. **Unigram Analysis**: Using the `re` library, I identified that certain languages have unique characters, which can make them easily recognizable. 
3. **N-gram Analysis**: I expanded my analysis to include words, bigrams, and trigrams. I used the training dataset for training and the validation dataset for testing. 
4. **Data Structures and Storage**: I utilized the `collections` module to create dictionaries for each language for counting occurrences and the `json` and `os` libraries for storing these dictionaries. Statistics were calculated using the `math` and `numpy` libraries.
5. **Results**: Through this process, I found that analyzing words provided good results within a reasonable timeframe.

## Repository Usage

### Files

- **load_dictionary.py**: This script creates the dataset for the dictionaries. Run this first with the correct path to the training dataset folder. It requires the paths to the folders containing the dictionaries and the training dataset.
- **language_detection.py**: This script detects the language using unique character recognition and Kullback-Leibler (KL) distance on words, not bigrams and trigrams as in the article.
- **test.py**: This script computes the accuracy on the test dataset. It requires the paths to the folders containing the dictionaries and the test dataset.
- **written_language_detection.py**: This script is used to detect the language from text input. It requires the path to the dictionary folder.

All paths need to be adjusted manually.

## My Solution

The solution provides interesting results:
- **Performance**: The solution is reasonably fast, processing 10,000 text samples in approximately 3 minutes.
- **Accuracy**: It achieves an accuracy of 93.15% for 20 languages, which is slightly better than the original document, as each sample has, on average, one line of text.
- **Code Quality**: The code is functional and maintainable, though there is room for improvement.

## To Do

Several improvements can be made to this version:
- **Environment Variables**: Use environment variables for paths and ensure the correct version of each library is used.
- **Additional Parameters**: Consider using additional parameters, such as word length and word associations, to improve accuracy.
- **Error Analysis**: Conduct a more rigorous analysis of errors to refine the algorithm. This should be done on a large number of samples to understand and address individual errors more effectively.

