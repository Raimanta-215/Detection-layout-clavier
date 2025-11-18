import numpy as np
import cv2

# --- CORRECTION ACADÉMIQUE : Corrélation par Fenêtre Glissante ---

def correlation_normalisee_numpy(image_path, gabarit_path):
    """
    Calcule la Corrélation Croisée Normalisée (CCNR) sur toute l'image
    en utilisant une fenêtre glissante purement en NumPy.
    
    Retourne le score maximum et la position (y, x) de ce match.
    """
    
    # Étape 1: Acquisition et Prétraitement
    image_brut = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    gabarit = cv2.imread(gabarit_path, cv2.IMREAD_GRAYSCALE)

    if image_brut is None or gabarit is None:
        return 0.0, (0, 0) # Score et position par défaut
    
    # 🔑 Étape 2: Redimensionnement de l'Image (I) à la taille du Gabarit (T)
    # Ceci est la correction du Mismatch d'Échelle.
    h_t, w_t = gabarit.shape
    
    # Utilisation de INTER_AREA pour réduire (meilleure qualité pour la corrélation)
    image = cv2.resize(image_brut, (w_t, h_t), interpolation=cv2.INTER_AREA)
    
    # Assurer la binarisation et la conversion en float pour les calculs NumPy
    _, I = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    _, T = cv2.threshold(gabarit, 127, 255, cv2.THRESH_BINARY)
    I = I.astype(np.float64)
    T = T.astype(np.float64)

    # Dimensions
    (h_i, w_i) = I.shape       # Hauteur et Largeur de l'image
    (h_t, w_t) = T.shape       # Hauteur et Largeur du gabarit

    if h_t > h_i or w_t > w_i:
        print(f"❌ Erreur de dimension: Le gabarit ({h_t}x{w_t}) est plus grand que l'image ({h_i}x{w_i}).")
        # Retourne 0 pour ce test, car la corrélation est impossible
        return 0.0, (0, 0), w_t, h_t, None
    
    meilleur_score = -1.0
    meilleure_position = (0, 0) # (y, x)

    # Moyenne et Norme L2 du gabarit (calculées une seule fois)
    T_norm = T - np.mean(T)
    T_std = np.sqrt(np.sum(T_norm**2))
    
    if np.isclose(T_std, 0): return 0.0, (0, 0) # Gabarit vide ou uniforme

    # --- ÉTAPE 2: CORRÉLATION PAR FENÊTRE GLISSANTE (Boucles et NumPy) ---
    h_map = h_i - h_t + 1
    w_map = w_i - w_t + 1

    correlation_map = np.zeros((h_map, w_map), dtype=np.float64)

    # Le filtre (gabarit) glisse de (0, 0) jusqu'à (H_i - H_t, W_i - W_t)
    for y in range(0,h_map):
        for x in range(0, w_map):
            
            # Découper la fenêtre (signal) : I_window est une matrice NumPy
            I_window = I[y:y + h_t, x:x + w_t]
            
            # --- CALCUL CCNR (Méthode de Classification/Similarité) ---
            
            # 1. Normalisation en moyenne de la fenêtre
            I_win_norm = I_window - np.mean(I_window)
            
            # 2. Corrélation (Numérateur = Produit Scalaire des signaux normalisés)
            numerateur = np.sum(I_win_norm * T_norm)
            
            # 3. Dénominateur (Produit des normes L2)
            I_win_std = np.sqrt(np.sum(I_win_norm**2))
            denominateur = I_win_std * T_std
            
            # Score CCNR (entre -1.0 et 1.0)
            if np.isclose(denominateur, 0):
                score = 0.0
            else:
                score = numerateur / denominateur

            correlation_map[y, x] = score

            # Mise à jour du meilleur score et de la position
            if score > meilleur_score:
                meilleur_score = score
                meilleure_position = (y, x) # (y, x)

    # Retourne le score max et la position (y, x) du coin supérieur gauche
    return meilleur_score, meilleure_position, correlation_map, T.shape[1], T.shape[0] # score, (y, x), w_t, h_t