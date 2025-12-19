# Glow AI - Consultant Beauté Intelligent ✨

Glow AI est une application de recommandation de routines de soins de la peau alimentée par l'Intelligence Artificielle (Mistral AI) et enrichie par une base de données produits (RAG).

## 📂 Structure du Projet

Le projet est divisé en quatres dossiers principaux :

*   **`Glow_front_IA_generative/`** : Contient l'interface utilisateur (Frontend) réalisée avec Streamlit.
*   **`générative/`** : Contient la logique IA (Backend), le moteur RAG et la base de données produits (`skincare_products.csv`).
*   **`Glow_front_IA_predictive/`** : Contient l'interface utilisateur (Frontend) réalisée avec Streamlit qui est donc reliée à l'i prédictive.
*   **`IA_predictive/`** : Contient la logique IA (Backend), de l'IA prédictive

## 🛠️ Prérequis

*   **Python 3.8** ou supérieur.
*   Une clé API **Mistral AI**.

## 🚀 Installation

1.  **Ouvrez un terminal** dans le dossier racine du projet (`Ia_predictive`).

2.  **Installez les dépendances** nécessaires pour le frontend et le backend. Exécutez la commande suivante :

    ```bash
    pip install streamlit langchain langchain-mistralai langchain-community faiss-cpu pandas python-dotenv pydantic sentence-transformers
    ```

3.  **Configuration de la clé API** :
    *   Assurez-vous d'avoir un fichier `.env` dans le dossier `Glow_front`.
    *   Ce fichier doit contenir votre clé API sous la forme suivante :
        ```env
        MISTRAL_API_KEY=votre_clé_api_ici
        ```

## ▶️ Lancement de l'Application

L'application fonctionne comme un tout unique. Vous n'avez besoin de lancer que l'interface Streamlit, qui chargera automatiquement le module IA. **Il n'y a pas de serveur backend séparé à lancer.**

1.  Placez-vous dans le dossier du frontend :
    ```bash
    cd Glow_front
    ```

2.  Lancez l'application :
    ```bash
    python -m streamlit run app.py
    ```

3.  L'application s'ouvrira automatiquement dans votre navigateur (généralement à l'adresse `http://localhost:8501`).

## 🧩 Fonctionnement Technique

*   **Interface** : L'utilisateur remplit son profil (âge, type de peau, budget, etc.) via `views.py`.
*   **Backend** :
    *   `glow.py` initialise l'agent IA.
    *   `product_retriever.py` indexe les produits du fichier CSV (`skincare_products.csv`) au démarrage pour permettre à l'IA de recommander des produits réels (RAG).
    *   Mistral AI génère une routine complète et personnalisée au format JSON.
*   **Résultat** : L'interface affiche la routine sous forme de magazine interactif.

## ⚠️ Dépannage Courant

*   **Erreur "ModuleNotFoundError"** : Vérifiez que vous avez bien installé toutes les bibliothèques listées dans la section Installation.
*   **Erreur "MISTRAL_API_KEY non trouvée"** : Vérifiez que le fichier `.env` est bien présent dans `Glow_front` et qu'il contient une clé valide.
*   **Lenteur au premier lancement** : C'est normal, le système télécharge le modèle d'embedding pour la recherche de produits.
