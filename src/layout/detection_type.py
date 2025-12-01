from layout.detection_lettre_v4 import detection_lettre
from layout.test_detetction_lettre import get_lettre_gab
import os
import glob


def identification_lettre(touche_detected):

    all_agabrits = sorted(glob.glob("gabarits/*/*.jpg"))

    touche = touche_detected


    lettre_identifie = "Inconnue"
    seuil_score = 0.65

    if  not all_agabrits:
        print("Aucune image ou gabarit trouvé dans les dossiers spécifiés.")
        return lettre_identifie
    
    for gabarit_path in all_agabrits:


        lettre_gab = get_lettre_gab(gabarit_path)
        nom_gab = os.path.basename(gabarit_path)

        try:
            score_actuel = detection_lettre(touche, gabarit_path, one=False)

            if score_actuel > seuil_score:
                lettre_identifie = lettre_gab
                return lettre_identifie

                
        except Exception as e:
            print(f"Erreur lors du traitement de l'image avec le gabarit {nom_gab} : {e}")



def classification (premiere_touche, deuxieme_touche):

    premiere_lettre = identification_lettre(premiere_touche)
    deuxieme_lettre = identification_lettre(deuxieme_touche)



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

    





