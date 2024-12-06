import nltk
import re
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize

nltk.download('gutenberg')
nltk.download('punkt')

corpus = gutenberg.raw('melville-moby_dick.txt')
tokens = word_tokenize(corpus)
words = [word.lower() for word in tokens if word.isalpha()]

def words_ending_with(pattern):
    return [word for word in words if word.endswith(pattern)]

def words_matching_pattern(pattern):
    return [word for word in words if re.search(pattern, word)]

def words_with_special_patterns(pattern):
    return [word for word in words if re.search(pattern, word)]

def words_without_vowels():
    return [word for word in words if re.search(r'^[^aeiou]+$', word)]

def words_with_curly_braces_patterns(pattern):
    return [word for word in words if re.search(pattern, word)]

pattern_ending = 'er'
print("A)",words_ending_with(pattern_ending)[:10])

pattern_wildcard = r'.*ing' 
print("\nB)",words_matching_pattern(pattern_wildcard)[:10])

pattern_special = r'^un.*|.*ing$'
print("\nC)",words_with_special_patterns(pattern_special)[:10])

print("\nD)",words_without_vowels()[:10])

pattern_curly = r'^.{3}$'# Example: words with exactly 3 characters
print(words_with_curly_braces_patterns(pattern_curly)[:10])

pattern_curly = r'^.{,3}$'# Example: words with up to 3 characters
print(words_with_curly_braces_patterns(pattern_curly)[:10])

pattern_curly = r'^.{3,}$'  # Example: words with at least 3 characters
print(words_with_curly_braces_patterns(pattern_curly)[:10])

pattern_curly = r'^.{2,4}$'  # Example: words with between 2 and 4 characters
print(words_with_curly_braces_patterns(pattern_curly)[:10])

pattern_curly = r'a(b|c)e'  # Example: words containing 'abe' or 'ace'
print(words_with_curly_braces_patterns(pattern_curly)[:10])