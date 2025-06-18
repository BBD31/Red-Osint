from telethon import TelegramClient
import requests
import re
from telethon.tl.functions.users import GetFullUserRequest

api_id = 26571005  
api_hash = '5257cad47d1fffb8b97e57f15f0683ae'  

client = TelegramClient('session', api_id, api_hash)

def extract_ip(text):
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    match = re.search(ip_pattern, text)
    return match.group(0) if match else None

def get_geo_by_ip(ip):
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}").json()
        if data['status'] == 'success':
            return data.get('city', 'Unknown'), data.get('country', 'Unknown')
    except:
        pass
    return None, None

async def main(username):
    user = await client.get_entity(username)
    full = await client(GetFullUserRequest(user.id))
    bio = full.full_user.about or ""

    print(f"[~] Username: {user.username}")
    print(f"[~] ID: {user.id}")
    print(f"[~] Bio: {bio}")

    ip = extract_ip(bio)
    if ip:
        city, country = get_geo_by_ip(ip)
        print(f"[~] IP detected: {ip}")
        print(f"[~] Geo by IP: {city}, {country}")
    else:
        print("[~] No IP found in bio")

if __name__ == "__main__":
    import asyncio
    username = input("[#] Enter Telegram username (without @): ")
    with client:
        client.loop.run_until_complete(main(username))
