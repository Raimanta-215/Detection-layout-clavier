from pathlib import Path
import cv2
import matplotlib.pyplot as plt


from src.traitement_image.recadrage_clavier import recadrer_clavier_depuis_fichier
#from src.layout.detection_lettre_v4 import detection_lettre


def main():
    print("PROJET LAYOUT")

    #image_path = 'img/test_touches/A_1.png'
    #chemins_gabarits = 'gabarits/G_A_1.jpg'

    #detection_lettre(image_path,chemins_gabarits)

    chemin_image = Path("img/dae03075-2ad0-416b-a9e5-02c1fba5e079.jpg")
    chemin_sortie = Path("img/clavier_recadrer/dae03075-2ad0-416b-a9e5-02c1fba5e079_recadre.jpg")

    image_orig = cv2.imread(str(chemin_image))
    if image_orig is None:
        print(f"Impossible de lire l'image d'origine : {chemin_image}")
        return
    
    clavier = recadrer_clavier_depuis_fichier(chemin_image, chemin_sortie)

    if clavier is None:
        print("❌ Aucun clavier détecté.")
        return

    print("✅ Clavier détecté et recadré !")
    print(f"📂 Image enregistrée dans : {chemin_sortie}")


    image_orig_rgb = cv2.cvtColor(image_orig, cv2.COLOR_BGR2RGB)
    clavier_rgb = cv2.cvtColor(clavier, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image_orig_rgb)
    plt.title("Clavier d'origine")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(clavier_rgb)
    plt.title("Clavier recadré")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()