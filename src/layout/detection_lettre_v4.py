import numpy as np
from skimage.transform import resize
from skimage.filters import threshold_otsu
from utils.correlation_v4 import correlation
from skimage.io import imread
from skimage.color import rgb2gray

def detection_lettre(image, gabarit):

    # --- CHARGEMENT ---
    img = imread(image)
    gab = imread(gabarit)

    # --- SUPPRESSION CANAL ALPHA ---
    if img.ndim == 3 and img.shape[2] == 4:
        img = img[:, :, :3]
    if gab.ndim == 3 and gab.shape[2] == 4:
        gab = gab[:, :, :3]

    # --- GRAYSCALE ---
    if img.ndim == 3:
        img = rgb2gray(img)
    if gab.ndim == 3:
        gab = rgb2gray(gab)




    # --- BINARISATION SEULEMENT POUR L’IMAGE D’ENTRÉE ---
    th = threshold_otsu(img)
    img_bin = (img > th).astype(np.float32)

    # -- DECOUPE ---

    mask = (img > th).astype(np.uint8)

    if mask.mean() < 0.5:
        mask = 1 - mask

    # -- ZONE BORNEE ---

    ys, xs = np.where(mask == 1)

    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()

    cropped_img = img_bin[y_min:y_max , x_min:x_max ]

    # -- PADDING ---

    padding = 1
    cropped_padded = np.pad(
        cropped_img,
        pad_width=padding,
        mode='constant',
        constant_values=0
    )

    # --- NORMALISATION TAILLE ---
    img_norm = resize(cropped_padded, (64, 64), anti_aliasing=True)
    gab_norm = resize(gab, (64, 64), anti_aliasing=True)

    # --- CORRÉLATION ---
    score = correlation(img_norm.flatten(), gab_norm.flatten())
    print(f"Score de corrélation: {score}")

    if score > 0.75:
        print("Lettre A.")
    else:
        print("Lettre inconnue.")
