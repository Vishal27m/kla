import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
nltk.download('omw-1.4')

# Sample text
gfg = "Geeks for Geeks Geeks"

# Tokenize the text
words = word_tokenize(gfg)

# Create frequency distribution
fdist = FreqDist(words)

# Print the frequency distribution in the desired format
print(f"FreqDist({dict(fdist)})")

# Get synonyms and definitions using WordNet
for word in fdist:
    synonyms = []
    definitions = []
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
        definitions.append(syn.definition())
    synonyms = set(synonyms)  # Remove duplicates
    print(f"\nWord: {word}")
    print(f"Synonyms: {', '.join(synonyms)}")
    print(f"Definitions: {', '.join(definitions)}")
