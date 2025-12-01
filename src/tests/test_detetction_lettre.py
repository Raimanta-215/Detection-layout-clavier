
from layout.detection_lettre_v4 import detection_lettre
import glob
import os

VERT = '\033[92m'
ROUGE = '\033[91m'
JAUNE = '\033[93m'
RESET = '\033[0m' 

def get_lettre_gab(gabarit_path):

    lettre = gabarit_path.split('_')[1]  
    return lettre

def get_lettre_attendu(image_path):

    lettre = image_path.split('\\')[-1].split('_')[0]
    return lettre


def test_detection_lettre():

    
    nbr_reussite = 0
    lettre_identifie = "--Inconnue--"
    nombre_tests = 0
    seuil_score = 0.65


    toutes_les_images = sorted(glob.glob("img/test_touches/*_*"))

    tous_les_gabarits = sorted(glob.glob("gabarits/*/*"))

    if not toutes_les_images or not tous_les_gabarits:
        print("Aucune image ou gabarit trouvé dans les dossiers spécifiés.")
        return lettre_identifie
    
    for image_path in toutes_les_images:

        lettre_attendue = get_lettre_attendu(image_path)

        meilleur_score = -1
        nom_img = os.path.basename(image_path)

        print(f"\n{JAUNE}=== Test pour l'image : {nom_img}{RESET} ===")

        for gabarit_path in tous_les_gabarits:


            lettre_gab = get_lettre_gab(gabarit_path)
            nom_gab = os.path.basename(gabarit_path)
            nombre_tests += 1

            doit_marcher = (lettre_attendue == lettre_gab)


            print   (f"\n--- Avec le gabarit : {nom_gab} pour la lettre {lettre_gab} ---")
            try:
                score_actuel = detection_lettre(image_path, gabarit_path, one=False)
                succes = False
                type_eval = ""

                if doit_marcher:
                    if score_actuel > seuil_score:
                        succes = True
                        type_eval = "SUCCES"
                    else:
                        type_eval = "ECHEC"
                else:
                    if score_actuel <= seuil_score:
                        succes = True
                        type_eval = "SUCCES vrai négatif"
                    else:
                        type_eval = "ECHEC" 


                if succes:
                    nbr_reussite += 1
                    couleur = VERT
                else:
                    couleur = ROUGE

                print(f"   Vs {nom_gab} ({lettre_gab}) : Score {score_actuel:.4f} --> {couleur}{type_eval}{RESET}")

                if score_actuel > meilleur_score:
                    meilleur_score = score_actuel
                    lettre_identifie = lettre_gab


            except Exception as e:
                print(f"Erreur lors du traitement de l'image {nom_img} avec le gabarit {nom_gab} : {e}")
       
        if meilleur_score > seuil_score:
            resultat = lettre_identifie
        else:
            resultat = "--Inconnue--"

        couleur_finale = VERT if resultat == lettre_attendue else ROUGE

        print(eval)
        print(f"\n\n{couleur_finale}==> Meilleur score pour l'image {meilleur_score:.4f}{RESET}")
        print(f"\nLettre identifiée {resultat}{RESET}")

    if nombre_tests > 0:
        pourcentage = (nbr_reussite / nombre_tests) * 100
    else:
        pourcentage = 0.0

    couleur_p = VERT if pourcentage > 75 else ROUGE

    print("""
        ╦═╗╔═╗╔═╗╦ ╦╦  ╔╦╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗╔╦╗╔═╗
        ╠╦╝║╣ ╚═╗║ ║║   ║ ╠═╣ ║    ║ ║╣ ╚═╗ ║ ╚═╗
        ╩╚═╚═╝╚═╝╚═╝╩═╝ ╩ ╩ ╩ ╩    ╩ ╚═╝╚═╝ ╩ ╚═╝
                                             
    \n""")
    print(f"\n{couleur_p}==> Pourcentage de fiabilité {pourcentage:.2f}% sur {nombre_tests} tests {RESET} ")

    