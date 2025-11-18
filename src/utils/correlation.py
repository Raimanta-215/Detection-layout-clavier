import numpy as np
import cv2
import matplotlib.pyplot as plt

# --- FONCTION PRINCIPALE DE CORRÉLATION (Purement NumPy) ---

def correlation_normalisee_numpy(image_path, gabarit_path):
    """
    Calcule le coefficient de corrélation croisée normalisée (CCNR) entre deux images.
    Ceci remplace cv2.matchTemplate() et l'OCR.
    """
    
    # Étape 1: Acquisition (lecture des chemins)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    gabarit = cv2.imread(gabarit_path, cv2.IMREAD_GRAYSCALE)

    if image is None or gabarit is None:
        print("❌ Erreur: Image ou gabarit non trouvé.")
        return 0.0

    # Étape 2: Normalisation des dimensions (Obligatoire pour cette méthode)
    # L'image d'entrée DOIT être redimensionnée à la taille exacte du gabarit
    # (Ex: si le gabarit est 30x30, l'image analysée le devient aussi).
    taille_gabarit = gabarit.shape
    image_redimensionnee = cv2.resize(image, (taille_gabarit[1], taille_gabarit[0]))
    
    # Binarisation (pour être sûr) et conversion en float pour les calculs NumPy
    _, image_bin = cv2.threshold(image_redimensionnee, 127, 255, cv2.THRESH_BINARY)
    _, gabarit_bin = cv2.threshold(gabarit, 127, 255, cv2.THRESH_BINARY)
    
    I = image_bin.astype(np.float64)
    T = gabarit_bin.astype(np.float64)

    # Étape 3: Calcul de la Corrélation Normalisée (NumPy)
    
    # 3.1. Normalisation en moyenne : I' = I - mean(I)
    I_norm = I - np.mean(I)
    T_norm = T - np.mean(T)

    # 3.2. Produit scalaire (Numérateur) : Somme(I' * T')
    # C'est la covariance entre les deux signaux/matrices.
    numerateur = np.sum(I_norm * T_norm)

    # 3.3. Dénominateur (Produit des normes L2)
    # Il assure que le score final est normalisé entre -1 et 1.
    denominateur = np.sqrt(np.sum(I_norm**2) * np.sum(T_norm**2))
    
    # Sécurité contre la division par zéro
    if np.isclose(denominateur, 0): 
        return 0.0

    score = numerateur / denominateur
    return score
