# Glow AI – Consultant Beauté Intelligent ✨

Glow AI est une application de recommandation de routines de soins de la peau basée sur deux approches complémentaires d’Intelligence Artificielle :

* **IA générative** : génération de routines personnalisées à l’aide de Mistral AI et d’un système RAG (produits réels).
* **IA prédictive** : prédiction et analyse via des modèles de machine learning classiques.

Les deux parties sont indépendantes mais partagent une interface commune basée sur Streamlit.

---

## Structure du Projet

Le projet est organisé en **quatre dossiers principaux**, séparant clairement les deux types d’IA :

### IA Générative

* **`Glow_front_IA_generative/`**
  Interface utilisateur (Frontend) réalisée avec Streamlit.

* **`generative/`**
  Backend de l’IA générative :

  * moteur RAG
  * logique IA
  * base de données produits (`skincare_products.csv`)

### 📊 IA Prédictive

* **`Glow_front_IA_predictive/`**
  Interface utilisateur (Frontend) réalisée avec Streamlit.

* **`IA_predictive/`**
  Backend de l’IA prédictive (modèles de machine learning, prédictions, traitements).

---

##  Prérequis

* **Python 3.8 ou supérieur**
* **Une clé API Mistral AI** (uniquement pour l’IA générative)

---

## Installation

###  Installation – IA Générative

1. Ouvrez un terminal à la racine du projet.

2. Installez les dépendances :

```bash
pip install streamlit langchain langchain-mistralai langchain-community faiss-cpu pandas python-dotenv pydantic sentence-transformers
```

3. Configuration de la clé API :

* Créez un fichier `.env` dans le dossier `Glow_front_IA_generative`
* Ajoutez :

```env
MISTRAL_API_KEY=votre_cle_api_ici
```

---

### Installation – IA Prédictive (Linux)

Sur Linux, il est obligatoire de créer un environnement virtuel Python.

1. Placez-vous dans le dossier :

```bash
cd Glow_front_IA_predictive
```

2. Créez l’environnement virtuel :

```bash
python3 -m venv venv
```

3. Activez-le :

```bash
source venv/bin/activate
```

4. Installez les dépendances :

```bash
pip install streamlit xgboost pandas joblib scikit-learn
```

---

## Lancement des Applications

### Lancer l’IA Générative

```bash
cd Glow_front_IA_generative
streamlit run app.py
```

Application accessible sur :

```
http://localhost:8501
```

---

### Lancer l’IA Prédictive

```bash
source venv/bin/activate
cd Glow_front_IA_predictive
streamlit run app.py
```

---

## 🧩 Fonctionnement Technique

### IA Générative

* L’utilisateur renseigne son profil (âge, type de peau, budget, etc.)
* Le moteur RAG indexe les produits depuis `skincare_products.csv`
* Mistral AI génère une routine personnalisée au format structuré (JSON)
* Le résultat est affiché via une interface Streamlit interactive

### IA Prédictive

* Les données utilisateur sont analysées par des modèles de machine learning
* Les prédictions utilisent `scikit-learn` et `xgboost`
* Les résultats sont affichés directement dans Streamlit

---

## ⚠️ Dépannage Courant

* **ModuleNotFoundError**
  → Dépendances non installées ou mauvais environnement activé

* **MISTRAL_API_KEY non trouvée**
  → Vérifier le fichier `.env` et son emplacement

* **Lenteur au premier lancement (IA générative)**
  → Téléchargement initial des modèles d’embedding

* **Commande `streamlit` introuvable**
  → Vérifier que l’environnement virtuel est bien activé
