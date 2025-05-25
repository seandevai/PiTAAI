from openai import OpenAI
import streamlit as st
import datetime

# Configura API Key
client = OpenAI(api_key=st.secrets["open_ai_key"])

# === UI ===
st.set_page_config(page_title="PiTA – Personal Trainer AI", layout="wide")
st.title("🏋️‍♂️ PiTA – Il tuo Assistente Virtuale di Personal Training")

tab1, tab2 = st.tabs(["💬 Chat AI", "📅 Appuntamenti"])

# === CHAT ===
with tab1:
    st.subheader("Parla con PiTA")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Scrivi qui la tua domanda o richiesta...")

    if st.button("Invia") and user_input:
        st.session_state.chat_history.append(("👤 Tu", user_input))

        try:
            messages = [
                {"role": "system", "content": "Sei PiTA, un assistente AI esperto in personal training, alimentazione e benessere fisico. Dai consigli pratici e motivanti."}
            ] + [{"role": "user", "content": msg[1]} for msg in st.session_state.chat_history if msg[0] == "👤 Tu"]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300
            )
            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"❌ Errore: {e}"

        st.session_state.chat_history.append(("🤖 PiTA", reply))

    for sender, msg in st.session_state.chat_history[::-1]:
        st.markdown(f"**{sender}:** {msg}")

# === APPUNTAMENTI ===
with tab2:
    st.subheader("Gestione Appuntamenti Settimanali")

    if "appointments" not in st.session_state:
        st.session_state.appointments = []

    with st.form("appointment_form"):
        col1, col2 = st.columns(2)
        with col1:
            day = st.selectbox("Giorno", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"])
        with col2:
            time = st.time_input("Orario")

        note = st.text_input("Nota (es. Allenamento cardio, yoga...)")
        submitted = st.form_submit_button("Aggiungi Appuntamento")

        if submitted:
            st.session_state.appointments.append((day, time.strftime("%H:%M"), note))
            st.success("✅ Appuntamento aggiunto!")

    st.markdown("### 📋 Appuntamenti Salvati:")
    if st.session_state.appointments:
        for a in st.session_state.appointments:
            st.markdown(f"- **{a[0]} alle {a[1]}** – _{a[2]}_")
    else:
        st.info("Nessun appuntamento ancora inserito.")
