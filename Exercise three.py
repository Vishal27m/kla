import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk import FreqDist
from wordcloud import STOPWORDS
from PIL import Image
from io import BytesIO
import os
import string
from IPython.display import display, Image as IPImage

# Function to fetch and parse the webpage content
def fetch_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to extract text content from the webpage
def extract_text(soup):
    content = soup.find('div', {'class': 'markdown-converter__text--rendered'})
    if content:
        paragraphs = content.find_all('p')
        text = ' '.join(paragraph.text for paragraph in paragraphs)
    else:
        text = soup.get_text()
    return text

# Function to tokenize and filter text
def tokenize_and_filter(text):
    tokens = nltk.word_tokenize(text)
    stopwords = set(STOPWORDS)
    punctuation = set(string.punctuation)
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords and word not in punctuation]
    return filtered_tokens

# Function to extract and process tables
def process_tables(soup):
    tables = soup.find_all('table')
    if tables:
        table_data = []
        for table in tables:
            headers = [header.text.strip() for header in table.find_all('th')]
            rows = table.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    cols = [ele.text.strip() for ele in cols]
                    if len(cols) == len(headers):
                        table_data.append(cols)
            
        if headers:
            df_table = pd.DataFrame(table_data, columns=headers)
        else:
            # If no headers, just return the data in a DataFrame without column names
            df_table = pd.DataFrame(table_data)
        
        return df_table
    return None


# Function to compute word frequency in a specific column
def compute_frequency_distribution(df_table, column_index, word_of_interest):
    if not df_table.empty:
        column_data = df_table.iloc[:, column_index].astype(str)
        column_text = ' '.join(column_data)
        column_tokens = nltk.word_tokenize(column_text)
        stopwords = set(STOPWORDS)
        punctuation = set(string.punctuation)
        column_filtered_tokens = [word for word in column_tokens if word.lower() not in stopwords and word not in punctuation]
        word_count = column_filtered_tokens.count(word_of_interest.lower())
        freq_dist = FreqDist(column_filtered_tokens)
        return word_count, freq_dist.most_common(10)
    return 0, []

# Function to download and display images
def download_and_display_images(soup, url, output_dir='images'):
    os.makedirs(output_dir, exist_ok=True)
    images = soup.find_all('img')
    image_urls = [img['src'] for img in images if 'src' in img.attrs]
    
    for idx, img_url in enumerate(image_urls):
        if not img_url.startswith('http'):
            img_url = requests.compat.urljoin(url, img_url)
        
        try:
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            
            # Determine the image format
            img_format = img_response.headers['Content-Type'].split('/')[1].upper()
            if img_format == 'SVG':
                print(f"Skipping SVG image: {img_url}")
                continue
            
            img = Image.open(BytesIO(img_response.content))
            
            # Display the image inline
            display(IPImage(data=img_response.content))
            
            # Save the image
            img_path = os.path.join(output_dir, f'image_{idx}.{img_format.lower()}')
            img.save(img_path, format=img_format)
            print(f"Image saved to {img_path}")
            
        except (requests.HTTPError, IOError) as e:
            print(f"Failed to process {img_url}: {e}")

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
soup = fetch_webpage(url)
text = extract_text(soup)
filtered_tokens = tokenize_and_filter(text)
nltk_text = nltk.Text(filtered_tokens)

if 'code' in filtered_tokens:
    nltk_text.concordance('code', lines=5)
else:
    print("The word 'code' is not in the text.")

print("Number of tokens:", len(filtered_tokens))
print("Raw text:", text[:500])
sentences = nltk.sent_tokenize(text)
print("Number of sentences:", len(sentences))

df_table = process_tables(soup)
if df_table is not None:
    print("Extracted table:")
    print(df_table.head())
    word_of_interest = 'immutable2222222222222222'
    word_count, most_common_words = compute_frequency_distribution(df_table, 1, word_of_interest)
    print(f"Frequency of '{word_of_interest}' in the selected column:", word_count)
    print("Frequency distribution of words in the selected column:")
    print(most_common_words)
else:
    print("No tables found on the webpage.")

if filtered_tokens:
    filtered_words = [word.lower() for word in filtered_tokens if word.lower().startswith('p')]
    print("Words that start with 'P':")
    print(filtered_words[:10])

    freq_dist_a = FreqDist(filtered_words)
    print("Frequency distribution of words starting with 'P':")
    print(freq_dist_a.most_common(10))
else:
    print("No tokens found for filtering.")

download_and_display_images(soup, url)
