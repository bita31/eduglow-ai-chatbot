import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman utama Streamlit
st.set_page_config(
    page_title="EduGlow - AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)

# Struktur Sidebar untuk Konfigurasi API Key
st.sidebar.title("⚙️ Konfigurasi")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("### Karakter Chatbot:")
st.sidebar.markdown("- **Domain:** Edukasi & Produktivitas")
st.sidebar.markdown("- **Gaya Bahasa:** Santai dan suportif")
st.sidebar.markdown("- **Fitur:** Memory Percakapan")

# Halaman Utama
st.title("🎓 EduGlow: Personal Study Assistant")
st.write("Asisten belajar interaktif bertenaga Gemini AI untuk membantu produktivitas Anda.")

# Instansiasi instruksi karakter AI (System Instruction)
system_instruction = (
    "Anda adalah EduGlow, seorang asisten belajar dan produktivitas yang cerdas. "
    "Gaya bahasa Anda harus santai, ramah, menyemangati, dan mudah dipahami oleh pelajar. "
    "Selalu berikan respons yang terstruktur (gunakan bullet points jika menjelaskan banyak hal). "
    "Bantu pengguna menyusun jadwal, merangkum materi, atau menjawab pertanyaan akademik."
)

# Memeriksa apakah API Key sudah dimasukkan
if not api_key:
    st.info("🔑 Silakan masukkan Google Gemini API Key Anda di sidebar untuk memulai chat.", icon="ℹ️")
else:
    # Konfigurasi library Google GenAI dengan API Key pengguna
    genai.configure(api_key=api_key)
    
    # Inisialisasi model menggunakan penulisan yang didukung sistem terbaru
    try:
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")

    # Mengatur penyimpanan riwayat chat di dalam memory session Streamlit
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Menampilkan riwayat chat yang sudah ada sebelumnya
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Menangkap input pesan baru dari pengguna
    user_input = st.chat_input("Tanyakan materi kuliah atau minta buatkan jadwal belajar...")

    if user_input:
        # Tampilkan pesan user ke layar secara langsung
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Kirim pesan ke Google Gemini dan tampilkan responsnya
        try:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response = st.session_state.chat_session.send_message(user_input)
                response_placeholder.markdown(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungi Gemini AI: {e}")
