import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="Gestione Affittacamere IA", page_icon="🏠", layout="centered")

st.title("🏠 Assistente Finanziario Affittacamere")
st.markdown("Carica le fatture o il foglio degli incassi per analizzare i conti, confrontare i dati e ricevere consigli strategici.")

# Configurazione sicura della chiave API con la libreria classica
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Errore di configurazione: controlla che la GEMINI_API_KEY sia impostata correttamente nei Secrets di Streamlit.")

st.divider()

# Area caricamento file multiplo
uploaded_files = st.file_uploader("Trascina qui le fatture (PDF/Excel) o i file degli incassi", type=["pdf", "xlsx", "csv"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file caricati con successo!")

# Casella di testo per la domanda dell'utente
user_query = st.text_area("Fai una domanda all'assistente sui dati caricati:", placeholder="Es. Qual è la spesa più alta di questo mese?")

# Pulsante di analisi
if st.button("Analizza con l'IA"):
    if not uploaded_files:
        st.warning("Per favore, carica prima almeno un file!")
    elif not user_query.strip():
        st.warning("Scrivi una domanda per l'assistente prima di avviare l'analisi.")
    else:
        with st.spinner("L'assistente sta analizzando i documenti..."):
            try:
                # Inizializziamo il modello stabile e sicuro
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Inviamo la richiesta di base all'IA
                response = model.generate_content(user_query)
                
                # Mostriamo il risultato all'utente
                st.subheader("Risposta dell'Assistente:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Si è verificato un errore durante l'analisi con l'IA: {e}")
