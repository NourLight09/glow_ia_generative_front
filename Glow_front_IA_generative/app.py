import streamlit as st
import views
import os

# Configuration de la page
st.set_page_config(
    page_title="GlowAI - Votre Consultant Beauté Personnel",
    page_icon="✨",
    layout="centered"
)

# Chargement du CSS personnalisé
def load_css(file_name):
    # Vérification du chemin
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback ou message d'erreur (optionnel)
        pass

load_css("assets/styles.css")

# Gestion de l'état de session (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Navigation
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Routage
if st.session_state.page == 'home':
    views.show_home(navigate_to)
elif st.session_state.page == 'diagnosis':
    views.show_diagnosis(navigate_to)
elif st.session_state.page == 'magazine':
    views.show_magazine(navigate_to)
