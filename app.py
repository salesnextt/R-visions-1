import streamlit as st
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="R-Vision 1", page_icon="🎓", layout="centered")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

st.title("🚀 R-Vision 1")
st.markdown("---")

try:
    df = load_data()
    
    with st.sidebar:
        st.header("🎯 Filtres")
        matieres = st.multiselect("Matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

    filtered_df = df[df['Thème'].isin(matieres)]

    if st.button("🎲 Nouvelle question", use_container_width=True):
        st.session_state.current_q = filtered_df.sample().iloc[0]
        st.session_state.answered = False
        st.session_state.user_choice = None

    if 'current_q' in st.session_state:
        q = st.session_state.current_q
        st.info(f"**{q['Niveau']}** | **{q['Thème']}**")
        st.write(f"### {q['Question']}")

        # Préparation des options
        options = {
            f"A) {q['A']}": "A",
            f"B) {q['B']}": "B",
            f"C) {q['C']}": "C",
            f"D) {q['D']}": "D"
        }
        
        # Affichage du choix
        choice = st.radio("Sélectionnez votre réponse :", list(options.keys()), index=None)

        if st.button("Valider la réponse ✅") and choice:
            st.session_state.answered = True
            st.session_state.user_choice = options[choice]

        if st.session_state.get('answered'):
            if st.session_state.user_choice == str(q['Réponse']).strip():
                st.success(f"Bravo ! La bonne réponse était bien la {q['Réponse']}.")
            else:
                st.error(f"Dommage... La bonne réponse était la {q['Réponse']}.")
                st.write(f"**Explication :** {q.get('Explication', 'Réviser ce point pour la L2 !')}")

except Exception as e:
    st.error(f"Erreur : {e}")
