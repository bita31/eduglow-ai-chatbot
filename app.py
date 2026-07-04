import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman web utama
st.set_page_config(page_title="EduGlow - AI Study Assistant", page_icon="🎓", layout="centered")

st.title("🎓 EduGlow: Personal Study Assistant")
st.caption("Asisten belajar interaktif bertenaga Gemini AI untuk membantu produktivitas Anda.")

# Input API Key dari pengguna via Sidebar demi keamanan
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
    st.markdown("---")
    st.markdown("### Karakter Chatbot:")
    st.write("- **Domain:** Edukasi & Produktivitas")
    st.write("- **Gaya Bahasa:** Santai dan suportif")
    st.write("- **Fitur:** Memory Percakapan")

if not api_key:
    st.info("Silakan masukkan Google Gemini API Key Anda di sidebar untuk memulai chat.", icon="🔑")
else:
    # Mengonfigurasi Gemini API
    genai.configure(api_key=api_key)
    
    # Menentukan System Instruction untuk memandu kepribadian AI
    system_instruction = (
        "Anda adalah EduGlow, seorang asisten belajar dan produktivitas pribadi yang cerdas untuk mahasiswa/pelajar. "
        "Gaya bahasa Anda harus santai, ramah, menyemangati, dan menggunakan analogi sederhana jika menjelaskan konsep sulit. "
        "Selalu berikan respons yang terstruktur (gunakan bullet points atau bolding jika perlu). "
        "Bantu pengguna menyusun jadwal, merangkum materi, atau menjawab pertanyaan akademik dengan tepat."
    )
    
    # Inisialisasi model dan session chat dalam memory Streamlit jika belum ada
    if "chat_session" not in st.session_state:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        st.session_state.chat_session = model.start_chat(history=[])
    
    # Menampilkan riwayat pesan yang ada di memori chat session
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)
            
    # Input dari pengguna
    if user_input := st.chat_input("Tanyakan materi kuliah atau minta buatkan jadwal belajar..."):
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("EduGlow sedang berpikir..."):
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)