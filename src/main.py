from layout.detection_lettre import identifier_caractere
from layout.detetction_lettre_v2 import classifieur_par_correlation
def main():
    print("PROJET LAYOUT")

    image_path = 'img/test_touches/A_1.png'
    chemins_gabarits = {
        'A': ['gabarits/A.jpg']
    }

    #identifier_caractere(image_path, chemins_gabarits)

    classifieur_par_correlation(image_path,chemins_gabarits)



if __name__ == "__main__":
    main()