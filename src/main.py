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
            detection_lettre(
                "img/test_touches/A_3.png",
                "gabarits/A/G_A_2.jpg",
                one=True
            )

if __name__ == "__main__":
    main()