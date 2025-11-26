import numpy as np

def correlation(img1, img2):
    img1 = img1 - np.mean(img1)
    img2 = img2 - np.mean(img2)

    num = np.sum(img1 * img2)
    den = np.sqrt(np.sum(img1**2) * np.sum(img2**2))

    if den  == 0:
        return 0.0 # Éviter la division par zéro   
    return  num / den