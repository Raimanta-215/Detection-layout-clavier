import cv2 as cv
import numpy as np

def rogner_lettre(image, padding = 2, is_gabarit=False):

    if image.dtype != np.uint8:
        img_8u = (image * 255).astype(np.uint8) if image.max() <= 1 else image.astype(np.uint8)
    else:
        img_8u = image

    # ===  Trouver les contours ===

    contours, hierarchy = cv.findContours(img_8u, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)    
    if contours is None:
        return image
    
    
    #=== Trouver le plus grand contour ===
    if is_gabarit:

        c = max(contours, key=cv.contourArea)
        
    else :
        hierarchy = hierarchy[0]

        best_candidate_idx = -1
        max_area = 0

        for i, c in enumerate(contours):
            area = cv.contourArea(c)
            
            has_parent = hierarchy[i][3] != -1
            
            if has_parent:
                if area > max_area:
                    max_area = area
                    best_candidate_idx = i
            
        if best_candidate_idx == -1:
            best_candidate_idx = max(range(len(contours)), key=lambda i: cv.contourArea(contours[i]))

        c = contours[best_candidate_idx]

    x, y, w, h = cv.boundingRect(c)

    height, width = image.shape

    x_start = max(x - padding, 0)
    y_start = max(y - padding, 0)
    x_end = min(x + w + padding, width)
    y_end = min(y + h + padding, height)



    #===  Rogner l'image ===

    cropped = image[y_start:y_end, x_start:x_end]
    return cropped
