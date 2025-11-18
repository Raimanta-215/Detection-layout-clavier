from utils.correlation import correlation_normalisee_numpy


# detetction_lettre_v2.py (Classifieur/Correlation Manuelle)

def classifieur_par_correlation(image_a_analyser_path, chemins_gabarits_dict):
    """
    Classifieur qui itère sur la structure de gabarits (dictionnaire de listes) 
    pour comparer l'image à chaque modèle.
    """
    meilleur_score = -1.0
    caractere_identifie = "INCONNU"

    # --- ÉTAPE 1: DOUBLE BOUCLE (Correction du passage d'argument) ---
    
    # Boucle 1: Itère sur les classes ('A', 'Q', etc.)
    for classe, liste_chemins in chemins_gabarits_dict.items():
        
        # Boucle 2: Itère sur CHAQUE chemin de gabarit dans la liste
        # C'est ici que l'on extrait le STRING du chemin
        for chemin_gabarit_unique in liste_chemins:
            
            # 💡 APPEL CORRIGÉ : On passe deux strings à la fonction de calcul
            score = correlation_normalisee_numpy(image_a_analyser_path, chemin_gabarit_unique)
            
            # --- ÉTAPE 2: MISE À JOUR DU MEILLEUR SCORE ---
            if score > meilleur_score:
                meilleur_score = score
                caractere_identifie = classe
                
    # --- ÉTAPE 3: DÉCISION FINALE (Classification) ---
    SEUIL_DE_CONFIANCE = 0.85 
    
    if meilleur_score >= SEUIL_DE_CONFIANCE:
        print(f"✅ Identification réussie : {caractere_identifie} (Score : {meilleur_score:.4f})")
        return caractere_identifie
    else:
        print(f"⚠️ Identification échouée (Score : {meilleur_score:.4f}).")
        return "INCONNU"