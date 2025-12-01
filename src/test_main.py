from layout.test_detetction_lettre import test_detection_lettre
from layout.detection_lettre_v4 import detection_lettre

def main():

    while True:
        print("\n\nPROJET LAYOUT\n\n")

        choix = int(
            input("Choisissez une option:\n1. Tester la détection de lettres sur plusieurs images\n2. Tester la détection de lettres sur une image spécifique\nVotre choix: "))

        try:
            if choix == 1:
                test_detection_lettre()
                
            elif choix == 2:
                choix_lettre = input("Lettre à tester (A, W, Q, Z)\n").upper()
                nbr_lettre = int(input("Nombre d'images à tester (1 à 5)\n"))
                choix_gabarit = int(
                    input("Nombre de gabarits à tester 1 à 2\n")
                )

                try:
                    detection_lettre(
                        f'img/test_touches/{choix_lettre}_{nbr_lettre}.png',
                        f'gabarits/{choix_lettre}/G_{choix_lettre}_{choix_gabarit}.jpg',
                        one=True,
                        
                    )
                    
                except FileNotFoundError as e:
                
                    print(f"Fichier non trouvé: {e}, essaie un nbr plus petit")

        except e as Exception:
            print("Choix invalide. Veuillez sélectionner 1 ou 2.")

if __name__ == "__main__":
    main()