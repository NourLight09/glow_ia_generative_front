import streamlit as st
import textwrap
import time
import datetime
import re
import sys
import os

# Ajout du chemin vers le module génératif
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'générative')))
from glow import get_glow_ai

# Base de données Produits Simulée (Catalogue GLOW)
MOCK_PRODUCTS = {
    "nettoyant": {
        "grasse": {"name": "Purifying Gel Cleanser", "price": "24€", "ing": "Zinc, Acide Salicylique", "desc": "Gel moussant purifiant intense."},
        "seche": {"name": "Milky Oil Cleanser", "price": "28€", "ing": "Huile d'Amande, Céramides", "desc": "Lait-huile reconfortant."},
        "normale": {"name": "Gentle Foam", "price": "22€", "ing": "Eau de Rose, Aloe Vera", "desc": "Mousse aérienne douce."},
        "sensible": {"name": "Calming Balm", "price": "30€", "ing": "Centella Asiatica, Avoine", "desc": "Baume fondant apaisant."}
    },
    "serum": {
        "eclat": {"name": "Vitamin C Radiance", "price": "45€", "ing": "Vitamine C 15%, Ferulic Acid", "desc": "Boost d'éclat immédiat."},
        "rides": {"name": "Retinol Renew", "price": "55€", "ing": "Retinol 0.3%, Peptides", "desc": "Lisse et raffermit la peau."},
        "imperfections": {"name": "Niacinamide Zinc", "price": "35€", "ing": "Niacinamide 10%, Zinc 1%", "desc": "Réduit les pores et imperfections."},
        "deshydratation": {"name": "Hyaluronic Boost", "price": "42€", "ing": "Acide Hyaluronique Multi-PM", "desc": "Hydratation profonde par couches."}
    },
    "creme": {
        "riche": {"name": "Deep Repair Cream", "price": "48€", "ing": "Beurre de Karité, Squalane", "desc": "Nutrition intense nuit."},
        "legere": {"name": "Hydro-Gel Cloud", "price": "38€", "ing": "Eau de Glacier, Concombre", "desc": "Gelée hydratante fini mat."},
        "active": {"name": "Pro-Collagen Cream", "price": "65€", "ing": "Collagène Marin, Algues", "desc": "Fermeté et rebond."}
    }
}

def show_home(navigate_callback):
    st.markdown("<h1 style='text-align: center; font-size: 6rem; font-family: Playfair Display, serif; margin-top: 50px;'>GLOW</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 50px;'>VOTRE CONSULTANT BEAUTÉ INTELLIGENT</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("LANCER LE DIAGNOSTIC"):
            navigate_callback('diagnosis')

def derive_skin_profile(data):
    # Logique simple pour déterminer le type de peau pour l'affichage
    oil = data.get('oil', 5)
    hydration = data.get('hydration', 5)
    sens = data.get('sensitivity', 3)
    
    skin_type = "NORMALE"
    concern = "ÉCLAT"
    
    if sens > 6:
        skin_type = "SENSIBLE"
        concern = "APAISANTE"
    elif oil > 7:
        skin_type = "GRASSE"
        concern = "MATIFIANT"
    elif oil < 3:
        skin_type = "SÈCHE"
        concern = "NUTRITION"
    elif oil > 6 and hydration < 4:
        skin_type = "MIXTE DÉSHYDRATÉE"
        concern = "RÉÉQUILIBRANTE"
    elif hydration < 3:
        skin_type = "DÉSHYDRATÉE"
        concern = "HYDRATATION INTENSE"
        
    return skin_type, concern

def get_product_selection(skin_type, concern):
    # Logique de sélection simple
    # 1. Nettoyant selon Type de Peau
    if "GRASSE" in skin_type: cle_type = "grasse"
    elif "SÈCHE" in skin_type or "DÉSHYDRATÉE" in skin_type: cle_type = "seche"
    elif "SENSIBLE" in skin_type: cle_type = "sensible"
    else: cle_type = "normale"
    
    # 2. Sérum selon Préoccupation
    if "RIDE" in concern.upper(): ser_type = "rides"
    elif "ACNÉ" in concern.upper() or "MATIFIANT" in concern.upper(): ser_type = "imperfections"
    elif "DÉSHYDRATÉE" in skin_type: ser_type = "deshydratation"
    else: ser_type = "eclat" # Default
    
    # 3. Crème selon Type
    if "SÈCHE" in skin_type: cre_type = "riche"
    elif "GRASSE" in skin_type: cre_type = "legere"
    else: cre_type = "active"
    
    return [
        MOCK_PRODUCTS["nettoyant"].get(cle_type, MOCK_PRODUCTS["nettoyant"]["normale"]),
        MOCK_PRODUCTS["serum"].get(ser_type, MOCK_PRODUCTS["serum"]["eclat"]),
        MOCK_PRODUCTS["creme"].get(cre_type, MOCK_PRODUCTS["creme"]["active"])
    ]

def show_diagnosis(navigate_callback):
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Diagnostiquez votre Peau</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    diagnosis_html = textwrap.dedent("""
    <div style='background-color: #ffdce5; padding: 20px; border-radius: 5px; margin-bottom: 30px; border-left: 3px solid #5e1223; color: #5e1223;'>
        <p style='margin:0; font-style:italic; color: #5e1223;'>Pour établir votre profil dermo-cosmétique précis, veuillez renseigner vos indicateurs biologiques. Nos algorithmes calculeront votre typologie exacte.</p>
    </div>
    """)
    st.markdown(diagnosis_html.strip(), unsafe_allow_html=True)
    
    with st.form("diagnosis_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Prénom")
            age = st.number_input("Âge", min_value=16, max_value=90, value=25)
        with c2:
            gender = st.selectbox("Genre", ["Femme", "Homme", "Autre"])
            skin_type_input = st.selectbox("Type de Peau (Skin_Type)", ["Normale", "Sèche", "Grasse", "Mixte"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Design "Carte Technologique" pour les données biométriques
        st.markdown("""
        <div style="background-color: #fffbf9; padding: 20px; border-radius: 15px; border: 1px solid #ffdce5; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 25px;">
            <h3 style='text-align: center; color: #5e1223; margin-top: 0; font-size: 1.4rem; font-family: "Playfair Display", serif;'>🧬 ANALYSE BIOMÉTRIQUE & ENVIRONNEMENT</h3>
            <p style='text-align: center; font-size: 0.9rem; color: #888; font-style: italic; margin-bottom: 0;'>
                Simulation des capteurs cutanés et données météo en temps réel
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_bio1, col_bio2 = st.columns(2)
        with col_bio1:
            st.markdown("<h4 style='color: #5e1223; border-bottom: 1px solid #ffdce5; padding-bottom: 5px;'>🔍 Analyse de Peau</h4>", unsafe_allow_html=True)
            hydration_level = st.slider("💧 Hydratation (%)", 0, 100, 50, help="Niveau d'eau dans l'épiderme")
            oil_level = st.slider("✨ Sébum (Oil)", 0, 100, 50, help="Production de sébum")
            sensitivity = st.slider("🛡️ Sensibilité (0-5)", 0, 5, 2, help="Réactivité de la peau")
            
        with col_bio2:
            st.markdown("<h4 style='color: #5e1223; border-bottom: 1px solid #ffdce5; padding-bottom: 5px;'>🌍 Environnement</h4>", unsafe_allow_html=True)
            temperature = st.number_input("🌡️ Température (°C)", value=25, help="Température locale")
            humidity = st.slider("☁️ Humidité (%)", 0, 100, 60, help="Taux d'humidité de l'air")

        st.markdown("<br>", unsafe_allow_html=True)

        # Budget plus clair
        budget = st.number_input(
            "Votre Budget Global (€)", 
            min_value=20, 
            max_value=500, 
            value=50,
            step=5,
            help="Indiquez le montant total approximatif pour la routine complète."
        )
        st.caption("L'IA optimisera la routine pour respecter ce montant.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Ajout des allergies et objectifs
        st.markdown("<h3 style='text-align: center; color: #5e1223;'>Personnalisation Avancée</h3>", unsafe_allow_html=True)
        
        goals = st.multiselect(
            "Vos Objectifs Prioritaires",
            ["Anti-âge", "Éclat", "Anti-imperfections", "Hydratation", "Apaisement", "Resserrer les pores"],
            default=["Éclat"]
        )
        
        allergies = st.text_input(
            "Allergies ou Ingrédients à éviter (optionnel)",
            placeholder="Ex: Parfum, Alcool, Huiles essentielles..."
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("GÉNÉRER MON ÉDITION SPÉCIALE")
        
        if submitted:
            if name:
                # Sauvegarde des données
                st.session_state.user_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'skin_type_input': skin_type_input,
                    'sensitivity': sensitivity,
                    'budget': f"{budget}€",
                    'goals': goals,
                    'allergies': allergies
                }
                
                with st.spinner('L\'IA générative analyse votre profil et cherche les meilleurs produits...'):
                    # Mapping direct pour l'IA
                    # Traduction Français -> Anglais pour le backend
                    type_map = {
                        "Normale": "Normal",
                        "Sèche": "Dry",
                        "Grasse": "Oily",
                        "Mixte": "Combination"
                    }
                    skin_map = type_map.get(skin_type_input, "Normal")
                    
                    # Mapping des nouvelles données biométriques
                    sens_map = "Low"
                    if sensitivity >= 4: sens_map = "High"
                    elif sensitivity >= 2: sens_map = "Medium"
                    
                    hydra_map = "Medium"
                    if hydration_level < 30: hydra_map = "Low"
                    elif hydration_level > 70: hydra_map = "High"

                    # Formatage intelligent du budget pour le RAG
                    budget_str = f"{budget}€"
                    if budget < 45:
                        budget_str += " (Budget Faible)"
                        
                    # Traitement des allergies (séparation par virgule)
                    avoid_list = [x.strip() for x in allergies.split(',')] if allergies else []
                    
                    # Construction du contexte environnemental pour le prompt
                    env_context = f"Vivant dans un environnement à {temperature}°C avec {humidity}% d'humidité."
                    
                    profil_ai = {
                        "skin_type": skin_map,
                        "hydration_level": hydra_map,
                        "sensitivity": sens_map,
                        "goals": ", ".join(goals) + f". {env_context}",
                        "budget": budget_str,
                        "avoid_ingredients": avoid_list,
                        "age": age
                    }
                    
                    try:
                        advisor = get_glow_ai()
                        routines = advisor.generate_full_routine(profil_ai)
                        st.session_state.user_data['routines'] = routines
                        navigate_callback('magazine')
                    except Exception as e:
                        st.error(f"Erreur IA : {e}")
            else:
                st.error("Merci d'indiquer votre prénom pour la couverture du magazine.")

def show_magazine(navigate_callback):
    user = st.session_state.user_data
    name = user.get('name', 'Chère Lectrice')
    age = user.get('age', 25)
    
    # LOGIQUE IA GÉNÉRATIVE
    if 'routines' in user:
        routines = user['routines']
        # On récupère les infos de la routine Matin comme référence
        r_matin = routines.get('morning')
        r_soir = routines.get('evening')
        
        skin_type = r_matin.target_skin_type.upper() if r_matin else "SUR-MESURE"
        concern = "ÉQUILIBRE & ÉCLAT" # Générique ou extrait de global_advice
        
        products = []
        
        # Sélection intelligente de 3 produits pour l'affichage Magazine
        # 1. Le Nettoyant (Matin Etape 1)
        if r_matin and r_matin.steps:
            p = r_matin.steps[0].products[0]
            products.append({"name": p.name, "price": p.price_estimation, "ing": p.brand, "desc": p.description})
            
        # 2. Le Traitement (Soir Etape 2 ou Matin Etape 2)
        if r_soir and len(r_soir.steps) > 1:
            p = r_soir.steps[1].products[0]
            products.append({"name": p.name, "price": p.price_estimation, "ing": p.brand, "desc": p.description})
        elif r_matin and len(r_matin.steps) > 1:
            p = r_matin.steps[1].products[0]
            products.append({"name": p.name, "price": p.price_estimation, "ing": p.brand, "desc": p.description})
            
        # 3. La Crème de Nuit (Soir Dernière étape)
        if r_soir and r_soir.steps:
            p = r_soir.steps[-1].products[0]
            products.append({"name": p.name, "price": p.price_estimation, "ing": p.brand, "desc": p.description})
            
        # Comblage si manque de produits
        while len(products) < 3:
            products.append({"name": "Soin Complémentaire", "price": "--", "ing": "Glow Lab", "desc": "Produit essentiel à votre routine."})
            
    else:
        # Fallback Mock (Ancien système)
        skin_type, concern = derive_skin_profile(user)
        products = get_product_selection(skin_type, concern)
    
    today = datetime.date.today().strftime("%B %Y")
    
    # Injection HTML pour la mise en page Magazine
    magazine_html = f"""
    <div class="magazine-container">
        <!-- EN-TÊTE COUVERTURE -->
        <div class="cover-header">
            <h1 class="brand-title">GLOW</h1>
            <div class="issue-details">
                <span>ÉDITION SPÉCIALE &bull; {age} ANS</span>
                <span>{today}</span>
                <span>VOL. 1</span>
            </div>
        </div>
        
        <!-- IMAGE HÉRO -->
        <div class="cover-hero">
            <img src="https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=1000&auto=format&fit=crop">
        </div>
        
        <!-- GROS TITRES -->
        <div class="headline-overlay">
            <div class="sub-headline">L'INTELLIGENCE ARTIFICIELLE RÉVÈLE</div>
            <div class="main-headline">VOTRE ROUTINE IDEALE<br>POUR PEAU {skin_type}</div>
            <div style="width: 50px; height: 1px; background: #5e1223; margin: 20px auto;"></div>
            <p style="font-style: italic;">Objectif : {concern}</p>
        </div>
        
        <!-- ÉDITO -->
        <div class="editorial-section">
            <h2 style="text-align: center; margin-bottom: 30px; font-size: 2rem;">LE MOT DE L'EXPERT</h2>
            <div class="editorial-layout">
                <p><span class="drop-cap">B</span>onjour {name},</p>
                <p>À {age} ans, votre peau a des besoins précis. Notre analyse montre que vous avez une peau <strong>{skin_type.lower()}</strong>.</p>
                <p>Ce que cela signifie : votre peau a besoin d'aide pour gérer son équilibre. Votre priorité est de traiter <strong>{concern.lower()}</strong>.</p>
                <p>Nous avons sélectionné pour vous 3 produits d'exception. Voici votre routine détaillée.</p>
                <p style="text-align: right; margin-top: 20px; font-weight: bold;">— Votre Coach Beauté</p>
            </div>
        </div>
        
        <!-- TIMELINE ROUTINE (NOUVEAU DESIGN) -->
        <div class="timeline-section">
            <h2 style="text-align:center; color: #5e1223; margin-bottom: 50px;">VOTRE AGENDA BEAUTÉ</h2>
            
            <div class="timeline-item">
                <div class="timeline-time">08:00</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">Le Réveil Éclat</h3>
                    <p>Nettoyez votre visage avec <strong>{products[0]['name']}</strong> pour éliminer les impuretés de la nuit. Une base saine est essentielle.</p>
                </div>
            </div>
            
            <div class="timeline-item">
                <div class="timeline-time">08:15</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">L'Hydratation</h3>
                    <p>Appliquez le sérum <strong>{products[1]['name']}</strong> puis scellez l'hydratation. N'oubliez pas votre SPF !</p>
                </div>
            </div>
            
            <div class="timeline-item">
                <div class="timeline-time">22:00</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">Le Soir Régénérant</h3>
                    <p>Le moment clé. Utilisez <strong>{products[2]['name']}</strong> pour réparer votre peau durant le sommeil.</p>
                </div>
            </div>
        </div>

        <!-- SÉLECTION PRODUITS DÉTAILLÉE -->
        <div class="product-grid">
            <div style="grid-column: 1 / -1; text-align: center; margin-bottom: 20px;">
                <h2>VOTRE SÉLECTION PERSONNALISÉE</h2>
                <p>LES PRODUITS DE VOTRE ROUTINE</p>
            </div>
            
            <!-- PRODUIT 1 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400">
                <div class="product-name">{products[0]['name']}</div>
                <div class="product-price">{products[0]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[0]['ing']}</div>
                <div class="product-desc">{products[0]['desc']}</div>
            </div>

            <!-- PRODUIT 2 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?w=400">
                <div class="product-name">{products[1]['name']}</div>
                <div class="product-price">{products[1]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[1]['ing']}</div>
                <div class="product-desc">{products[1]['desc']}</div>
            </div>

            <!-- PRODUIT 3 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=400">
                <div class="product-name">{products[2]['name']}</div>
                <div class="product-price">{products[2]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[2]['ing']}</div>
                <div class="product-desc">{products[2]['desc']}</div>
            </div>
            
        </div>
        
    </div>
    """
    
    # Nettoyage de l'indentation pour éviter les conflits Markdown
    magazine_html = re.sub(r'^\s+', '', magazine_html, flags=re.MULTILINE)
    st.markdown(magazine_html, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Création d'un fichier HTML autonome pour le téléchargement
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Glow Magazine - {name}</title>
            <style>
                body {{ font-family: 'Helvetica', sans-serif; color: #1a1a1a; padding: 40px; background-color: #fffbf9; }}
                .magazine-container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                h1, h2, h3 {{ color: #5e1223; font-family: serif; }}
                .product-card {{ border: 1px solid #eee; padding: 20px; margin-bottom: 20px; border-radius: 8px; text-align: center; }}
                img {{ max-width: 100%; height: auto; border-radius: 4px; margin-bottom: 15px; }}
                .product-name {{ font-weight: bold; font-size: 1.2em; margin-bottom: 5px; }}
                .product-price {{ color: #5e1223; font-weight: bold; margin-bottom: 5px; }}
                .timeline-item {{ border-left: 2px solid #5e1223; padding-left: 20px; margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            {magazine_html}
        </body>
        </html>
        """
        
        st.download_button(
            label="TÉLÉCHARGER (VERSION WEB)",
            data=full_html,
            file_name=f"Glow_Magazine_{name}.html",
            mime="text/html"
        )
        
    with col2:
        if st.button("NOUVEAU DIAGNOSTIC"):
            # Réinitialisation complète pour un nouveau parcours
            if 'user_data' in st.session_state:
                st.session_state.user_data = {}
            navigate_callback('home')
