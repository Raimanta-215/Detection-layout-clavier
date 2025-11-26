from layout.detection_lettre_v4 import detection_lettre
import glob
import os

def test_detection_lettre():

    
    toutes_les_images = sorted(glob.glob("img/test_touches/*.png"))

    tous_les_gabarits = sorted(glob.glob("gabarits/A/*.jpg"))

    if not toutes_les_images or not tous_les_gabarits:
        print("Aucune image ou gabarit trouvé dans les dossiers spécifiés.")
        return
    
    for image_path in toutes_les_images:

        nom_img = os.path.basename(image_path)
        print(f"\n=== Test pour l'image : {nom_img} ===")

        for gabarit_path in tous_les_gabarits:
            nom_gab = os.path.basename(gabarit_path)
            print   (f"\n--- Avec le gabarit : {nom_gab} ---")

            try:
                detection_lettre(image_path, gabarit_path)
            except Exception as e:
                print(f"Erreur lors du traitement de l'image {nom_img} avec le gabarit {nom_gab} : {e}")




