from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd

def fetch_and_save_wikipedia_article(url, article_filename, table_filename, list_filename):
    # Set up Selenium WebDriver 
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Menjalankan Chrome di mode headless 
    service = Service('C:/chromedriver-win64/chromedriver.exe')  # Masukin path ChromeDriver 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Code buat buka URL
    driver.get(url)

    # Code untuk Scroll untuk memuat seluruh halaman
    scroll_pause_time = 2  # ini Waktu jeda antara scroll
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # code perintah buat Scroll ke bawah sampai akhir halaman
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # code buat tunggu halaman selesai dimuat
        time.sleep(scroll_pause_time)

        # Code buat hitung tinggi halaman setelah scroll
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Jika tinggi halaman tidak berubah, keluar dari loop
        last_height = new_height

    # Code buat ambil konten halaman yang udah di muat
    html_content = driver.page_source

    # Parsing konten HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Code buat ambil judul artikel
    article_title = soup.find('h1', {'id': 'firstHeading'})
    if article_title:
        article_title = article_title.get_text(strip=True)
    else:
        article_title = "Judul tidak ditemukan"

    # Code buat ambil konten artikel paragraf dan section
    article_content = soup.find('div', {'id': 'mw-content-text'})
    if article_content is None:
        return  # Konten artikel tidak ditemukan, hentikan eksekusi

    # Code buat pisahin artikel berdasarkan section termasuk konten 
    sections = {}
    current_section = 'Introduction'  # Section default untuk artikel yang tidak punya heading awal
    section_text = []

    # Code buat ambil semua heading dan konten (h2 untuk section, p/ul/ol untuk konten)
    for tag in article_content.find_all(['h2', 'p', 'ul', 'ol', 'table']):
        # Jika tag adalah heading section
        if tag.name == 'h2':
            if section_text:  # kalo ada konten di section sebelumnya, melakukan simpan dulu
                sections[current_section] = '\n'.join(section_text)
            current_section = tag.get_text(strip=True)  # Code buat ambil nama section dari heading
            section_text = []  # Reset konten untuk section baru
        
        # Code kalau tag adalah paragraf atau list, nanti bakal menambahkan kontennya ke section saat ini
        elif tag.name == 'p':
            section_text.append(tag.get_text(strip=True))

        # kalau ada tabel, tandai tabel di dalam section
        elif tag.name == 'table':
            section_text.append('Tabel ditemukan, akan disimpan secara terpisah.')

        # kalau tag adalah ul atau ol atau list, nanti bakal menambahkan kontennya ke section saat ini
        elif tag.name in ['ul', 'ol']:
            section_text.append(tag.get_text(strip=True))

    # Code buat tambahkan section terakhir
    if section_text:
        sections[current_section] = '\n'.join(section_text)

    # Code buat simpan artikel beserta section ke dalam DataFrame
    df_sections = pd.DataFrame(list(sections.items()), columns=['Section', 'Content'])

    # Code buat simpan artikel berdasarkan section jadi file CSV
    df_sections.to_csv(article_filename, index=False)

    # Code buat ekstrak tabel
    try:
        tables = pd.read_html(html_content)
    except ValueError:
        tables = []

    # Code buat simpan setiap tabel ke dalam file CSV kalo ada tabel
    if tables:
        for idx, table in enumerate(tables):
            table.to_csv(f'{table_filename}_table_{idx + 1}.csv', index=False)

    # Code buat ambil list (ul/ol) dari artikel di wikipedia
    lists = article_content.find_all(['ul', 'ol'])
    all_lists = []

    for l in lists:
        list_items = [li.get_text(strip=True) for li in l.find_all('li')]
        all_lists.append(list_items)

    # Simpan list ke file CSV
    if all_lists:
        df_lists = pd.DataFrame({'List': all_lists})
        df_lists.to_csv(list_filename, index=False)

    driver.quit()

# URL Wikipedia yang diberikan dan nama file output
url = 'https://en.wikipedia.org/wiki/Billboard_and_Vibe%27s_50_Greatest_Rappers_of_All_Time'
article_filename = 'wikipedia_article_sections.csv'
table_filename = 'wikipedia_tables'
list_filename = 'wikipedia_lists.csv'

fetch_and_save_wikipedia_article(url, article_filename, table_filename, list_filename)
