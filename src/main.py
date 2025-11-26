from layout.test_detetction_lettre import test_detection_lettre
from layout.detection_lettre_v4 import detection_lettre

def main():

    while True:
        print("PROJET LAYOUT")

        choix = int(
            input("Choisissez une option:\n1. Tester la détection de lettres sur plusieurs images\n2. Tester la détection de lettres sur une image spécifique\nVotre choix: "))

        if choix == 1:
            test_detection_lettre()
        elif choix == 2:
            choix_lettre = int(
                input("Chiffre de l'image test 1 à 5\n")
            )
            choix_gabarit = int(input("chiffre gabarit de 1 à 3 \n"))
            detection_lettre(
                f'img/test_touches/A_{choix_lettre}.png',
                f'gabarits/A/G_A_{choix_gabarit}.jpg',
                one=True
            )

if __name__ == "__main__":
    main()