import cv2 as   cv
import numpy as np

def resize(image, target_size=(64, 64)):
    
    h, w = image.shape
    target_h, target_w = target_size

    #== Calculer facteur echelle

    scale = min(target_w / w, target_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    #== Redimensionner l'image

    resized = cv.resize(image, (new_w, new_h), interpolation=cv.INTER_AREA)

    #== Créer une nouvelle image avec fond noir
    output_image = np.zeros((target_h, target_w), dtype=image.dtype)

    #== centerer l'image redimensionnée
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2

    output_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return output_image