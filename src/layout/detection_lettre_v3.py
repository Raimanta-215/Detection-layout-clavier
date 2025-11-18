import numpy as np
from skimage.transform import resize
from skimage.filters import threshold_otsu




def detection_lettre(image, gabarit):
    """
    Détecte la lettre dans l'image en utilisant la corrélation normalisée.
    
    Args:
        image (ndarray): Image d'entrée en niveaux de gris.
        gabarit (ndarray): Gabarit de la lettre à détecter en niveaux de gris.
        
    Returns:
        float: Score de corrélation maximale.
        tuple: Position (y, x) du meilleur match.
    """
    
    # Redimensionner l'image à la taille du gabarit
    h_t, w_t = gabarit.shape
    image_redimensionnee = resize(image, (h_t, w_t), anti_aliasing=True)
    
    # Binarisation des images
    seuil_image = threshold_otsu(image_redimensionnee)
    I = (image_redimensionnee > seuil_image).astype(np.float64)
    
    seuil_gabarit = threshold_otsu(gabarit)
    T = (gabarit > seuil_gabarit).astype(np.float64)
    
    # Calcul de la corrélation normalisée
    I_norm = I - np.mean(I)
    T_norm = T - np.mean(T)
    
    numerator = np.sum(I_norm * T_norm)
    denominator = np.sqrt(np.sum(I_norm**2) * np.sum(T_norm**2))
    
    if denominator == 0:
        return 0.0, (0, 0)  # Éviter la division par zéro
    
    score_correlation = numerator / denominator
    
    # Pour cette version simplifiée, on retourne une position fictive
    position_meilleur_match = (0, 0)
    
    return score_correlation, position_meilleur_match
#binarisation avec skimage
