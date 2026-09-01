import streamlit as st
from groq import Groq

# Inizializziamo il client Groq prendendo la chiave dalle secrets di Streamlit
client = Groq(api_key="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")

st.set_page_config(page_title="Assistente Affittacamere", page_icon="🏠")

st.title("🏠 Assistente Virtuale Affittacamere")
st.write("Carica i documenti e fai domande all'intelligenza artificiale.")

# Inizializziamo la cronologia della chat se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostriamo tutti i messaggi precedenti della chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caricamento file multiplo
uploaded_files = st.file_uploader(
    "Trascina qui le fatture (PDF/Excel) o i file degli incassi",
    type=["pdf", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file caricati con successo!")

# Casella di testo per la domanda dell'utente
user_query = st.chat_input("Fai una domanda all'assistente sui dati caricati...")

if user_query:
    if not uploaded_files:
        st.warning("Per favore, carica prima almeno un file!")
    else:
        # Aggiungiamo subito la domanda dell'utente alla cronologia visibile
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generiamo la risposta dell'IA
        with st.chat_message("assistant"):
            with st.spinner("L'assistente sta analizzando i documenti..."):
                try:
                    file_names = ", ".join([f.name for f in uploaded_files])
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"L'utente ha caricato questi file: {file_names}. Domanda dell'utente: {user_query}"}]
                    )
                    bot_reply = chat_completion.choices[0].message.content
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    error_message = f"Si è verificato un errore durante l'analisi con l'IA: {e}"
                    st.error(error_message)
