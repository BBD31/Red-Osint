import requests
from bs4 import BeautifulSoup

def check_telegram(username):
    if username.startswith("@"):
        username = username[1:]

    url = f"https://t.me/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)

        if "If you have <strong>Telegram</strong>" in response.text:
            print(f"[~] {username} here: {url}")
        elif "tgme_page_title" in response.text:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("div", class_="tgme_page_title").text.strip()
            desc = soup.find("div", class_="tgme_page_description")
            description = desc.text.strip() if desc else "null"
            print(f"[~] Знайдено: {url}")
            print(f"[~] Ім’я: {title}")
            print(f"[~] Опис: {description}")
        else:
            print(f"[~] {username} null")
    except Exception as e:
        print(f"[~] Помилка: {e}")

if __name__ == "__main__":
    username = input("[~] Telegram username (without @): ")
    check_telegram(username)
