import json
import os
import logging

class V6Hafiza:
    def __init__(self, kullanici_adi="Hbvnb"):
        """
        Hisseleri sadece yerel bilgisayarınızda saklayan, 10+3+3 yapısına uygun hafıza modülü.
        """
        self.kullanici_adi = kullanici_adi.lower().strip()
        self.dosya_yolu = f"data/portfoy_{self.kullanici_adi}.json"
        
        # Data klasörü mühürleniyor
        if not os.path.exists("data"):
            os.makedirs("data")
        
        self.load_data()

    def load_data(self):
        """Hisseleri yerel JSON dosyasından yükler."""
        try:
            if os.path.exists(self.dosya_yolu):
                with open(self.dosya_yolu, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                # 10+3+3 Yapısı için boş mühürlü şablon
                self.data = {
                    "ELIMDEKILER": [],
                    "KISA_VADE": [], 
                    "ORTA_VADE": [], 
                    "UZUN_VADE": []
                }
                self.save_data()
        except Exception as e:
            logging.error(f"Hafıza Yükleme Hatası: {e}")
            self.data = {"ELIMDEKILER": [], "KISA_VADE": [], "ORTA_VADE": [], "UZUN_VADE": []}

    def save_data(self):
        """Veriyi yerel dosyaya kalıcı olarak mühürler."""
        try:
            with open(self.dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            logging.error(f"Hafıza Kayıt Hatası: {e}")
            return False

    def yukle(self) -> dict:
        """Dashboard'a güncel veriyi teslim eder."""
        return self.data

    def elimdekileri_guncelle(self, hisse_listesi: list) -> bool:
        """Cüzdandaki (10+3+3) hisseleri günceller."""
        self.data["ELIMDEKILER"] = [h.strip().upper() for h in hisse_listesi if h.strip()]
        return self.save_data()

    def hisse_bende_var_mi(self, hisse_kodu: str) -> bool:
        """Hissenin portföyde olup olmadığını kontrol eder."""
        h_kod = hisse_kodu.upper()
        hepsi = []
        for k in ["KISA_VADE", "ORTA_VADE", "UZUN_VADE", "ELIMDEKILER"]:
            hepsi.extend(self.data.get(k, []))
        return h_kod in hepsi