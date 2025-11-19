from layout.detection_lettre_v4 import detection_lettre
def main():
    print("PROJET LAYOUT")

    image_path = 'img/test_touches/A_1.png'
    chemins_gabarits = 'gabarits/G_A_1.jpg'

    detection_lettre(image_path,chemins_gabarits)




if __name__ == "__main__":
    main()