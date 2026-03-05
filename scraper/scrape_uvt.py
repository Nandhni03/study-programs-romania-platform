import json
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://admitere.uvt.ro/procesul-de-admitere/programe-studii/"
PARAMS = "?type=toate-programele&ciclul-de-studii=licenta&pg={}"

programs = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page_num = 1
    while True:
        url = BASE_URL + PARAMS.format(page_num)
        print(f"Scraping page {page_num}...")
        page.goto(url)
        page.wait_for_timeout(5000)  # wait for JS

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".grid-item")

        if not cards:
            print("No more programs found. Stopping.")
            break

        for card in cards:
            title_el = card.select_one("h4.case27-primary-text")
            link_el = card.select_one("a")
            faculty = card.get("data-category-text")
            if not faculty and link_el:
                parts = link_el["href"].split("/")
                if len(parts) > 4:
                    faculty = parts[4].replace("-", " ").title()
                else:
                    faculty = "Unknown"

            lang_el = card.select_one(".listing-language")
            language = lang_el.text.strip() if lang_el else "Română"

            if title_el and link_el:
                programs.append({
                    "university": "UVT",
                    "program": title_el.text.strip(),
                    "faculty": faculty.strip() if faculty else "Unknown",
                    "url": link_el["href"],
                    "degree": "Licenta",
                    "language": language,
                    "city": "Timisoara",
                    "lat": None,
                    "lng": None
                })

        page_num += 1
        time.sleep(1)

    browser.close()

# SCreate and Save JSON
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(exist_ok=True)

json_file = data_dir / "uvt_programs_raw.json"

# Always write fresh, encoding utf-8
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(programs, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {len(programs)} programs to {json_file}")

print(f"Done! Extracted {len(programs)} programs across {page_num-1} pages!")