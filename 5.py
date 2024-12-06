import re
import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize

# Download the necessary NLTK data
nltk.download('gutenberg')
nltk.download('punkt')

# Load and tokenize the text corpus
corpus = gutenberg.raw('austen-emma.txt')
tokens = word_tokenize(corpus)

# Function to extract words based on a pattern
def extract_words(tokens, pattern):
    regex = re.compile(pattern)
    return [word for word in tokens if regex.search(word)]

pattern_with_ranges = r'\b\a{4,7}\b'
textonyms_with_ranges = extract_words(tokens, pattern_with_ranges)
print(f"Textonyms with 4 to 7 characters (using ranges): {textonyms_with_ranges[:100]}")

patterns_without_ranges = [r'\b\a{4}\b', r'\b\a{5}\b', r'\b\a{6}\b', r'\b\w{7}\b']
textonyms_without_ranges = []
for pattern in patterns_without_ranges:
    textonyms_without_ranges.extend(extract_words(tokens, pattern))
print(f"Textonyms with 4 to 7 characters (without using ranges): {textonyms_without_ranges[:100]}")


pattern_star = r'a*'  
words_with_star = extract_words(tokens, pattern_star)
print(f"Words with pattern 'a*': {words_with_star[:100]}")

pattern_plus = r'm+'  
words_with_plus = extract_words(tokens, pattern_plus)
print(f"Words with pattern 'a+': {words_with_plus[:100]}")
