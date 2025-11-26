from layout.detection_lettre_v4 import detection_lettre
import glob
import os

VERT = '\033[92m'
ROUGE = '\033[91m'
JAUNE = '\033[93m'
RESET = '\033[0m' 

def test_detection_lettre():

    
    nbr_reussite = 0

    toutes_les_images = sorted(glob.glob("img/test_touches/*.png"))

    tous_les_gabarits = sorted(glob.glob("gabarits/A/*.jpg"))

    if not toutes_les_images or not tous_les_gabarits:
        print("Aucune image ou gabarit trouvé dans les dossiers spécifiés.")
        return
    
    for image_path in toutes_les_images:

        meilleur_score = -1

        nom_img = os.path.basename(image_path)
        print(f"\n{JAUNE}=== Test pour l'image : {nom_img}{RESET} ===")

        for gabarit_path in tous_les_gabarits:
            nom_gab = os.path.basename(gabarit_path)
            print   (f"\n--- Avec le gabarit : {nom_gab} ---")
            try:
                score_actuel = detection_lettre(image_path, gabarit_path, one=False)

                if score_actuel > meilleur_score:
                    meilleur_score = score_actuel

            except Exception as e:
                print(f"Erreur lors du traitement de l'image {nom_img} avec le gabarit {nom_gab} : {e}")
        if meilleur_score > 0.65:
            couleur = VERT
            nbr_reussite += 1
        else:
            couleur = ROUGE

        print(f"\n\n{couleur}==> Meilleur score pour l'image {meilleur_score:.4f}{RESET}")
        
    nbr_total_images = len(toutes_les_images)
    if nbr_total_images > 0:
        pourcentage = (nbr_reussite / nbr_total_images) * 100
    else:
        pourcentage = 0.0

    couleur_p = VERT if pourcentage > 70 else ROUGE
    print(f"\n{couleur_p}==> Pourcentage de reuissite {pourcentage:.2f}{RESET} ")

