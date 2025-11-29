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

    chemin_image = Path("img/keyboard.jpg")
    chemin_sortie = Path("img/clavier_recadrer/keyboard_recadre.jpg")

    
    clavier = recadrer_clavier_depuis_fichier(chemin_image, chemin_sortie)

    if clavier is None:
        print("❌ Aucun clavier détecté.")
        return

    print("✅ Clavier détecté et recadré !")
    print(f"📂 Image enregistrée dans : {chemin_sortie}")

    # Affichage du résultat
    clavier_rgb = cv2.cvtColor(clavier, cv2.COLOR_BGR2RGB)
    plt.imshow(clavier_rgb)
    plt.title("Clavier recadré")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()