# detetction_lettre_v2.py (Classifieur/Correlation Manuelle)
from utils.correlation import correlation_normalisee_numpy as calculer_carte_correlation
import matplotlib.pyplot as plt
import cv2
from layout.debug import debug_visualisation_correlation

def classifieur_par_correlation_glissante(image_a_analyser_path, chemins_gabarits_dict):
    """
    Classifieur qui utilise la Corrélation par Fenêtre Glissante pour localiser 
    et identifier le caractère le plus probable dans l'image.
    """
    
    meilleur_score_absolu = -1.0
    caractere_identifie = "INCONNU"
    meilleure_position = (0, 0) # (y, x)
    taille_gabarit = (0, 0) # (w, h)

    # --- ÉTAPE 1: CLASSIFICATION PAR MAX DE CORRÉLATION ---
    for classe, liste_chemins in chemins_gabarits_dict.items():
        for chemin_gabarit_unique in liste_chemins:
            
            # Appel à la fonction qui effectue la corrélation glissante
            # Retourne : score, (y, x), w_t, h_t
            resultat = calculer_carte_correlation(image_a_analyser_path, chemin_gabarit_unique)
            
            if resultat is None: continue 
            max_score_local, max_loc_local, w_t, h_t, carte_locale = resultat
            
            # Mise à jour du meilleur match sur TOUS les gabarits
            if max_score_local > meilleur_score_absolu:
                meilleur_score_absolu = max_score_local
                caractere_identifie = classe
                meilleure_position = max_loc_local
                taille_gabarit = (w_t, h_t)



    # --- ÉTAPE 2: DÉCISION FINALE (Classification) ---
    SEUIL_DE_CONFIANCE = 0.70 # Seuil souvent utilisé pour la CCNR en image

    if meilleur_score_absolu >= SEUIL_DE_CONFIANCE:
        
        # Visualisation de la zone de meilleure corrélation (Chapitre 8)

        print(f"\n--- RÉSULTAT FINAL ---")
        print(f"Caractère identifié : **{caractere_identifie}**")
        print(f"Score max trouvé : {meilleur_score_absolu:.4f}")
        print(f"Position (y, x) du match : {meilleure_position}")
        return caractere_identifie
    else:
        print(f"⚠️ Identification échouée. Score max : {meilleur_score_absolu:.4f} est inférieur au seuil.")
        return "INCONNU"


