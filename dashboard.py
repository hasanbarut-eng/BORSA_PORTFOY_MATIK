import streamlit as st
import json
import os
from modules.v6_hafiza import V6Hafiza

def v6_ui_render():
    # Sayfa tasarımı tam genişlikte ve Master başlığıyla mühürleniyor
    st.set_page_config(layout="wide", page_title="HBVNB Master Strateji")
    
    # Kullanıcı Hbvnb olarak mühürlendi (Giriş ekranı ve sidebar kaldırıldı)
    user = "Hbvnb"
    hafiza = V6Hafiza(kullanici_adi=user)
    user_data = hafiza.yukle()

    # --- 🚀 ANA PANEL BAŞLIĞI ---
    st.title(f"🚀 {user.upper()} master strateji paneli")
    st.caption("Sistem Durumu: LOKAL MÜHÜRLÜ | Sidebar Devre Dışı")

    # Veriler v6_canli_sonuclar.json dosyasından çekilir
    if os.path.exists("v6_canli_sonuclar.json"):
        try:
            with open("v6_canli_sonuclar.json", "r", encoding="utf-8") as f:
                veriler = json.load(f)
        except Exception as e:
            st.error(f"Veri okuma hatası: {e}")
            veriler = []

        # --- ❗ STRATEJİK PORTFÖY ÖNERİSİ (10+3+3) ---
        st.subheader("❗ STRATEJİK PORTFÖY ÖNERİSİ")
        col_gunluk, col_orta, col_uzun = st.columns(3)

        # 1. GÜNLÜK AL-SAT (10 Hisse) - Skor >= 90 olanlar
        with col_gunluk:
            st.markdown("#### 🔥 GÜNLÜK AL-SAT (10)")
            gunlukler = [h for h in veriler if h.get('vade_tipi') == "GUNLUK"][:10]
            for h in gunlukler:
                with st.expander(f"🚀 #{h.get('hisse')} (Skor: %{h.get('skor')})"):
                    st.write(h.get('icerik'))

        # 2. ORTA VADE (3 Hisse) - Skor 80-90 arası olanlar
        with col_orta:
            st.markdown("#### 📈 ORTA VADE (3)")
            ortalar = [h for h in veriler if h.get('vade_tipi') == "ORTA"][:3]
            for h in ortalar:
                with st.expander(f"📈 #{h.get('hisse')} (Skor: %{h.get('skor')})"):
                    st.write(h.get('icerik'))

        # 3. UZUN VADE (3 Hisse) - PD/DD odaklı en düşük 3 hisse
        with col_uzun:
            st.markdown("#### 💎 UZUN VADE (3)")
            # PD/DD oranına göre küçükten büyüğe sırala
            uzunlar = sorted([h for h in veriler if h.get('vade_tipi') == "UZUN"], 
                            key=lambda x: x.get('pd_dd', 99))[:3]
            for h in uzunlar:
                pd_val = h.get('pd_dd', 'N/A')
                with st.expander(f"💎 #{h.get('hisse')} (PD/DD: {pd_val})"):
                    st.write(h.get('icerik'))
    else:
        st.warning("📡 Canlı raporlar bekleniyor... Lütfen v6_listener.py programını çalıştırın.")

if __name__ == "__main__":
    v6_ui_render()