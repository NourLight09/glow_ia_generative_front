import streamlit as st
import views
import os
import joblib # Import indispensable pour charger l'IA
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="GlowAI - Votre Consultant Beauté Personnel",
    page_icon="✨",
    layout="centered"
)

# --- CHARGEMENT DE L'IA ---
@st.cache_resource # On utilise le cache pour ne charger les fichiers qu'une seule fois
def load_ml_models():
    # Assure-toi que ces fichiers sont bien dans le dossier racine
    model = joblib.load('modele_peau_xgboost.pkl')
    scaler = joblib.load('scaler_peau.pkl')
    le = joblib.load('label_encoder_peau.pkl')
    return model, scaler, le

try:
    # On stocke les modèles dans la session pour les passer aux vues
    st.session_state.model, st.session_state.scaler, st.session_state.le = load_ml_models()
except Exception as e:
    st.error("Erreur lors du chargement des modèles IA. Vérifiez que les fichiers .pkl sont présents.")

# --- CSS ET NAVIGATION ---
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/styles.css")

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Routage (on passe les modèles aux vues si nécessaire)
if st.session_state.page == 'home':
    views.show_home(navigate_to)
elif st.session_state.page == 'diagnosis':
    # On passe les outils de l'IA à la vue de diagnostic
    views.show_diagnosis(navigate_to)
elif st.session_state.page == 'magazine':
    views.show_magazine(navigate_to)