import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

st.set_page_config(page_title="Gestione Affittacamere IA", page_icon="🏠", layout="centered")

st.title("🏠 Assistente Finanziario Affittacamere")
st.markdown("Carica le fatture di Aruba o il foglio degli incassi per analizzare i conti, confrontare i dati e ricevere consigli strategici.")

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.divider()

# Area caricamento file
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
        # Prepara la lista dei contenuti prendendo tutti i file caricati
        contents = []
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.getvalue()
            contents.append(
                types.Part.from_bytes(
                    data=bytes_data,
                    mime_type=uploaded_file.type,
                )
            )
        
        # Aggiungi il prompt testuale alla fine dei file
        prompt = f"""
        Sei l'assistente amministrativo e finanziario di un affittacamere.
        Analizza i documenti allegati (fatture, costi o incassi) e rispondi alla seguente richiesta dell'utente:
        
        Richiesta: {user_query}
        
        Fai calcoli precisi, evidenzia anomalie nei costi (utenze, fornitori) e dai consigli pratici su come ottimizzare la gestione.
        """
        contents.append(prompt)

        # Chiamata all'IA con il client configurato e il modello corretto
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents
        )

                    st.subheader("Risposta dell'Assistente:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Si è verificato un errore durante l'analisi: {e}")
        else:
            st.warning("Scrivi prima una domanda per l'assistente.")
