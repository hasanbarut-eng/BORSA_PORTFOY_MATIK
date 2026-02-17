import os
import asyncio
import json
from telethon import TelegramClient, events
from dotenv import load_dotenv
# MODÜL YOLU GÜNCELLENDİ
from modules.v6_analiz import V6AnalizMotoru

async def run_listener():
    load_dotenv()
    client = TelegramClient('v6_smart_session', os.getenv('V6_API_ID'), os.getenv('V6_API_HASH'))
    analiz = V6AnalizMotoru()
    kanal_id = -1003728280766 

    try:
        await client.start()
        print(">>> SISTEM AKTIF: Telegram dinleniyor...")

        @client.on(events.NewMessage(chats=kanal_id))
        async def handler(event):
            print(f"🔔 YENI MESAJ YAKALANDI!")
            taze_firsatlar = analiz.raporu_parcala(event.raw_text)
            
            if taze_firsatlar:
                mevcut = []
                if os.path.exists("v6_canli_sonuclar.json"):
                    with open("v6_canli_sonuclar.json", "r", encoding="utf-8") as f:
                        try: mevcut = json.load(f)
                        except: mevcut = []
                
                hisseler = {h['hisse']: h for h in mevcut}
                for yeni in taze_firsatlar:
                    hisseler[yeni['hisse']] = yeni
                
                with open("v6_canli_sonuclar.json", "w", encoding="utf-8") as f:
                    json.dump(list(hisseler.values()), f, ensure_ascii=False, indent=4)
                print(f"✅ {len(taze_firsatlar)} hisse mühürlendi.")

        await client.run_until_disconnected()
    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    asyncio.run(run_listener())
