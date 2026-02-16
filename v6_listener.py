import os
import asyncio
import json
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv
from modules.v6_hafiza import V6Hafiza
from modules.v6_analiz import V6AnalizMotoru

# Günlükleme Yapılandırması
logging.basicConfig(filename='v6_sistem.log', level=logging.INFO, format='%(asctime)s | %(message)s')

class V6MasterListener:
    def __init__(self):
        load_dotenv()
        self.api_id = os.getenv('V6_API_ID')
        self.api_hash = os.getenv('V6_API_HASH')
        self.kanal_id = -1003728280766 # Mühürlü Kanal
        
        self.hafiza = V6Hafiza()
        self.analiz = V6AnalizMotoru(self.hafiza)
        self.client = TelegramClient('v6_smart_session', self.api_id, self.api_hash)

    async def run(self):
        try:
            await self.client.start()
            print(">>> V6 MASTER SİSTEMİ: Telegram Canlı Dinleniyor... (Veri Birleştirme Modu Aktif)")

            @self.client.on(events.NewMessage(chats=self.kanal_id))
            async def handler(event):
                try:
                    # Yeni gelen raporu parçala
                    taze_firsatlar = self.analiz.raporu_parcala(event.raw_text)
                    
                    if taze_firsatlar:
                        # --- 🔄 VERİ BİRLEŞTİRME MANTIĞI ---
                        mevcut_veriler = []
                        if os.path.exists("v6_canli_sonuclar.json"):
                            with open("v6_canli_sonuclar.json", "r", encoding="utf-8") as f:
                                try:
                                    mevcut_veriler = json.load(f)
                                except:
                                    mevcut_veriler = []

                        # Aynı hissenin mükerrer yazılmaması için kontrol (Mühürlü)
                        mevcut_hisseler = {h['hisse'] for h in mevcut_veriler}
                        yeni_eklenen_sayisi = 0
                        
                        for yeni in taze_firsatlar:
                            if yeni['hisse'] not in mevcut_hisseler:
                                mevcut_veriler.append(yeni)
                                yeni_eklenen_sayisi += 1

                        # Güncellenmiş tam listeyi dosyaya mühürle
                        with open("v6_canli_sonuclar.json", "w", encoding="utf-8") as f:
                            json.dump(mevcut_veriler, f, ensure_ascii=False, indent=4)
                        
                        print(f"✔️ {yeni_eklenen_sayisi} yeni hisse eklendi. Toplam Portföy: {len(mevcut_veriler)}")
                        logging.info(f"Portföy güncellendi. Toplam hisse: {len(mevcut_veriler)}")
                except Exception as e:
                    logging.error(f"Mesaj İşleme Hatası: {e}")

            await self.client.run_until_disconnected()
        except Exception as e:
            print(f"KRİTİK SİSTEM HATASI: {e}")

if __name__ == "__main__":
    v6 = V6MasterListener()
    asyncio.run(v6.run())