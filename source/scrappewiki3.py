import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Tentukan URL halaman Wikipedia
url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

# Step 2: Lakukan permintaan untuk mendapatkan konten HTML
response = requests.get(url)
html_content = response.text

# Step 3: Parsing konten HTML menggunakan BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 4: Ambil konten artikel
article_content = soup.find('div', {'class': 'mw-parser-output'})

# Step 5: Ekstrak teks dari konten artikel
text = ''
for paragraph in article_content.find_all('p'):
    text += paragraph.get_text() + '\n'

# Step 6: Simpan teks ke dalam DataFrame
df = pd.DataFrame({'Article': [text]})

# Step 7: Simpan DataFrame ke file CSV
df.to_csv('wikipedia_article.csv', index=False)

print("Konten artikel telah disimpan ke dalam file 'wikipedia_article.csv'")