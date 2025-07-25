from pyrogram import Client
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
REG_CHANNEL_ID = "maboypostbacksarbitraj"
USERS_FILE = Path(__file__).parent / 'users.json'

async def check_user_registered(user_id: int) -> bool:
    async with Client("check_session", api_id=API_ID, api_hash=API_HASH) as app:
        async for message in app.get_chat_history(REG_CHANNEL_ID, limit=100):
            if message.text and message.text.startswith(f"REG;UZ:{user_id}"):
                try:
                    with open(USERS_FILE, 'r+', encoding='utf-8') as f:
                        data = json.load(f)
                        for u in data.get("users", []):
                            if u["id"] == user_id:
                                u["reg"] = True
                                break
                        f.seek(0)
                        json.dump(data, f, ensure_ascii=False, indent=4)
                        f.truncate()
                except Exception as e:
                    print(f"Error updating user: {e}")
                return True
    return False
