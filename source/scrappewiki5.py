import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_and_save_wikipedia_article(url, article_filename, table_filename, list_filename):
    # Lakukan permintaan untuk mendapatkan konten HTML
    response = requests.get(url)
    if response.status_code != 200:
        return  # Gagal mengambil halaman, hentikan eksekusi
    html_content = response.text

    # Parsing konten HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ambil judul artikel
    article_title = soup.find('h1', {'id': 'firstHeading'})
    if article_title:
        article_title = article_title.get_text(strip=True)
    else:
        article_title = "Judul tidak ditemukan"

    # Ambil konten artikel (paragraf) dan section
    article_content = soup.find('div', {'id': 'mw-content-text'})
    if article_content is None:
        return  # Konten artikel tidak ditemukan, hentikan eksekusi

    # Pisahkan artikel berdasarkan section, termasuk konten di dalamnya
    sections = {}
    current_section = 'Introduction'  # Section default untuk artikel yang tidak punya heading awal
    section_text = []

    # Ambil semua heading dan konten yang relevan (h2 untuk section, p/ul/ol untuk konten)
    for tag in article_content.find_all(['h2', 'p', 'ul', 'ol', 'table']):
        # Jika tag adalah heading section
        if tag.name == 'h2':
            if section_text:  # Jika ada konten di section sebelumnya, simpan dulu
                sections[current_section] = '\n'.join(section_text)
            current_section = tag.get_text(strip=True)  # Ambil nama section dari heading
            section_text = []  # Reset konten untuk section baru
        
        # Jika tag adalah paragraf atau list, tambahkan kontennya ke section saat ini
        elif tag.name == 'p':
            section_text.append(tag.get_text(strip=True))

        # Jika ada tabel, tandai tabel di dalam section
        elif tag.name == 'table':
            section_text.append('Tabel ditemukan, akan disimpan secara terpisah.')

        # Jika tag adalah ul atau ol (list), tambahkan konten list ke section saat ini
        elif tag.name in ['ul', 'ol']:
            section_text.append(tag.get_text(strip=True))

    # Tambahkan section terakhir
    if section_text:
        sections[current_section] = '\n'.join(section_text)

    # Simpan artikel beserta section ke dalam DataFrame
    df_sections = pd.DataFrame(list(sections.items()), columns=['Section', 'Content'])

    # Simpan artikel berdasarkan section jadi file CSV
    df_sections.to_csv(article_filename, index=False)

    # Ekstrak tabel
    try:
        tables = pd.read_html(html_content)
    except ValueError:
        tables = []

    # Simpan setiap tabel ke dalam file CSV kalo ada tabel
    if tables:
        for idx, table in enumerate(tables):
            table.to_csv(f'{table_filename}_table_{idx + 1}.csv', index=False)

    # Ambil list (ul/ol) dari artikel
    lists = article_content.find_all(['ul', 'ol'])
    all_lists = []

    for l in lists:
        list_items = [li.get_text(strip=True) for li in l.find_all('li')]
        all_lists.append(list_items)

    # Simpan list ke file CSV
    if all_lists:
        df_lists = pd.DataFrame({'List': all_lists})
        df_lists.to_csv(list_filename, index=False)

# URL Wikipedia yang diberikan dan nama file output
url = 'https://en.wikipedia.org/wiki/Billboard_and_Vibe%27s_50_Greatest_Rappers_of_All_Time'
article_filename = 'wikipedia_article_sections.csv'
table_filename = 'wikipedia_tables'
list_filename = 'wikipedia_lists.csv'

fetch_and_save_wikipedia_article(url, article_filename, table_filename, list_filename)
