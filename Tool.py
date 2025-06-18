import requests
from bs4 import BeautifulSoup
import re

def parse_geo_and_id(username):
    if username.startswith("@"):
        username = username[1:]

    url = f"https://t.me/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to find user ID (if available in the page)
        user_id = None
        user_id_tag = soup.find(attrs={"data-user-id": True})
        if user_id_tag:
            user_id = user_id_tag["data-user-id"]

        # Get profile description
        desc_tag = soup.find("div", class_="tgme_page_description")
        description = desc_tag.text.strip() if desc_tag else ""

        # Try to find city and country in description, e.g. "Kyiv, Ukraine"
        city, country = None, None
        match = re.search(r"([A-ZА-Я][a-zа-я]+),\s*([A-ZА-Я][a-zа-я]+)", description)
        if match:
            city = match.group(1)
            country = match.group(2)

        print(f"[~] Username: {username}")
        print(f"[~] User ID: {user_id if user_id else 'Not available'}")
        print(f"[~] Description: {description if description else 'None'}")
        print(f"[~] City: {city if city else 'Not found in description'}")
        print(f"[~] Country: {country if country else 'Not found in description'}")

    except Exception as e:
        print(f"[~] Error: {e}")

if __name__ == "__main__":
    user = input("[#] Enter Telegram username (without @): ")
    parse_geo_and_id(user)
