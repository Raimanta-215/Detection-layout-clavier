import cv2
import numpy as np

# === 1. Charger l'image (déjà la version brute) ===
img = cv2.imread("ToucheA.png", cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Image introuvable")

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