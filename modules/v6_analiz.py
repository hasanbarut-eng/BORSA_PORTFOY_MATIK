import re
import logging

class V6AnalizMotoru:
    def __init__(self, hafiza_nesnesi=None):
        self.hafiza = hafiza_nesnesi

    def raporu_parcala(self, metin: str) -> list:
        try:
            # Mesajı "Hocamın borsa analizleri" ifadesine göre parçala
            bloklar = re.split(r'Hocamın borsa analizleri,', metin)
            sonuclar = []

            for blok in bloklar:
                if not blok.strip() or "ANALİST" in blok: continue
                
                # Regex ile Hisse, PD/DD ve RSI ayıklama
                hisse_match = re.search(r'#(\w+)', blok)
                pd_dd_match = re.search(r'PD/DD:\s*([\d.]+)', blok)
                rsi_match = re.search(r'RSI:\s*([\d.]+)', blok)
                
                if hisse_match:
                    h_kod = hisse_match.group(1).upper()
                    
                    # Başlığa göre Vade ve Skor Atama (90+ Günlük, 80-90 Orta)
                    if "TAVAN ADAYI" in blok:
                        vade_tipi = "GUNLUK"
                        skor = 98
                    elif "ORTA VADE" in blok:
                        vade_tipi = "ORTA"
                        skor = 85
                    else:
                        vade_tipi = "UZUN"
                        skor = 75

                    sonuclar.append({
                        "hisse": h_kod,
                        "sinyal": "TAVAN ADAYI" if "TAVAN" in blok else "GÜÇLÜ",
                        "skor": skor,
                        "pd_dd": float(pd_dd_match.group(1)) if pd_dd_match else 99.0,
                        "vade_tipi": vade_tipi,
                        "icerik": blok.strip()
                    })
            return sonuclar
        except Exception as e:
            logging.error(f"Analiz Hatası: {e}")
            return []
