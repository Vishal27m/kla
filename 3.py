import nltk
from nltk import sent_tokenize, word_tokenize, Text
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO

# Function to fetch and clean text from a URL
def fetch_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    raw_text = soup.get_text()
    cleaned_text = ' '.join(raw_text.split())
    return cleaned_text

# Function to fetch a table from a URL and convert it to a pandas DataFrame
def fetch_table_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table_html = soup.find('table')
    table_df = pd.read_html(StringIO(str(table_html)))[0]
    return table_df

# Define the URLs for text and table data
url_text = "https://www.york.ac.uk/teaching/cws/wws/webpage1.html"  
url_table = "https://www.w3schools.com/html/html_tables.asp"  

# Retrieve and process the raw text
text_raw = fetch_text_from_url(url_text)
words_tokenized = word_tokenize(text_raw)
text_processed = Text(words_tokenized)

# Analyze the text for a specific keyword
keyword = "HTML"  
print("\n---- Concordance Analysis ----")
text_processed.concordance(keyword)

# Display various text statistics
print("\n---- Text Statistics ----")
print(f'Total number of tokens: {len(words_tokenized)}')
print(f'Total number of characters in text: {len(text_raw)}')
sentences_tokenized = sent_tokenize(text_raw)
print(f'Total number of sentences: {len(sentences_tokenized)}')

# Show a sample of the lowercased text
sample_lowercased_text = text_raw.lower()[:100]
print("\n---- Sample Lowercased Text ----")
print(sample_lowercased_text)

# Find sentences starting with a specific word
start_word = "A"  
sentences_starting_with_word = [sentence for sentence in sentences_tokenized if sentence.startswith(start_word)]
print(f'\n---- Sentences Starting with "{start_word}" ----')
for i, sentence in enumerate(sentences_starting_with_word, 1):
    print(f'{i}. {sentence}')
o
# Retrieve and analyze the table data
table_data = fetch_table_from_url(url_table)

# Check and display distribution based on 'Company' column
print("\n---- Company Distribution ----")
if 'Company' in table_data.columns:
    company_distribution = table_data['Company'].value_counts()
    for company, count in company_distribution.items():
        print(f'{company}: {count}')
else:
    print('The specified column "Company" does not exist in the table.')
