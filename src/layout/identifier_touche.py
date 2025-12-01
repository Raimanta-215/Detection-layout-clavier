import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout.detection_lettre_v4 import detection_lettre
from tests.test_detetction_lettre import get_lettre_gab
import glob

def identifier_une_touche(touche):

    tous_les_gabarits = sorted(glob.glob("gabarits/*/*"))

    meilleur_score = 0
    lettre_retenue = "Inconnue"
    seuil_score = 0.65
    
    for gabarit_path in tous_les_gabarits:
        try:
            lettre_gab = get_lettre_gab(gabarit_path) 
            
            score = detection_lettre(touche, gabarit_path, one=False)
            
            if score > meilleur_score:
                meilleur_score = score
                lettre_retenue = lettre_gab
                
        except Exception as e:
            print(f"Erreur avec le gabarit {gabarit_path}: {e}")

    if meilleur_score > seuil_score:
        return lettre_retenue
    else:
        return "Inconnue"