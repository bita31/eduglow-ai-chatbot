import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="EduGlow - AI Study Assistant", page_icon="🎓", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Konfigurasi")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

# Halaman Utama
st.title("🎓 EduGlow: Personal Study Assistant")
st.write("Asisten belajar interaktif bertenaga Gemini AI untuk membantu produktivitas Anda.")

if not api_key:
    st.info("🔑 Silakan masukkan Google Gemini API Key Anda di sidebar untuk memulai.", icon="ℹ️")
else:
    # Memaksa konfigurasi menggunakan API versi v1 terbaru
    genai.configure(api_key=api_key, transport='rest')
    
    user_input = st.chat_input("Tanyakan materi kuliah atau minta buatkan jadwal belajar...")
    
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
            
        try:
            with st.chat_message("assistant"):
                # Menggunakan model standar terbaru yang pasti aktif di semua project AI Studio
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(user_input)
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
