import streamlit as st
from openai import OpenAI

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Gestione Affittacamere IA", layout="wide")

st.title("Gestione Affittacamere - Assistente IA")
st.write("Trascina qui le fatture (PDF/Excel) o i file degli incassi e chiedi informazioni all'assistente.")

# Inizializzazione del client OpenAI usando i Secrets di Streamlit
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Errore di configurazione: inserisci la chiave 'OPENAI_API_KEY' nei Secrets di Streamlit Cloud.")
    st.stop()

# Sezione caricamento file
uploaded_files = st.file_uploader(
    "Trascina qui le fatture o i file degli incassi", 
    accept_multiple_files=True, 
    type=["pdf", "xlsx", "xls"]
)

if uploaded_files:
    st.success(f"{len(file_names := [f.name for f in uploaded_files])} file caricati con successo!")

# Inizializzazione della cronologia della chat nella sessione
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostriamo i messaggi precedenti della chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Casella di input per la domanda dell'utente
user_query = st.chat_input("Fai una domanda sui file caricati...")

if user_query:
    if not uploaded_files:
        st.warning("Per favore, carica prima almeno un file!")
    else:
        # Aggiungiamo subito la domanda dell'utente alla cronologia visibile
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generiamo la risposta dell'IA con ChatGPT
        with st.chat_message("assistant"):
            with st.spinner("L'assistente sta analizzando i documenti..."):
                try:
                    file_names_str = ", ".join([f.name for f in uploaded_files])
                    
                    chat_completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user", 
                                "content": f"L'utente ha caricato questi file: {file_names_str}. Domanda: {user_query}"
                            }
                        ]
                    )
                    
                    bot_reply = chat_completion.choices[0].message.content
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    
                except Exception as e:
                    st.error(f"Errore tecnico dettagliato: {e}")
