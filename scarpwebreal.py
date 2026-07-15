import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def parse_page():
    """Одна итерация парсинга — возвращает список словарей"""
    resp = requests.get("https://bina.az/", headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "lxml")

    s = []
    card = soup.find_all("div", class_="sc-dbf80956-2 dkgyVD item-card")
    for i in card:
        card_more_div = i.find("div", class_="sc-b327383c-0 sc-b327383c-2 sc-dbf80956-15 imcXHf etkIhJ dJqvrS")
        if card_more_div is None:
            continue

        price_block = card_more_div.find("div", class_="sc-b327383c-0 sc-b327383c-3 imcXHf fJzfNg")
        price_container = price_block.find(
            "span", class_="sc-283548f-0 cXiQFh sc-dbf80956-13 cUqUUl price-container"
        ) if price_block else None
        if price_container is None:
            continue

        spans = price_container.find_all("span", recursive=False)
        price = spans[0].get_text(strip=True)
        period = spans[-1].get_text(strip=True)

        card_place = card_more_div.find("span", class_="sc-283548f-0 fbvGTp sc-dbf80956-16 jeTPnH").text
        card_all = card_more_div.find("span", class_="sc-283548f-0 fgtkNg sc-dbf80956-17 krTweC").find_all("span")

        card_komnati = card_all[0].get_text(strip=True) if len(card_all) > 0 else ""
        card_area = card_all[1].get_text(strip=True) if len(card_all) > 1 else ""
        card_floors = card_all[2].get_text(strip=True) if len(card_all) > 2 else ""

        loc_time = card_more_div.find("div", class_="sc-b327383c-4 hpcGwB").text.split(",")
        card_location = loc_time[0]
        card_day_time = loc_time[1].strip() if len(loc_time) > 1 else ""

        s.append({
            "qiymet": f"{price} {period}".strip(),
            "otaqlar": card_komnati,
            "sahe": card_area,
            "mertebe": card_floors,
            "erazi": card_place,
            "sheher": card_location,
            "gun ve vaxt": card_day_time,
            "parsed_at": pd.Timestamp.now()  # чтобы видеть, на какой итерации собрано
        })
    return s


all_data = []
start_time = time.time()
duration = 2 * 60      # 10 минут
interval = 5            # 5 секунд

iteration = 0
while time.time() - start_time < duration:
    iter_start = time.time()
    iteration += 1
    try:
        data = parse_page()
        all_data.extend(data)
        print(f"[{iteration}] собрано {len(data)} карточек, всего {len(all_data)}")
    except Exception as e:
        print(f"[{iteration}] ошибка: {e}")

    elapsed = time.time() - iter_start
    sleep_time = max(0, interval - elapsed)
    time.sleep(sleep_time)

df = pd.DataFrame(all_data)
# опционально: убрать дубликаты, если одни и те же объявления попались на разных итерациях
# df = df.drop_duplicates(subset=["qiymet", "otaqlar", "sahe", "erazi", "sheher"])

print(df.shape)
df.drop_duplicates(inplace=True)
df.to_csv("bina_data.csv", index=False, encoding="utf-8-sig")
