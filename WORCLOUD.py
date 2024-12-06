
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.probability import FreqDist
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

def read_text(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()
    return text

# Sample text for the word cloud
file_path = 'C:/NLTK/sample.txt'

text = read_text(file_path)

# Tokenize and convert to lower case
words = word_tokenize(text.lower())

# Join the words back into a single string
words_string = ' '.join(words)

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words_string)

# Display the generated word cloud
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

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
