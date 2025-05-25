import streamlit as st
import openai

st.set_page_config(page_title="PiTA – AI Personal Trainer", layout="wide")
st.title("🏋️‍♂️ PiTA – Il tuo Assistente Virtuale di Personal Training")

# Configura la chiave OpenAI
openai.api_key = st.secrets["openai_api_key"]

# Chat con PiTA
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("💬 Chatta con PiTA")
user_input = st.text_input("Scrivi qui la tua domanda...")

if st.button("Invia") and user_input:
    st.session_state.chat_history.append(("👤 Tu", user_input))

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei PiTA, un assistente AI esperto in fitness, nutrizione e motivazione. Dai risposte brevi, chiare e motivanti."}
            ] + [{"role": "user", "content": msg[1]} for msg in st.session_state.chat_history if msg[0] == "👤 Tu"],
            max_tokens=300
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Errore: {e}"

    st.session_state.chat_history.append(("🤖 PiTA", reply))

for sender, msg in st.session_state.chat_history[::-1]:
    st.markdown(f"**{sender}:** {msg}")
