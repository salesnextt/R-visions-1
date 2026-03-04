import streamlit as st
import pandas as pd

# Ton lien de publication Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="R-Vision 1", page_icon="🎓", layout="centered")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# Titre demandé
st.title("🚀 R-Vision 1")
st.markdown("---")

try:
    df = load_data()
    
    with st.sidebar:
        st.header("🎯 Filtres")
        niveaux = st.multiselect("Niveaux", options=df['Niveau'].unique(), default=list(df['Niveau'].unique()))
        matieres = st.multiselect("Matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

    mask = df['Niveau'].isin(niveaux) & df['Thème'].isin(matieres)
    filtered_df = df[mask]

    if filtered_df.empty:
        st.warning("Aucune question trouvée.")
    else:
        if st.button("🎲 Nouvelle question", use_container_width=True):
            st.session_state.current_q = filtered_df.sample().iloc[0]
            st.session_state.reveal = False

        if 'current_q' in st.session_state:
            q = st.session_state.current_q
            
            st.info(f"**{q['Niveau']}** | **{q['Thème']}**")
            
            # Utilisation de st.write pour supporter le Markdown et le LaTeX
            st.markdown(f"### {q['Question']}")
            
            if st.button("💡 Voir la solution"):
                st.session_state.reveal = True
            
            if st.session_state.get('reveal'):
                # On affiche la réponse avec un style "Success"
                st.success("🎯 **Réponse :**")
                # Ici on utilise st.write qui interprète automatiquement le LaTeX entre $ $
                st.write(q['Réponse'])

except Exception as e:
    st.error(f"Erreur : {e}")
