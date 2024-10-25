from fastapi import APIRouter
from server.utils.schema import TaskTesting
from source.testscrappe import fetch_and_save_wikipedia_article  # Impor fungsi dari testscrappe.py
from source.calculation import person_age  # Impor fungsi person_age dari calculation.py
import os

main_route = APIRouter(tags=["main routes"])

@main_route.post("/api/v1/incites-hallo-world")
def post_incites_hallo_world(task: TaskTesting):
    age = person_age(task.birthyear)  # Fungsi person_age
    return {"content": f"hallo {task.name} to the world, you are {age} years old"}

# Route baru untuk Wikipedia scrapping
@main_route.get("/api/v1/scrape-wikipedia")
def scrape_wikipedia(url: str):
    # Taroh nama file output untuk artikel, tabel, dan list
    article_filename = "wikipedia_article_sections.csv"
    table_filename = "wikipedia_tables"
    list_filename = "wikipedia_lists.csv"

    # Code buat jalanin fungsi scrapping
    fetch_and_save_wikipedia_article(url, article_filename, table_filename, list_filename)

    # Code buat ngecek ngasih tau kalau file berhasil disimpan atau engga
    if os.path.exists(article_filename):
        return {"message": "Scraping successful", "article_file": article_filename}
    else:
        return {"message": "Scraping failed"}
