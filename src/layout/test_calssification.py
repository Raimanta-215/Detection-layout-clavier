import os
import sys
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from layout.detection_type import classification

VERT = '\033[92m'
ROUGE = '\033[91m'
JAUNE = '\033[93m'
RESET = '\033[0m'

def test_auto_classification():
    print(f"\n{JAUNE}=== Lancement des Tests Automatiques de Classification ==={RESET}\n")

    
    scenarios = [
        {
            "nom": "Test AZERTY Classique",
            "img1": "img/test_touches/A_1.png", 
            "img2": "img/test_touches/Z_1.png",
            "attendu": "AZERTY"
        },
        {
            "nom": "Test QWERTY Classique",
            "img1": "img/test_touches/Q_1.png",
            "img2": "img/test_touches/W_1.png",
            "attendu": "QWERTY"
        },
        {
            "nom": "Test Partiel AZERTY (2ème touche ratée/inconnue)",
            "img1": "img/test_touches/A_1.png",
            "img2": "img/test_touches/Q_2.png", #TOUCHE INCONNUE
            "attendu": "AZERTY"
        },
        {
            "nom": "Test Partiel QWERTY (1ère touche ratée)",
            "img1": "img/test_touches/Q_2.png", #TOUCHE INCONNUE
            "img2": "img/test_touches/W_1.png",
            "attendu": "QWERTY"
        }
    ]

    nb_reussites = 0
    nb_tests = 0

    for scenario in scenarios:
        nom = scenario["nom"]
        path1 = scenario["img1"]
        path2 = scenario["img2"]
        attendu = scenario["attendu"]

        if not os.path.exists(path1) or not os.path.exists(path2):
            print(f"{ROUGE}[SKIP] {nom} : Images introuvables ({path1} ou {path2}){RESET}")
            continue

        nb_tests += 1
        print(f"Test : {nom}")
        print(f"   Images : {os.path.basename(path1)} & {os.path.basename(path2)}")

        try:
            resultat_obtenu = classification(path1, path2)
            
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
        print(f"\n{ROUGE}Aucun test n'a pu être lancé (vérifiez les chemins des images).{RESET}")

if __name__ == "__main__":
    test_auto_classification()