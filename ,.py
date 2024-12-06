import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import wordnet
import networkx as nx
import re

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Function to add words and their relationships to the WordNet graph
def add_word_to_graph(G, word):
    synsets = wordnet.synsets(word)
    if synsets:
        main_node = synsets[0].lemmas()[0].name()
        G.add_node(main_node, label=main_node, color='violet')
        for syn in synsets:
            for lemma in syn.lemmas():
                related_word = lemma.name()
                if related_word != main_node:
                    G.add_node(related_word, label=related_word, color='pink')
                    G.add_edge(main_node, related_word)

# Function to create and display the WordNet graph
def create_wordnet_graph(input_words):
    G = nx.Graph()
    for word in input_words:
        add_word_to_graph(G, word.strip())

    for i in range(len(input_words)):
        for j in range(i + 1, len(input_words)):
            word1_synsets = wordnet.synsets(input_words[i].strip())
            word2_synsets = wordnet.synsets(input_words[j].strip())
            if word1_synsets and word2_synsets:
                word1 = word1_synsets[0].lemmas()[0].name()
                word2 = word2_synsets[0].lemmas()[0].name()
                G.add_edge(word1, word2)

    pos = nx.spring_layout(G, k=0.3)
    colors = [G.nodes[node]['color'] for node in G]
    labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, labels=labels, node_color=colors, with_labels=True, font_size=8, node_size=500, font_color='blue', font_weight='bold', edge_color='red')
    plt.title('Related Words for Given Inputs')
    plt.show()

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Astronomical_object"
response = requests.get(url)

# Parsing the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting the main content of the article
content = soup.find('div', {'class': 'mw-parser-output'})
paragraphs = content.find_all('p')
corpus = "\n".join([para.get_text() for para in paragraphs])

print("Text Corpus Preview:")
print(corpus[:500])

# Generate and display a Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(corpus)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Create a WordNet Diagram for the word "astronomy"
word = "astronomy"
synsets = wordnet.synsets(word)
G = nx.Graph()

# Add edges between the target word and its synsets
for synset in synsets:
    G.add_edge(word, synset.name())
    for lemma in synset.lemmas():
        G.add_edge(word, lemma.name())

# Add edges between synsets and their lemmas
for synset in synsets:
    for lemma in synset.lemmas():
        G.add_edge(synset.name(), lemma.name())

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
plt.title(f"WordNet Diagram for '{word}'")
plt.show()

# Extract and print occurrences of the word "object"
tokens = nltk.word_tokenize(corpus.lower())
word = 'object'
cfd = nltk.ConditionalFreqDist()

for sentence in nltk.sent_tokenize(corpus):
    if word in sentence.lower():
        cfd[word][sentence] += 1

total_occurrences = sum(cfd[word].values())
print(f"\nTotal occurrences of '{word}' in the text corpus: {total_occurrences}")

# Extract All Words That Start with a Vowel
words_starting_with_vowel = re.findall(r'\b[aeiouAEIOU]\w*', corpus)
print("Words starting with a vowel:", words_starting_with_vowel)

# Apply Regular Expressions and print only the first 10 matches for each
# a. [a-zA-Z]+ : Match any sequence of alphabetic characters
words_a = re.findall(r'[a-zA-Z]+', corpus)
print("a:", words_a[:10])

# b. [A-Z][a-z]* : Match any word starting with a capital letter followed by lowercase letters
words_b = re.findall(r'[A-Z][a-z]*', corpus)
print("b:", words_b[:10])

# c. p[aeiou]{,2}t : Match words that start with 'p', followed by 0-2 vowels, ending with 't'
words_c = re.findall(r'p[aeiou]{,2}t', corpus)
print("c:", words_c[:10])

# d. \d+(\.\d+)? : Match any integer or decimal number
numbers = re.findall(r'\d+(\.\d+)?', corpus)
print("d:", numbers[:10])

# e. ([^aeiou][aeiou][^aeiou])* : Match sequences of consonant-vowel-consonant patterns
patterns_e = re.findall(r'([^aeiou][aeiou][^aeiou])*', corpus)
print("e:", patterns_e[:10])

# f. \w+|[^\w\s]+ : Match any word or punctuation
words_f = re.findall(r'\w+|[^\w\s]+', corpus)
print("f:", words_f[:10])

# Read input words and create a WordNet graph
input_file = 'C:/NLTK/sample.txt'
passage = ""
encodings = ['utf-8', 'latin-1', 'iso-8859-1']

for encoding in encodings:
    try:
        with open(input_file, 'r', encoding=encoding) as file:
            passage = file.read()
            break  
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        break
    except UnicodeDecodeError:
        print(f"Error: Cannot decode file with {encoding} encoding. Trying next encoding.")
    except Exception as e:
        print(f"An error occurred while reading the file with {encoding} encoding: {e}")

input_words = input("Enter words separated by commas: ").split(',')

create_wordnet_graph(input_words)
