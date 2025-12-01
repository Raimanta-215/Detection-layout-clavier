import os
import sys
import glob
import numpy as np # Import nécessaire pour vérifier si c'est une image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from traitement_image.detectionTouche import detec_key_image
from layout.detection_type import classification

VERT = '\033[92m'
ROUGE = '\033[91m'
JAUNE = '\033[93m'
RESET = '\033[0m'



def test_auto_classification(clvr):
    print(f"\n{JAUNE}=== Lancement des Tests Automatiques de Classification ==={RESET}\n")

    try:
        img_reelle_1, img_reelle_2, dig = detec_key_image(clvr)
        test_reel_dispo = True
    except Exception as e:
        print(f"{ROUGE}Attention: Impossible de charger l'image réelle {clvr}: {e}{RESET}")
        test_reel_dispo = False
        img_reelle_1, img_reelle_2 = None, None

    scenarios = [
        {
            "nom": "Test clavier réél QWERTY (Extraction auto)",
            "img1": img_reelle_1, 
            "img2": img_reelle_2,
            "attendu": "QWERTY",
            "is_raw_image": True # Marqueur pour dire que ce n'est pas un chemin
        }]

    """
        {
            "nom": "Test AZERTY Classique",
            "img1": "img/test_touches/A_1.png", 
            "img2": "img/test_touches/Z_1.png",
            "attendu": "AZERTY"
        },
        {
            "nom": "Test QWERTY Classique",
            "img1": "img/test_touches/Q_2.png",
            "img2": "img/test_touches/W_1.png",
            "attendu": "QWERTY"
        },
        {
            "nom": "Test Partiel AZERTY (2ème touche ratée)",
            "img1": "img/test_touches/A_1.png",
            "img2": "img/test_touches/Q_2.png", 
            "attendu": "AZERTY"
        },
        {
            "nom": "Test Partiel QWERTY (1ère touche ratée)",
            "img1": "img/test_touches/Q_2.png",
            "img2": "img/test_touches/W_1.png",
            "attendu": "QWERTY"
        }
        """

    

    nb_reussites = 0
    nb_tests = 0

    for scenario in scenarios:
        nom = scenario["nom"]
        entree1 = scenario["img1"]
        entree2 = scenario["img2"]
        attendu = scenario["attendu"]
        
        # Vérification spéciale pour le cas où l'extraction réelle a échoué
        if scenario.get("is_raw_image") and not test_reel_dispo:
            print(f"{ROUGE}[SKIP] {nom} : Extraction précédente échouée{RESET}")
            continue

        # Gestion différente si c'est un chemin (str) ou une image (array)
        if isinstance(entree1, str):
            # C'est un chemin de fichier
            if not os.path.exists(entree1) or not os.path.exists(entree2):
                print(f"{ROUGE}[SKIP] {nom} : Images introuvables ({entree1}){RESET}")
                continue
            nom_affich = f"{os.path.basename(entree1)} & {os.path.basename(entree2)}"
        else:
            # C'est une image directe (numpy array)
            nom_affich = "Images en mémoire "

        nb_tests += 1
        print(f"Test : {nom}")
        print(f"   Source : {nom_affich}")

        try:
            # On passe les arguments (soit des chemins, soit des images)
            resultat_obtenu = classification(entree1, entree2)
            
            if resultat_obtenu == attendu:
                print(f"   Résultat : {VERT}{resultat_obtenu} (CORRECT){RESET}")
                nb_reussites += 1
            else:
                print(f"   Résultat : {ROUGE}{resultat_obtenu} (ATTENDU: {attendu}){RESET}")

        except Exception as e:
            print(f"   {ROUGE}Erreur technique : {e}{RESET}")
        
        print("-" * 40)

    # --- BILAN ---
    if nb_tests > 0:
        score = (nb_reussites / nb_tests) * 100
        couleur_finale = VERT if score == 100 else ROUGE
        print(f"\n{couleur_finale}Bilan : {score:.0f}% de réussite ({nb_reussites}/{nb_tests} scénarios valides){RESET}")
    else:
        print(f"\n{ROUGE}Aucun test n'a pu être lancé.{RESET}")
    



def test_toutes_classifications():
    toutes_img = sorted(glob.glob("img/clavier_recadrer/*.*"))

    for img_path in toutes_img:
        print(f"\n--- Test automatique de classification pour l'image : {os.path.basename(img_path)} ---")
        test_auto_classification(img_path)


if __name__ == "__main__":
    test_toutes_classifications()