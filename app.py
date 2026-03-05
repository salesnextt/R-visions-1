import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lien de ton Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRcc-V3xEYUl_Mv05vjB_FMbo2mvjrFRTheCIkuQIuAVgcSw2ZcHDgbmupZORUYtNCVVCUG3Zt2SZTR/pub?output=csv"

st.set_page_config(page_title="R-Vision 1", page_icon="🎓", layout="centered")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    # On remplace les cases vides (NaN) par du texte vide pour éviter les erreurs d'affichage
    df = df.fillna('')
    return df

# --- SECTION QUIZ (Ta version améliorée) ---
def section_quiz():
    st.title("🚀 R-Vision 1 : Quiz")
    st.markdown("---")
    try:
        df = load_data()
        themes_a_exclure = ['Orientation', 'Job', 'Méthode']
        df = df[~df['Thème'].isin(themes_a_exclure)]

        with st.sidebar:
            st.header("🎯 Filtres")
            matieres = st.multiselect("Matières", options=df['Thème'].unique(), default=list(df['Thème'].unique()))

        filtered_df = df[df['Thème'].isin(matieres)]

        if st.button("🎲 Nouvelle question", use_container_width=True):
            if not filtered_df.empty:
                st.session_state.current_q = filtered_df.sample().iloc[0]
                st.session_state.answered = False
            else:
                st.warning("Aucune question ne correspond à tes filtres.")

        if 'current_q' in st.session_state:
            q = st.session_state.current_q
            st.info(f"**{q['Niveau']}** | **{q['Thème']}**")
            st.markdown(f"### {q['Question']}")

            # Construction des labels proprement
            options_labels = [f"A) {q['A']}", f"B) {q['B']}", f"C) {q['C']}", f"D) {q['D']}"]
            choice = st.radio("Sélectionnez votre réponse :", options_labels, index=None)

            if st.button("Valider ✅") and choice:
                st.session_state.answered = True
                st.session_state.user_choice = choice[0]

            if st.session_state.get('answered'):
                bonne_rep = str(q['Réponse']).strip()
                if st.session_state.user_choice == bonne_rep:
                    st.success(f"Bravo ! La bonne réponse était la {bonne_rep}.")
                else:
                    st.error(f"Faux. La réponse était la {bonne_rep}.")
                
                if q['Explication']:
                    with st.expander("🔎 Explication technique"):
                        st.write(q['Explication'])
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- SECTION SIMULATEUR IS-LM ---
def section_simulateur():
    st.title("📈 Simulateur IS-LM")
    st.write("Modélisation des chocs macroéconomiques.")
    
    g = st.slider("Dépenses Publiques (G)", 10.0, 50.0, 20.0)
    ms = st.slider("Masse Monétaire (M)", 10.0, 50.0, 25.0)
    
    y = np.linspace(0, 100, 100)
    is_curve = (80 + g - y) / 2 
    lm_curve = (0.5 * y - ms + 20)
    
    fig, ax = plt.subplots()
    ax.plot(y, is_curve, label='Courbe IS', color='blue')
    ax.plot(y, lm_curve, label='Courbe LM', color='red')
    ax.set_ylim(0, 50)
    ax.set_xlabel('Revenu (Y)')
    ax.set_ylabel('Taux d’intérêt (r)')
    ax.legend()
    st.pyplot(fig)
    st.info("💡 **Analyse :** Augmenter G déplace IS à droite. Augmenter M déplace LM à droite.")

# --- SECTION CALCULATEUR ---
def section_calculateur():
    st.title("🧮 Calculateur de Déterminant")
    st.write("Matrice $2 \\times 2$")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", value=1.0)
        c = st.number_input("c", value=0.0)
    with col2:
        b = st.number_input("b", value=0.0)
        d = st.number_input("d", value=1.0)
    det = (a * d) - (b * c)
    st.latex(f"\\det(A) = {det}")
    if det == 0: st.error("Non inversible")
    else: st.success("Inversible")

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.markdown("---")
    st.title("🎮 Menu")
    choix = st.radio("Navigation", ["📖 Quiz", "📈 Simulateur IS-LM", "🧮 Calculateur Maths"])

if choix == "📖 Quiz":
    section_quiz()
elif choix == "📈 Simulateur IS-LM":
    section_simulateur()
elif choix == "🧮 Calculateur Maths":
    section_calculateur()
