import re
import logging

class V6AnalizMotoru:
    def __init__(self, hafiza_nesnesi=None):
        self.hafiza = hafiza_nesnesi

    def raporu_parcala(self, metin: str) -> list:
        try:
            bloklar = metin.split('━━━━━━━━━━━━━━━━━━━━')
            sonuclar = []

            for blok in bloklar:
                if not blok.strip() or "ANALİST" in blok: continue
                
                h_match = re.search(r'#(\w+)', blok)
                skor_match = re.search(r'Skor:\s*%(\d+)', blok)
                pd_dd_match = re.search(r'PD/DD:\s*([\d.]+)', blok)

                if h_match:
                    h_kod = h_match.group(1).upper()
                    skor = int(skor_match.group(1)) if skor_match else 0
                    pd_dd = float(pd_dd_match.group(1)) if pd_dd_match else 99.0
                    
                    # --- 🚀 10+3+3 VADE ETİKETLEME (MÜHÜRLÜ) ---
                    # Senior Developer Kararı: %90 ve üstü doğrudan GÜNLÜK MOMENTUM
                    if skor >= 90:
                        vade_tipi = "GUNLUK"
                    elif 80 <= skor < 90:
                        vade_tipi = "ORTA"
                    else:
                        vade_tipi = "UZUN"

                    sonuclar.append({
                        "hisse": h_kod,
                        "sinyal": "TAVAN ADAYI" if "TAVAN" in blok.upper() else "GÜÇLÜ",
                        "skor": skor,
                        "pd_dd": pd_dd,
                        "vade_tipi": vade_tipi,
                        "icerik": blok.strip()
                    })
            return sonuclar
        except Exception as e:
            logging.error(f"Analiz Hatası: {e}")
            return []