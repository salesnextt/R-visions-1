import streamlit as st
import pandas as pd

# Lien de ton Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="R-Vision 1", page_icon="🎓", layout="centered")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

st.title("🚀 R-Vision 1")
st.write
st.markdown("---")

try:
    df = load_data()
    
    # On retire les thèmes que tu ne veux plus (comme 'Orientation' ou 'Job')
    themes_a_exclure = ['Orientation', 'Job', 'Méthode']
    df = df[~df['Thème'].isin(themes_a_exclure)]

    with st.sidebar:
        st.header("🎯 Filtres")
        matieres = st.multiselect("Matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

    filtered_df = df[df['Thème'].isin(matieres)]

    if st.button("🎲 Nouvelle question", use_container_width=True):
        st.session_state.current_q = filtered_df.sample().iloc[0]
        st.session_state.answered = False

    if 'current_q' in st.session_state:
        q = st.session_state.current_q
        st.info(f"**{q['Niveau']}** | **{q['Thème']}**")
        
        # Affichage de la question (supporte le LaTeX)
        st.markdown(f"### {q['Question']}")

        # On vérifie que les colonnes A, B, C, D existent bien dans la ligne
        options_labels = [f"A) {q['A']}", f"B) {q['B']}", f"C) {q['C']}", f"D) {q['D']}"]
        options_map = {"A": options_labels[0], "B": options_labels[1], "C": options_labels[2], "D": options_labels[3]}
        
        choice = st.radio("Sélectionnez votre réponse :", options_labels, index=None)

        if st.button("Valider ✅") and choice:
            st.session_state.answered = True
            st.session_state.user_choice = choice[0] # On prend juste la lettre A, B, C ou D

        if st.session_state.get('answered'):
            bonne_rep = str(q['Réponse']).strip()
            if st.session_state.user_choice == bonne_rep:
                st.success(f"Bravo ! La bonne réponse était la {bonne_rep}.")
            else:
                st.error(f"Faux. La réponse était la {bonne_rep}.")
            
            with st.expander("🔎 Explication technique"):
                st.write(q['Explication'])

except Exception as e:
    st.error(f"Erreur de configuration : {e}")
    st.write("Vérifie que ton Google Sheet possède bien les colonnes : Niveau, Thème, Question, Réponse, A, B, C, D, Explication")
