import os
import sys
import glob

# Configuration des chemins pour importer les modules frères
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from traitement_image.detectionTouche import detec_key_image
from layout.detection_type import classification

# Couleurs pour la console
VERT = '\033[92m'
ROUGE = '\033[91m'
JAUNE = '\033[93m'
RESET = '\033[0m'

def test_auto_classification(image_path, layout_attendu="QWERTY"):
    nom_fichier = os.path.basename(image_path)
    print(f"\n{JAUNE}=== Test sur l'image : {nom_fichier} ==={RESET}")

    # 1. Extraction des touches (Traitement d'image)
    try:
        # On essaie d'extraire les touches
        img_touche_1, img_touche_2, dig = detec_key_image(image_path)
        
        # Vérification critique : Si detectionTouche renvoie None, on arrête tout de suite
        if img_touche_1 is None:
             print(f"{ROUGE}   [ECHEC CRITIQUE] Impossible d'isoler les touches (lignes non trouvées){RESET}")
             return False

    except Exception as e:
        print(f"{ROUGE}   [ERREUR TECHNIQUE] Lors de l'extraction : {e}{RESET}")
        return False

    # 2. Classification (Reconnaissance des lettres)
    print(f"   > Touches extraites avec succès. Lancement de l'identification...")
    
    try:
        # On lance la classification sur les images extraites (tableaux numpy)
        resultat_obtenu = classification(img_touche_1, img_touche_2)
        
        # 3. Vérification du résultat
        if resultat_obtenu == layout_attendu:
            print(f"   > Résultat : {VERT}{resultat_obtenu} (CORRECT){RESET}")
            return True
        else:
            print(f"   > Résultat : {ROUGE}{resultat_obtenu} (FAUX - Attendu: {layout_attendu}){RESET}")
            print(f"     {ROUGE}Analysez pourquoi : Le 'Q' a-t-il été vu comme un 'A' ?{RESET}")
            return False

    except Exception as e:
        print(f"   {ROUGE}[ERREUR] Lors de la classification : {e}{RESET}")
        return False


def test_toutes_classifications():
    # On récupère toutes les images dans le dossier
    extensions = ["*.jpg", "*.jpeg", "*.png"]
    toutes_img = []
    for ext in extensions:
        toutes_img.extend(glob.glob(f"img/clavier_recadrer/{ext}"))
    
    toutes_img = sorted(toutes_img)
    
    total_files = 0
    total_success = 0

    if not toutes_img:
        print(f"{ROUGE}Aucune image trouvée dans img/clavier_recadrer/{RESET}")
        return

    print(f"Début des tests sur {len(toutes_img)} images (Attente : TOUT QWERTY)...")

    for img_path in toutes_img:
        # ICI : On force l'attente à QWERTY car vous avez confirmé que c'est le cas
        succes = test_auto_classification(img_path, layout_attendu="QWERTY")
        
        total_files += 1
        if succes:
            total_success += 1

    # Bilan Global
    if total_files > 0:
        pourcentage = (total_success / total_files) * 100
        couleur = VERT if pourcentage > 80 else ROUGE
        print(f"\n{couleur}=== BILAN FINAL : {pourcentage:.1f}% de réussite ({total_success}/{total_files} images) ==={RESET}")

if __name__ == "__main__":
    test_toutes_classifications()