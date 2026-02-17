import streamlit as st
import json
import os
import datetime

def v6_ui_render():
    st.set_page_config(layout="wide", page_title="HBVNB Master Strateji")
    
    # --- 🚀 OTOMATİK YENİLEME TETİKLEYİCİ (30 Saniye) ---
    @st.fragment(run_every="30s")
    def show_dashboard():
        dosya = "v6_canli_sonuclar.json"
        
        st.title("🚀 HBVNB MASTER STRATEJİ PANELİ")
        
        if os.path.exists(dosya):
            mtime = os.path.getmtime(dosya)
            son_zaman = datetime.datetime.fromtimestamp(mtime).strftime('%H:%M:%S')
            st.caption(f"Veri Durumu: CANLI | Son Mühür: {son_zaman} | Her 30sn'de bir güncellenir.")

            try:
                with open(dosya, "r", encoding="utf-8") as f:
                    veriler = json.load(f)
            except:
                veriler = []

            col_gunluk, col_orta, col_uzun = st.columns(3)

            with col_gunluk:
                st.markdown("### 🔥 GÜNLÜK AL-SAT (90+)")
                gunlukler = sorted([h for h in veriler if h['vade_tipi'] == "GUNLUK"], key=lambda x: x['skor'], reverse=True)[:10]
                for h in gunlukler:
                    with st.expander(f"🚀 #{h['hisse']} (Skor: %{h['skor']})"):
                        st.write(h['icerik'])

            with col_orta:
                st.markdown("### 📈 ORTA VADE (80-90)")
                ortalar = sorted([h for h in veriler if h['vade_tipi'] == "ORTA"], key=lambda x: x['skor'], reverse=True)[:3]
                for h in ortalar:
                    with st.expander(f"📈 #{h['hisse']} (Skor: %{h['skor']})"):
                        st.write(h['icerik'])

            with col_uzun:
                st.markdown("### 💎 UZUN VADE (PD/DD Odaklı)")
                uzunlar = sorted([h for h in veriler if h['vade_tipi'] == "UZUN"], key=lambda x: x['pd_dd'])[:3]
                for h in uzunlar:
                    with st.expander(f"💎 #{h['hisse']} (PD/DD: {h['pd_dd']})"):
                        st.write(h['icerik'])
        else:
            st.warning("📡 Veri bekleniyor... Lütfen v6_listener.py'nin çalıştığından emin olun.")

    show_dashboard()

if __name__ == "__main__":
    v6_ui_render()
