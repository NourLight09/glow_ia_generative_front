"""
Module RAG pour la recherche de produits de beauté
"""
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

class ProductRetriever:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.vector_store = None
        # On utilise un modèle léger et gratuit pour transformer le texte en vecteurs
        print("Initialisation du modele d'embedding...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        print(f"Chargement et indexation des produits depuis {self.csv_path}...")
        
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Le fichier {self.csv_path} est introuvable !")

        # Chargement du CSV
        df = pd.read_csv(self.csv_path)
        
        # Création des documents pour le RAG
        documents = []
        for _, row in df.iterrows():
            # On crée un texte descriptif riche pour que l'IA comprenne bien le produit
            # On combine Type, Nom, Prix et Ingrédients
            content = f"Type: {row['product_type']}. " \
                      f"Nom: {row['product_name']}. " \
                      f"Prix: {row['price']}. " \
                      f"Ingrédients: {str(row['ingredients'])}."
            
            # On garde les infos propres dans les métadonnées pour l'affichage final
            metadata = {
                "name": row['product_name'],
                "type": row['product_type'],
                "price": row['price'],
                "url": row['product_url'] if 'product_url' in row else "",
                "ingredients": str(row['ingredients']).lower() # Stocké pour le filtrage
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
            
        # Création de la base vectorielle FAISS (le "cerveau")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print(f"Base de donnees produits prete ! ({len(documents)} produits indexes)")

    def get_relevant_products(self, query, k=3, avoid_ingredients=None):
        """
        Cherche les k produits les plus pertinents pour la requête.
        Filtre automatiquement les produits contenant des ingrédients à éviter.
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        # On récupère plus de candidats pour pouvoir filtrer après
        # Si on veut 3 produits finaux, on en cherche 10 au départ
        fetch_k = k * 4 
        results = self.vector_store.similarity_search(query, k=fetch_k)
        
        if not avoid_ingredients:
            return results[:k]
            
        filtered_results = []
        avoid_ingredients_lower = [ing.lower() for ing in avoid_ingredients]
        
        for doc in results:
            product_ingredients = doc.metadata.get("ingredients", "")
            
            # Vérifie si un ingrédient interdit est présent
            contains_bad_ingredient = False
            for bad_ing in avoid_ingredients_lower:
                if bad_ing in product_ingredients:
                    contains_bad_ingredient = True
                    break
            
            if not contains_bad_ingredient:
                filtered_results.append(doc)
                
            if len(filtered_results) >= k:
                break
                
        return filtered_results

# Petit test pour vérifier que ça marche tout seul
if __name__ == "__main__":
    # On suppose que le CSV est dans le même dossier
    try:
        retriever = ProductRetriever("skincare_products.csv")
        
        print("\nTEST DE RECHERCHE")
        query = "crème hydratante pour peau sèche et sensible pas cher"
        print(f"Recherche : '{query}'")
        
        results = retriever.get_relevant_products(query, k=3)
        
        for doc in results:
            print(f"Trouve : {doc.metadata['name']} ({doc.metadata['price']})")
            # print(f"   Détails : {doc.page_content[:100]}...")
            
    except Exception as e:
        print(f"Erreur : {e}")
