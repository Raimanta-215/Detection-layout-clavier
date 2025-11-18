import cv2
import numpy as np
import matplotlib.pyplot as plt
def identifier_caractere(image_path, chemins_gabarits):
    """
    Identifie un unique caractère en le comparant à une liste de gabarits (multi-template).
    
    :param chemins_gabarits: Dictionnaire { 'A': [path_A1, path_A2, ...], 'Q': [...] }
    """
    
    # ... (Étape 1: Acquisition de input_image, comme précédemment) ...
    # (Supposons que 'input_image' a été chargé et binarisé)
    input_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if input_image is None: return "INCONNU"
    _, input_image = cv2.threshold(input_image, 127, 255, cv2.THRESH_BINARY)
    
    # Initialisation du meilleur score et du meilleur candidat
    meilleur_score = -1.0
    caractere_identifie = "INCONNU"

    # --- ÉTAPE 2: CLASSIFICATION ROBUSTE PAR BOUCLE (Chapitre 9) ---
    
    # Boucle sur les classes (A, Q)
    for classe, chemins in chemins_gabarits.items():
        # Boucle sur chaque gabarit pour cette classe
        for chemin_gabarit in chemins:
            template = cv2.imread(chemin_gabarit, cv2.IMREAD_GRAYSCALE)
            if template is None: continue
            _, template = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)
            
            # Calcul de la Corrélation (Mesure de Similarité)
            # La taille de l'input_image doit être égale à celle du template pour cette fonction
            # On suppose ici que toutes les images ont été normalisées à la même taille (Pre-processing)
            
            try:
                score = cv2.matchTemplate(input_image, template, cv2.TM_CCOEFF_NORMED)[0][0]
            except:
                # Si les tailles ne correspondent pas (cas fréquent), on ne peut pas corréler.
                print(f"⚠️ Taille non compatible avec le gabarit {chemin_gabarit}")
                continue

            # Mise à jour du meilleur score
            if score > meilleur_score:
                meilleur_score = score
                caractere_identifie = classe
                
    # --- ÉTAPE 3: DÉCISION FINALE ---
    
    SEUIL_DE_CONFIANCE = 0.85 # Seuil élevé requis pour la classification

    if meilleur_score >= SEUIL_DE_CONFIANCE:
        print(f"\n--- RÉSULTAT FINAL ROBUSTE ---")
        print(f"Caractère identifié : **{caractere_identifie}**")
        print(f"Score maximum de corrélation : {meilleur_score:.4f}")
        return caractere_identifie
    else:
        print(f"\n--- RÉSULTAT FINAL ROBUSTE ---")
        print(f"Score max trop faible ({meilleur_score:.4f} < {SEUIL_DE_CONFIANCE}). Classification échouée.")
        return "INCONNU"


