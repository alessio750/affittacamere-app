import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="Assistente virtuale affittacamere IA", page_icon="🏡​", layout="centered")

st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 2.5em;">🏡</span>
        <h1 style="margin: 0;">Assistente virtuale affittacamere IA</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("Carica le tue fatture o i file degli incassi e chiedi qualsiasi cosa all'IA.")
# Configurazione della chiave API segreta da Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Errore di configurazione: controlla che la GEMINI_API_KEY sia impostata correttamente nei Secrets di Streamlit.")

st.divider()

# 1. MEMORIA DELLA CHAT: Inizializziamo lo storico dei messaggi se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. MOSTRHIAMO LA CRONOLOGIA: Ridisegniamo tutti i messaggi precedenti sullo schermo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Area caricamento file multiplo
uploaded_files = st.file_uploader("Trascina qui le fatture (PDF/Excel) o i file degli incassi", type=["pdf", "xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file caricati con successo!")

# Casella di testo per la domanda dell'utente (usiamo st.chat_input per un look da chat perfetto)
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
                    # Inizializziamo il modello
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Prepariamo la lista dei file da inviare all'IA
                    file_parts = []
                    for uploaded_file in uploaded_files:
                        bytes_data = uploaded_file.getvalue()
                        file_parts.append({
                            "mime_type": uploaded_file.type,
                            "data": bytes_data
                        })
                    
                    # Uniamo i file e la domanda in un'unica richiesta
                    prompt_content = [user_query] + file_parts
                    
                    # Inviamo tutto all'IA
                    response = model.generate_content(prompt_content)
                    bot_reply = response.text
                    
                    # Mostriamo la risposta
                    st.markdown(bot_reply)
                    
                    # Salviamo anche la risposta dell'assistente nella cronologia
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                except Exception as e:
                    error_message = f"Si è verificato un errore durante l'analisi con l'IA: {e}"
                    st.error(error_message)
