import cv2
import numpy as np
from .rogner_lettre import rogner_lettre
from .resize import resize

def preprocess_type2(input_data, final_size=(64, 64), is_gabarit=False):

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

    # === Standard preprocessing steps ===

    h, w = sharpened.shape
    corners = [sharpened[0, 0], sharpened[0, w-1], sharpened[h-1, 0], sharpened[h-1, w-1]]
    
    if np.mean(corners) > 127:
        working_img = cv2.bitwise_not(sharpened)
    else:
        working_img = sharpened

    # === 3. Inverser ===

    blurred = cv2.GaussianBlur(working_img, (5, 5), 0)

    kernel2 = cv2.getStructuringElement(cv2 .MORPH_RECT, (15, 15))
    top_hat = cv2.morphologyEx(blurred, cv2.MORPH_TOPHAT, kernel2)

    # === 4. Améliorer le contraste ===
    enhanced = cv2.add(blurred,top_hat)
    enhanced2 = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
    # === 5. Agrandir fortement l'image ===
    scale = 8
    big = cv2.resize(enhanced2, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    # === 6. Binarisation ===
    _, thresh = cv2.threshold(big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   

    kernel_clean = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh_clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel_clean)
    # === 7. Rogner les bords vides ===

    image_cropped = rogner_lettre(thresh_clean, padding=5, is_gabarit=is_gabarit)


    h, w = image_cropped.shape
    corners = [
        image_cropped[0, 0], image_cropped[0, w-1],
        image_cropped[h-1, 0], image_cropped[h-1, w-1]
    ]

    if np.mean(corners) > 127:
        good_img = cv2.bitwise_not(image_cropped)
    else:
        good_img = image_cropped
    

    if final_size is not None:
            result = resize(good_img, target_size=final_size)
            return result / 255.0 
    

    
    return thresh