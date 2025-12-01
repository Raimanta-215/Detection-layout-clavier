from layout.detection_lettre_v4 import detection_lettre
from layout.test_detetction_lettre import get_lettre_gab
import os
import glob
from traitement_image.detectionTouche import preprocess_image


def identifier_une_touche(touche):

    tous_les_gabarits = sorted(glob.glob("gabarits/*/*.jpg"))

    meilleur_score = 0
    lettre_retenue = "Inconnue"
    seuil_score = 0.65
    
    for gabarit_path in tous_les_gabarits:
        try:
            lettre_gab = get_lettre_gab(gabarit_path) 
            
            score = detection_lettre(image_touche, gabarit_path, one=False)
            
            if score > meilleur_score:
                meilleur_score = score
                lettre_retenue = lettre_gab
                
        except Exception as e:
            print(f"Erreur avec le gabarit {gabarit_path}: {e}")

    if meilleur_score > seuil_score:
        return lettre_retenue
    else:
        return "Inconnue"
    

def classification ():

    premiere_lettre = preprocess_image()[0]
    deuxieme_lettre = preprocess_image()[1]



    if premiere_lettre is 'A' :
        if deuxieme_lettre is 'Z':
            return "AZERTY"
        
    if deuxieme_lettre is 'W':
        return "QWERTY"
    
    if premiere_lettre == "Inconnue" and deuxieme_lettre == "Inconnue" :
        return "Inconnu"
    
    if premiere_lettre == "Inconnue" :
        if deuxieme_lettre == 'W':
            return "QWERTY"

    





