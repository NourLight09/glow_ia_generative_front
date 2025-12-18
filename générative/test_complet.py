"""Test complet du Glow AI"""

from glow import get_glow_ai

print("GLOW AI - Test Complet")

# Créer le profil beauté (simulant la sortie du diagnostic prédictif)
profil_utilisateur = {
    "skin_type": "Combination",              # Du diagnostic prédictif
    "hydration_level": "Medium",             # Du diagnostic prédictif
    "sensitivity": "Low",                    # Du diagnostic prédictif
    "avoid_ingredients": ["parabens", "sulfates"],

    "goals": "Équilibre et éclat",

    "budget": "Moyen (20-40€ par produit)"
}

print("\nPROFIL BEAUTE:")
for key, value in profil_utilisateur.items():
    print(f"   - {key}: {value}")

print("\n")

# Initialiser le conseiller beauté
advisor = get_glow_ai()

print("\n")

# Générer la routine complète
print("Génération de votre routine personnalisée...\n")

try:
    routines = advisor.generate_full_routine(profil_utilisateur)
    
    # Dictionnaire de traduction pour l'affichage
    noms_routines = {
        "morning": "MATIN",
        "evening": "SOIR",
        "weekly": "HEBDOMADAIRE"
    }

    # Affichage des routines formatées
    for routine_key, routine_obj in routines.items():
        if routine_obj:
            titre_francais = noms_routines.get(routine_key, routine_key.upper())
            print(f"\nROUTINE {titre_francais}")
            print(f"Type Peau Cible: {routine_obj.target_skin_type}")
            print(f"Budget Estimé: {routine_obj.total_estimated_budget}")
            print(f"Conseil Global: {routine_obj.global_advice}\n")
            
            for i, step in enumerate(routine_obj.steps, 1):
                product_names = ", ".join([f"{p.name} ({p.brand} - {p.price_estimation})" for p in step.products])
                print(f"  {i}. {step.step_name}: {product_names}")
                print(f"     Conseil: {step.usage_tips}")

    print("\n")
    print("SUCCES! Toutes les routines ont ete generees (Format Structure)!")
    print("\n")
    
    # Sauvegarder dans un fichier JSON (plus adapté maintenant)
    import json
    
    # Conversion des objets Pydantic en dictionnaires
    routines_dict = {
        k: v.model_dump() if v else None 
        for k, v in routines.items()
    }
    
    with open("ma_routine_beaute.json", "w", encoding="utf-8") as f:
        json.dump(routines_dict, f, ensure_ascii=False, indent=4)
    
    print("\nRoutine sauvegardée dans: ma_routine_beaute.json")
    
except Exception as e:
    print(f"\nErreur: {e}")
    import traceback
    traceback.print_exc()
    print("\nVérifiez votre configuration Mistral")
