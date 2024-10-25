import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_and_save_wikipedia_article(url, article_filename, table_filename):
    # Step 1: Lakukan permintaan untuk mendapatkan konten HTML
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Gagal mengambil halaman. Status code: {response.status_code}")
        return
    html_content = response.text

    # Step 2: Parsing konten HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Ambil konten artikel (paragraf)
    article_content = soup.find('div', {'class': 'mw-parser-output'})

    # Debugging untuk memastikan elemen ditemukan
    if article_content is None:
        print("Konten artikel tidak ditemukan.")
        return
    else:
        print("Konten artikel ditemukan.")
        # Cetak snippet untuk debugging
        print("Snippet dari article_content:", article_content.prettify()[:500])

    # Step 4: Ekstrak seluruh teks dari mw-parser-output
    text = article_content.get_text(separator='\n')

    # Debugging untuk memastikan teks berhasil diekstrak
    if text.strip() == '':
        print("Tidak ada teks yang ditemukan di dalam konten artikel.")
    else:
        print("Teks ditemukan, mulai menulis ke file.")

    # Step 5: Simpan konten artikel ke dalam DataFrame
    df_article = pd.DataFrame({'Article': [text]})

    # Step 6: Simpan artikel ke file CSV
    df_article.to_csv(article_filename, index=False)
    print(f"Konten artikel telah disimpan ke dalam file '{article_filename}'")

    # Step 7: Ekstrak tabel (jika ada)
    try:
        tables = pd.read_html(html_content)
    except ValueError:
        tables = []

    # Step 8: Simpan setiap tabel ke dalam file CSV jika ada tabel
    if tables:
        for idx, table in enumerate(tables):
            table.to_csv(f'{table_filename}_table_{idx + 1}.csv', index=False)
        print(f"{len(tables)} tabel telah disimpan ke dalam file '{table_filename}_table_X.csv'")
    else:
        print("Tidak ada tabel yang ditemukan di halaman ini.")

# Menggunakan fungsi untuk URL Wikipedia yang diberikan dan nama file output
url = 'https://en.wikipedia.org/wiki/Billboard_and_Vibe%27s_50_Greatest_Rappers_of_All_Time'
article_filename = 'wikipedia_article.csv'
table_filename = 'wikipedia_tables'
fetch_and_save_wikipedia_article(url, article_filename, table_filename)
