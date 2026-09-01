import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="Gestione Affittacamere IA", page_icon="🏠", layout="centered")

st.title("🏠 Assistente Finanziario Affittacamere")
st.markdown("Carica le fatture di Aruba o il foglio degli incassi per analizzare i conti, confrontare i dati e ricevere consigli strategici.")

# Configurazione semplice e sicura con la libreria classica
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.divider()

# Area caricamento file multiplo
uploaded_files = st.file_uploader("Trascina qui le fatture di Aruba (PDF/Excel) o i file degli incassi", type=["pdf", "xlsx", "csv"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file caricati con successo!")

    # Mostra anteprima se tra i file c'è un file excel/csv
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(('.xlsx', '.csv')):
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.write(f"Anteprima dati ({uploaded_file.name}):")
                st.dataframe(df.head())
            except Exception as e:
                pass

user_query = st.text_area("Fai una domanda all'assistente sui dati caricati:", placeholder="Es. Qual è la spesa più alta di questo mese? Ci sono aumenti rispetto all'anno scorso?")

if st.button("Analizza con l'IA"):
    if user_query:
        with st.spinner("L'assistente sta analizzando i documenti..."):
            try:
                # Prepara i file nel formato supportato dalla libreria classica
                contents = []
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.getvalue()
                    contents.append({
                        'mime_type': uploaded_file.type,
                        'data': bytes_data
                    })
                
                # Aggiungi il prompt testuale alla fine
                prompt = f"""
                Sei l'assistente amministrativo e finanziario di un affittacamere.
                Analizza i documenti allegati (fatture, costi o incassi) e rispondi alla seguente richiesta dell'utente:
                
                Richiesta: {user_query}
                
                Fai calcoli precisi, evidenzia anomalie nei costi (utenze, fornitori) e dai consigli pratici su come ottimizzare la gestione.
                """
                contents.append(prompt)

                # Chiamata pulita con il modello flash
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(contents)
                
                st.subheader("Risposta dell'Assistente:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Si è verificato un errore durante l'analisi: {e}")
    else:
        st.warning("Scrivi prima una domanda per l'assistente.")
