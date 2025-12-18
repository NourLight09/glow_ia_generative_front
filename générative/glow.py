"""Module IA Générative - Glow avec LangChain, Mistral AI et RAG"""

import os
from dotenv import load_dotenv
from typing import Dict, Any, List
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from product_retriever import ProductRetriever  # Import du module RAG

# Charger configuration
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

if not api_key:
    raise ValueError("MISTRAL_API_KEY non trouvée dans .env")

# --- DÉFINITION DES SCHÉMAS (LES MOULES) ---

class SkincareProduct(BaseModel):
    """Représente un produit de soin recommandé."""
    name: str = Field(description="Nom complet du produit")
    brand: str = Field(description="Marque du produit")
    description: str = Field(description="Courte explication de pourquoi ce produit est choisi (bénéfices)")
    price_estimation: str = Field(description="Prix estimé (ex: '15€')")

class RoutineStep(BaseModel):
    """Une étape de la routine beauté."""
    step_name: str = Field(description="Nom de l'étape (ex: 'Nettoyage', 'Sérum')")
    products: List[SkincareProduct] = Field(description="Liste des produits recommandés pour cette étape")
    usage_tips: str = Field(description="Conseils d'application spécifiques pour cette étape")

class SkincareRoutine(BaseModel):
    """La routine beauté complète générée."""
    routine_type: str = Field(description="Type de routine (Matin, Soir, ou Hebdomadaire)")
    target_skin_type: str = Field(description="Type de peau ciblé")
    steps: List[RoutineStep] = Field(description="Liste ordonnée des étapes de la routine")
    global_advice: str = Field(description="Conseil général pour cette routine")
    total_estimated_budget: str = Field(description="Estimation du budget total pour la routine")


class GlowAI:
    """Génère des routines beauté personnalisées et STRUCTURÉES avec LangChain et Mistral"""
    
    def __init__(self, model_name='mistral-large-latest'):
        """Initialise le modèle Mistral via LangChain et le RAG"""
        self.llm = ChatMistralAI(
            model=model_name,
            mistral_api_key=api_key,
            temperature=0  # Température basse pour être rigoureux sur le format JSON
        )
        
        # Initialisation du RAG (Recherche de produits)
        try:
            print("Initialisation du moteur de recherche de produits (RAG)...")
            # Chemin absolu vers le CSV (même dossier que ce script)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, "skincare_products.csv")
            
            self.retriever = ProductRetriever(csv_path)
            print("RAG prêt !")
        except Exception as e:
            print(f"Attention: Impossible d'initialiser le RAG ({e}). L'IA utilisera ses connaissances générales.")
            self.retriever = None

        print(f"Glow AI initialisé avec {model_name} (LangChain + sorties structurées + RAG)")
    
    def _get_rag_context(self, skin_profile: Dict[str, Any], routine_type: str) -> str:
        """Cherche des produits pertinents dans le CSV pour enrichir le prompt"""
        if not self.retriever:
            return ""
            
        # On construit une requête de recherche basée sur le profil
        query = f"produits {routine_type} pour peau {skin_profile.get('skin_type')} " \
                f"hydratation {skin_profile.get('hydration_level')} " \
                f"sensibilité {skin_profile.get('sensitivity')}"
        
        # Si budget faible, on ajoute "pas cher" à la recherche
        if "faible" in str(skin_profile.get('budget', '')).lower():
            query += " pas cher abordable"
            
        print(f"Recherche RAG ({routine_type}): '{query}'")
        
        # Récupération des ingrédients à éviter
        avoid_list = skin_profile.get('avoid_ingredients', [])
        
        results = self.retriever.get_relevant_products(query, k=5, avoid_ingredients=avoid_list)
        
        context_text = "\nVOICI DES PRODUITS DISPONIBLES DANS NOTRE STOCK (Utilise-les en priorité !) :\n"
        for doc in results:
            context_text += f"- {doc.metadata['name']} ({doc.metadata['type']}) - Prix: {doc.metadata['price']}\n"
            
        return context_text

    def _generate_structured(self, prompt_text: str, schema) -> Any:
        """Méthode interne pour appeler l'API Mistral avec une sortie structurée (JSON)"""
        try:
            # On crée une chaîne qui force la sortie structurée selon le schéma donné
            prompt = ChatPromptTemplate.from_template("{input}")
            structured_llm = self.llm.with_structured_output(schema)
            chain = prompt | structured_llm
            
            response_object = chain.invoke({"input": prompt_text})
            return response_object
        except Exception as e:
            print(f"Erreur lors de la génération structurée : {str(e)}")
            return None

    def generate_morning_routine(self, skin_profile: Dict[str, Any]) -> SkincareRoutine:
        """Génère une routine du matin structurée"""
        
        # 1. Récupération du contexte RAG
        rag_context = self._get_rag_context(skin_profile, "matin nettoyant crème solaire")
        
        # 2. Construction du prompt enrichi
        prompt = f"""Tu es un expert en soins de la peau.
Génère une routine du MATIN complète et structurée pour ce profil :
- Type de peau: {skin_profile.get('skin_type', 'Normal')}
- Hydratation: {skin_profile.get('hydration_level', 'Medium')}
- Sensibilité: {skin_profile.get('sensitivity', 'Low')}
- Budget: {skin_profile.get('budget', 'Moyen')}
- Ingrédients à éviter: {', '.join(skin_profile.get('avoid_ingredients', []))}
- Objectifs: {skin_profile.get('goals', 'Soin quotidien')}

{rag_context}

INSTRUCTIONS :
1. Utilise EN PRIORITÉ les produits du stock listés ci-dessus s'ils sont adaptés.
2. Respecte strictement le budget.
3. Détaille chaque étape (Nettoyage, Sérum, Hydratation, SPF).
"""
        return self._generate_structured(prompt, SkincareRoutine)
    
    def generate_evening_routine(self, skin_profile: Dict[str, Any]) -> SkincareRoutine:
        """Génère une routine du soir structurée"""
        
        # 1. Récupération du contexte RAG
        rag_context = self._get_rag_context(skin_profile, "soir démaquillant nettoyant crème nuit")
        
        prompt = f"""Tu es un expert en soins de la peau.
Génère une routine du SOIR complète et structurée pour ce profil :
- Type de peau: {skin_profile.get('skin_type', 'Normal')}
- Hydratation: {skin_profile.get('hydration_level', 'Medium')}
- Sensibilité: {skin_profile.get('sensitivity', 'Low')}
- Budget: {skin_profile.get('budget', 'Moyen')}
- Ingrédients à éviter: {', '.join(skin_profile.get('avoid_ingredients', []))}

{rag_context}

INSTRUCTIONS :
1. Utilise EN PRIORITÉ les produits du stock listés ci-dessus.
2. Focus sur le nettoyage et la réparation.
3. Respecte le budget.
"""
        return self._generate_structured(prompt, SkincareRoutine)
    
    def generate_weekly_treatments(self, skin_profile: Dict[str, Any]) -> SkincareRoutine:
        """Génère des soins hebdomadaires structurés"""
        
        # 1. Récupération du contexte RAG
        rag_context = self._get_rag_context(skin_profile, "masque gommage traitement")
        
        prompt = f"""Tu es un expert en soins de la peau.
Génère une routine HEBDOMADAIRE (Weekly) complète et structurée pour ce profil :
- Type de peau: {skin_profile.get('skin_type', 'Normal')}
- Budget: {skin_profile.get('budget', 'Moyen')}

{rag_context}

Propose 2 ou 3 étapes de soins ponctuels (Masque, Gommage...) à faire 1-2 fois par semaine.
Privilégie les produits du stock.
"""
        return self._generate_structured(prompt, SkincareRoutine)
    
    def generate_full_routine(self, skin_profile: Dict[str, Any]) -> Dict[str, SkincareRoutine]:
        """Génère toutes les routines (objets structurés)"""
        
        print("Génération routine matin (JSON + RAG)...")
        morning = self.generate_morning_routine(skin_profile)
        
        print("Génération routine soir (JSON + RAG)...")
        evening = self.generate_evening_routine(skin_profile)
        
        print("Génération soins hebdomadaires (JSON + RAG)...")
        weekly = self.generate_weekly_treatments(skin_profile)
        
        return {
            "morning": morning,
            "evening": evening,
            "weekly": weekly
        }


def get_glow_ai(model_name='mistral-large-latest') -> GlowAI:
    """Factory function pour créer une instance de GlowAI"""
    return GlowAI(model_name)
