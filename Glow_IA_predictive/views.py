import streamlit as st
import time
import datetime
import pandas as pd
import joblib
import inspect

# ==========================================
# 1. LOGIQUE IA PRÉDICTIVE (XGBOOST)
# ==========================================
def get_skin_type_from_ai(data):
    try:
        model = st.session_state.model
        scaler = st.session_state.scaler
        le = st.session_state.le

        gender_map = {"Femme": 0, "Homme": 1, "Autre": 2}
        
        def map_level(val):
            if val <= 3: return 0
            if val <= 7: return 1
            return 2

        cols = ['Age', 'Hydration_Level', 'Oil_Level', 'Sensitivity', 'Humidity', 'Temperature', 'Gender_encoded']
        input_df = pd.DataFrame([[
            data['age'],
            map_level(data['hydration']),
            map_level(data['oil']),
            map_level(data['sensitivity']),
            data.get('env_hum', 50.0),
            data.get('env_temp', 22.0),
            gender_map.get(data['gender'], 0)
        ]], columns=cols)

        input_scaled = scaler.transform(input_df)
        pred_code = model.predict(input_scaled)[0]
        proba = model.predict_proba(input_scaled)[0][pred_code]
        skin_type = le.inverse_transform([pred_code])[0]
        
        return skin_type.upper(), proba
    except Exception as e:
        st.error(f"Erreur IA : {e}")
        return "NORMAL", 0.0

# ==========================================
# 2. VUES DE L'INTERFACE
# ==========================================

def show_home(navigate_callback):
    st.markdown("<h1 style='text-align: center; font-size: 6rem; font-family: serif; margin-top: 50px;'>GLOW</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 50px;'>VOTRE CONSULTANT BEAUTÉ INTELLIGENT</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("LANCER LE DIAGNOSTIC", use_container_width=True):
            navigate_callback('diagnosis')

def show_diagnosis(navigate_callback):
    st.markdown("<h2 style='text-align: center;'>Diagnostic Biologique</h2>", unsafe_allow_html=True)
    
    with st.form("diagnosis_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Prénom")
            age = st.number_input("Âge", min_value=16, max_value=90, value=25)
        with c2:
            gender = st.selectbox("Genre", ["Femme", "Homme", "Autre"])
            
        st.write("---")
        st.subheader("Analyse des caractéristiques")
        hydration = st.slider("Niveau d'Hydratation", 0, 10, 5)
        oil_level = st.slider("Niveau de Sébum (Gras)", 0, 10, 5)
        sensitivity = st.slider("Niveau de Sensibilité", 0, 10, 3)

        st.subheader("Conditions Environnementales")
        env_hum = st.number_input("Humidité ambiante (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        env_temp = st.number_input("Température extérieure (°C)", min_value=-10.0, max_value=45.0, value=20.0, step=0.1)
        
        submitted = st.form_submit_button("ANALYSER MON PROFIL")
        
        if submitted:
            if name:
                st.session_state.user_data = {
                    'name': name, 'age': age, 'gender': gender,
                    'hydration': hydration, 'oil': oil_level, 
                    'sensitivity': sensitivity, 'env_hum': env_hum, 'env_temp': env_temp
                }
                with st.spinner('L\'IA analyse vos données...'):
                    skin_type, confidence = get_skin_type_from_ai(st.session_state.user_data)
                    st.session_state.user_data['skin_type'] = skin_type
                    st.session_state.user_data['confidence'] = confidence
                    time.sleep(1.0)
                    navigate_callback('magazine')
            else:
                st.error("Veuillez renseigner votre prénom.")

def show_magazine(navigate_callback):
    user = st.session_state.user_data
    skin_type = user.get('skin_type', 'NORMALE')
    confidence = user.get('confidence', 0.0)
    
    dic_fr = {"DRY": "SÈCHE", "OILY": "GRASSE", "NORMAL": "NORMALE", "COMBINATION": "MIXTE"}
    skin_fr = dic_fr.get(skin_type, skin_type)
    
    html_content = inspect.cleandoc(f"""
        <div style="border: 1px solid #5e1223; padding: 40px; border-radius: 5px; text-align: center; font-family: serif; background-color: white;">
            <h1 style="font-size: 5rem; color: #5e1223; margin: 0;">GLOW</h1>
            <p style="letter-spacing: 3px; color: #888; margin-bottom: 40px;">ÉDITION IA • DÉCEMBRE 2025</p>
            <div style="margin: 40px 0;">
                <img src="https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=800" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 2px;">
            </div>
            <div style="background-color: #fdf2f4; padding: 20px; border-radius: 5px;">
                <h3 style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; color: #5e1223; margin: 0;">Résultat du diagnostic</h3>
                <h2 style="font-size: 3.5rem; margin: 10px 0; color: #5e1223;">TYPE DE PEAU : {skin_fr}</h2>
                <div style="width: 50px; height: 1px; background-color: #5e1223; margin: 15px auto;"></div>
                <p style="font-style: italic; color: #666; margin: 0;">Les réponses générées par l’IA peuvent contenir des erreurs et ne constituent pas une information fiable à 100 %.</p>
            </div>
        </div>
    """)

    st.markdown(html_content, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("REFAIRE UNE ANALYSE"):
        navigate_callback('home')