from utils.correlation_v4 import correlation
from traitement_image.processing import preprocess_image
import matplotlib.pyplot as plt
from traitement_image.processing_type2 import preprocess_type2
import os

def detection_lettre(image, gabarit, one = False):

    # --- PREPROCESSING ---

    img_traitee = preprocess_image(image, final_size=(64, 64), is_gabarit=False)

    gab_traite = preprocess_image(gabarit, final_size=(64, 64), is_gabarit=True)




    # --- CORRÉLATION ---
    score = correlation(img_traitee.flatten(), gab_traite.flatten())

    if score > 0.65:
        print(f"Score de corrélation: {score:.4f}")
    elif score < 0.65:
        img_traitee  = preprocess_type2(image, final_size=(64, 64), is_gabarit=False)
        score = correlation(img_traitee.flatten(), gab_traite.flatten())
        print(f"RE  :Score de corrélation: {score:.4f}")
        
        if score > 0.65:
            pass
        else:print  ("Lettre inconnue.")
        
    else:
        print("Lettre inconnue.")


    #== test affichage ===

    if one:

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(img_traitee, cmap='gray')
        plt.title("Image lettre vue par l'algo")

        plt.subplot(1, 2, 2)
        plt.imshow(gab_traite, cmap='gray')
        plt.title("Gabarit vu par l'algo")

        plt.show()

    return score
