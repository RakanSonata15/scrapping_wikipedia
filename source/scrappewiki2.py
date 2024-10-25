import requests
from bs4 import BeautifulSoup

# URL halaman Wikipedia yang ingin discrape
url = "https://en.wikipedia.org/wiki/Web_scraping"

# Mengirim permintaan ke halaman
response = requests.get(url)


# Mengecek apakah permintaan berhasil
if response.status_code == 200:
    # Mengambil konten dari halaman
    soup = BeautifulSoup(response.content, 'html.parser')

    # Contoh mengambil judul halaman
    title = soup.find('h1').text
    print(f"Title: {title}")

    # Contoh mengambil semua paragraf di artikel
    paragraphs = soup.find_all('p')
    
    for i, paragraph in enumerate(paragraphs):
        print(f"Paragraph {i+1}: {paragraph.text}")

    

else:
    print(f"Failed to retrieve page with status code {response.status_code}")

