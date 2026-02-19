import re
import logging

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    filename='v6_sistem.log',
    filemode='a'
)

class V6AnalizMotoru:
    def __init__(self):
        # Sinyal tiplerini ve karşılık gelen verileri mühürlemek için anahtar kelimeler
        self.kategoriler = {
            "TAVAN ADAYI": {"vade": "GUNLUK", "skor": 98, "etiket": "🚀 TAVAN ADAYI"},
            "ORTA VADE": {"vade": "ORTA", "skor": 85, "etiket": "🛡️ ORTA VADE"},
            "UZUN VADE": {"vade": "UZUN", "skor": 75, "etiket": "💎 UZUN VADE"}
        }

    def raporu_parcala(self, metin: str) -> list:
        """
        Telegram mesajını dürüst bir süzgeçten geçirir. 
        Zorlama yapmaz, sadece mesajda tanımlı olan kategorileri mühürler.
        """
        if not metin or len(metin.strip()) < 10:
            logging.warning("Analiz edilecek metin boş veya çok kısa.")
            return []

        firsatlar = []
        
        try:
            # Mesajı ana bölümlere ayır (Başlıklar genellikle emoji ile başlar veya çizgi ile ayrılır)
            # Bu regex, mesajdaki farklı vade gruplarını birbirinden ayırır.
            bloklar = re.split(r'(?=🚀|🛡️|💎|━━━━━━━━━━━━━━━━━━━━)', metin)
            
            su_anki_vade = None
            su_anki_skor = 70
            su_anki_baslik = "ANALİZ"

            for blok in bloklar:
                blok = blok.strip()
                if not blok:
                    continue

                # 1. KATEGORİ TESPİTİ (Zorlamayı engelleyen kısım)
                kategori_bulundu = False
                for anahtar, deger in self.kategoriler.items():
                    if anahtar in blok:
                        su_anki_vade = deger["vade"]
                        su_anki_skor = deger["skor"]
                        su_anki_baslik = deger["etiket"]
                        kategori_bulundu = True
                        break
                
                # Eğer blok bir kategori başlığı değilse ve daha önce bir kategori seçilmişse, hisseleri tara
                if su_anki_vade:
                    # Hisseleri yakala (Format: #HISSE | Fiyat: 1.23 TL)
                    # Regex: # sembolü ile başlayan 3-5 harfli büyük harf dizisini yakalar
                    hisse_satirlari = re.findall(r'#([A-Z-]{3,6})\s*\|\s*Fiyat:\s*([\d.]+)', blok)
                    
                    for hisse_kodu, fiyat in hisse_satirlari:
                        # Derin analiz içeriğini oluştur veya varsa ayıkla
                        derin_analiz = self._icerik_olustur(blok, hisse_kodu, fiyat, su_anki_baslik)
                        
                        firsat = {
                            "hisse": hisse_kodu,
                            "sinyal": su_anki_baslik.split()[-1], # Örn: "TAVAN ADAYI"
                            "skor": su_anki_skor,
                            "pd_dd": self._pd_dd_ayikla(blok), # Eğer metinde varsa ayıkla
                            "vade_tipi": su_anki_vade,
                            "icerik": derin_analiz
                        }
                        firsatlar.append(firsat)
                        logging.info(f"Mühürlendi: {hisse_kodu} | Kategori: {su_anki_vade}")

            return firsatlar

        except Exception as e:
            logging.error(f"Analiz motorunda beklenmedik hata: {str(e)}", exc_info=True)
            return []

    def _pd_dd_ayikla(self, metin: str) -> float:
        """Metin içindeki PD/DD oranını matematiksel olarak ayıklar."""
        match = re.search(r'PD/DD:\s*([\d.]+)', metin)
        return float(match.group(1)) if match else 0.0

    def _icerik_olustur(self, blok, hisse, fiyat, baslik):
        """Dashboard'da görünecek zengin metni hazırlar."""
        # Eğer mesajın içinde zaten o hisseye özel bir "DERİN ANALİZ" varsa onu al, yoksa standart şablon yap.
        if "💡 DERİN ANALİZ:" in blok:
            # Bloktan ilgili hissenin analizini kesip almayı deneyebiliriz 
            # (Basitlik ve sağlamlık için şimdilik blok içeriğini dürüstçe yansıtıyoruz)
            return blok
        
        return f"{baslik}\n━━━━━━━━━━━━━━━━━━━━\n#{hisse} | Fiyat: {fiyat} TL\n\nVeri akışına göre mühürlenmiştir."

# Test Bloğu
if __name__ == "__main__":
    motor = V6AnalizMotoru()
    test_msg = "🛡️ ORTA VADE YATIRIM\n━━━━━━━━━━━━━━━━━━━━\n#AKENR | Fiyat: 11.75 TL"
    print(motor.raporu_parcala(test_msg))
