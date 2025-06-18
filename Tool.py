import requests
from telethon.sync import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from datetime import datetime
import os

def ip_lookup(ip=None):
    try:
        url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
        res = requests.get(url).json()

        country = res.get("country_name", "Unknown")
        region = res.get("region", "Unknown")
        city = res.get("city", "Unknown")
        ip_address = res.get("ip", ip or "Unknown")

        location_data = f"{ip_address} | {city}, {region}, {country}"
        return location_data
    except Exception as e:
        return f"Location unavailable: {e}"

def save_log(data):
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n" + "-"*40 + "\n")

print("[~] PowerTG-OSINT started")
api_id = int(input("[~] Enter your API ID: "))
api_hash = input("[~] Enter your API HASH: ")
username = input("[~] Enter target Telegram username (without @): ")

with TelegramClient("osint_session", api_id, api_hash) as client:
    try:
        user = client.get_entity(username)
        full = client(GetFullUserRequest(user.id))

        bio = getattr(full.full_user, 'about', 'Not set')
        lang = getattr(full.full_user, 'lang_code', 'Unknown')
        photo_url = f"https://t.me/i/userpic/320/{user.username}.jpg"

        info = f"""
[~] Username: @{user.username}
[~] ID: {user.id}
[~] Name: {user.first_name or ''} {user.last_name or ''}
[~] Is Bot: {"Yes" if user.bot else "No"}
[~] Phone Public: {getattr(user, 'phone', 'Hidden')}
[~] Bio: {bio}
[~] Profile Picture: {photo_url}
[~] Common Chats: {full.common_chats_count}
[~] Status: {user.status.__class__.__name__}
[~] Language (inferred): {lang}
"""
        print(info)
        save_log(info)
    except Exception as e:
        print("[!] Error:", e)

print("[~] --- Geo IP Lookup ---")
target_ip = input("[~] Enter target IP (or leave blank to get your IP): ").strip()
location = ip_lookup(target_ip if target_ip else None)
print("[~] Location Info:")
print("[~] " + location)
save_log("GeoIP: " + location)
