import cv2
import numpy as np
from .rogner_lettre import rogner_lettre
from .resize import resize
import matplotlib.pyplot as plt

def preprocess_image(input_data, final_size=(64, 64)):

    # === 1. Charger l'image (déjà la version brute) ===
    if isinstance(input_data, str):
            img = cv2.imread(input_data, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise FileNotFoundError(f"Image introuvable : {input_data}")
    else:
        if len(input_data.shape) == 3:
            img = cv2.cvtColor(input_data, cv2.COLOR_BGR2GRAY)
        else:
            img = input_data

    # === 2. Appliquer un filtre de rehaussement ===
    kernel = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)

    # === 3. Inverser ===
    inverted = cv2.bitwise_not(sharpened)

    # === 4. Améliorer le contraste ===
    enhanced = cv2.convertScaleAbs(inverted, alpha=1.8, beta=0)

    # === 5. Agrandir fortement l'image ===
    scale = 8
    big = cv2.resize(enhanced, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    # === 6. Binarisation ===
    _, thresh = cv2.threshold(big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   
    # === 7. Rogner les bords vides ===

    image_cropped = rogner_lettre(thresh, padding=5)


    

    if final_size is not None:
            result = resize(image_cropped, target_size=final_size)
            return result / 255.0 
    

    
    return thresh