import cv2 as cv
import numpy as np

def rogner_lettre(image, padding = 2):
    # === 1. Trouver les contours ===
    contours = cv.findNonZero(image)

    if contours is None:
        return image
    
    x, y, w, h = cv.boundingRect(contours)

    height, width = image.shape

    x_start = max(x - padding, 0)
    y_start = max(y - padding, 0)
    x_end = min(x + w + padding, width)
    y_end = min(y + h + padding, height)

    #=== 2. Rogner l'image ===

    cropped = image[y_start:y_end, x_start:x_end]
    return cropped
