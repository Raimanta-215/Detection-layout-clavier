import numpy as np
from skimage.transform import resize
from skimage.filters import threshold_otsu
from utils.correlation_v4 import correlation
from skimage.io import imread
from skimage.color import rgb2gray
from traitement_image.processing import preprocess_image

def detection_lettre(image, gabarit):

    # --- PREPROCESSING ---

    img_traitee = preprocess_image(image, final_size=(64, 64))
    gab_traite = preprocess_image(gabarit, final_size=(64, 64))


    # --- CORRÉLATION ---
    score = correlation(img_traitee.flatten(), gab_traite.flatten())
    print(f"Score de corrélation: {score:.4f}")

    if score > 0.75:
        print("Lettre A.")
    else:
        print("Lettre inconnue.")
