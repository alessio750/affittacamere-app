import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

st.set_page_config(page_title="Gestione Affittacamere IA", page_icon="🏠", layout="centered")

st.title("🏠 Assistente Finanziario Affittacamere")
st.markdown("Carica le fatture di Aruba o il foglio degli incassi per analizzare i conti, confrontare i dati e ricevere consigli strategici.")

api_key = st.secrets["GEMINI_API_KEY"]

st.divider()

# Area caricamento file
uploaded_file = st.file_uploader("Trascina qui il file di Aruba (PDF/Excel) o il file degli incassi", type=["pdf", "xlsx", "csv"])

if uploaded_file is not None:
    st.success("File caricato con successo!")

    # Mostra anteprima se è un file excel/csv
    if uploaded_file.name.endswith(('.xlsx', '.csv')):
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.write("Anteprima dati:")
            st.dataframe(df.head())
        except Exception as e:
            pass

    user_query = st.text_area("Fai una domanda all'assistente sui dati caricati:", placeholder="Es. Qual è la spesa più alta di questo mese? Ci sono aumenti rispetto all'anno scorso?")

    if st.button("Analizza con l'IA"):
        if user_query:
            with st.spinner("L'assistente sta analizzando i documenti..."):
                try:
                    # Legge il file come bytes per passarlo all'IA
                    bytes_data = uploaded_file.getvalue()

                    # Upload del file tramite l'API di Gemini
                    prompt = f"""
                    Sei l'assistente amministrativo e finanziario di un affittacamere.
                    Analizza il documento allegato (fatture, costi o incassi) e rispondi alla seguente richiesta dell'utente:

                    Richiesta: {user_query}

                    Fai calcoli precisi, evidenzia anomalie nei costi (utenze, fornitori) e dai consigli pratici su come ottimizzare la gestione.
                    """

                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=bytes_data,
                                mime_type=uploaded_file.type,
                            ),
                            prompt
                        ]
                    )

                    st.subheader("Risposta dell'Assistente:")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Si è verificato un errore durante l'analisi: {e}")
        else:
            st.warning("Scrivi prima una domanda per l'assistente.")
