import matplotlib.pyplot as plt
import numpy as np
import skimage as skim
from skimage.transform import resize

#Lire l'image et mettre en niveau de gris
I = skim.img_as_float(plt.imread('img/Querty.jpg'))
I_gray = skim.color.rgb2gray(I)


# Déterminer si l'inversion est nécessaire (seuillage de robustesse)
LUMINOSITE_MOYENNE = I_gray.mean()
print(f"Luminosité moyenne : {LUMINOSITE_MOYENNE:.2f}")

# Inversion selon luminausite
if LUMINOSITE_MOYENNE < 0.3:
    I_inverted = 1 - I_gray
    print("Image inversée pour le traitement.")
else:
    I_inverted = I_gray
    print("Image non inversée.")

# Utiliser un seuil local
block_size = 51 
local_thresh = skim.filters.threshold_local(I_inverted, block_size, offset=0.01) 
binary = I_inverted > local_thresh

# Nettoyage
binary = skim.morphology.remove_small_objects(binary, min_size=300)

# Labeliser les régions
L, N = skim.measure.label(binary, return_num = True)
regions = skim.measure.regionprops(L)
print(f'Nombre de régions détectées: {N}')
area_L = [props.area for props in regions] 
print(area_L) 
area_L1 = [props.bbox for props in regions] 
print("BBBBOX : ", area_L1)

# Filtrer les touches par tailles 
touches = []
for prop in regions:
    minr, minc, maxr, maxc = prop.bbox
    h = maxr - minr
    w = maxc - minc
    if 15 < h < 75 and 15 < w < 200: 
        touches.append(prop)
print(f'Nombre de touches filtrées: {len(touches)}')

# calculer le centre Y de toutes les touches filtrées
centreY = np.array([(props.bbox[0] + props.bbox[2]) //2 for props in touches])
# Trouver le centre Y de la rangée principale (la rangée A/Q)
second_row_y = np.median(centreY)  

# Sélectionner les touches proches de cette rangée
row_touches = [prop for i, prop in enumerate(touches) if abs(centreY[i] - second_row_y) < 25] 

# Identifier Tab : touche la plus large ET la plus à gauche de cette rangée
tab_key_candidate = max(row_touches, key=lambda p: p.bbox[3] - p.bbox[1])

# Une touche Tab est large et a un bbox_minc très faible dans la rangée.
standard_keys_in_row = [p for p in row_touches if (p.bbox[3]-p.bbox[1]) < 50] # Largeur standard

# Après avoir identifié les touches standard dans la rangée
row_touches_sorted = sorted(standard_keys_in_row, key=lambda p: p.bbox[1])

# Identifier Touche 1 (A/Q) et Touche 2 (Z/W)
if len(row_touches_sorted) >= 2:
    Touche1_key = row_touches_sorted[0]
    Touche2_key = row_touches_sorted[1]
else:
    print("Erreur: Pas assez de touches détectées dans la rangée pour trouver la Touche 1 et Touche 2.")
    exit()

# Affichage des bboxes pour la vérification
print("Touche 1 (A/Q) bbox:", Touche1_key.bbox)
print("Touche 2 (Z/W) bbox:", Touche2_key.bbox)


# Extraire les images
def crop_touch(image, prop):
    minr, minc, maxr, maxc = prop.bbox
    return image[minr:maxr, minc:maxc]

plt.figure(figsize=(8,3))
plt.subplot(1,2,1)
plt.imshow(crop_touch(I, Touche1_key))
plt.title("Touche 1 (Q ou A)")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(crop_touch(I, Touche2_key))
plt.title("Touche 2 (W ou Z)")
plt.axis('off')

plt.show()


##########################

image_A_brute = crop_touch(I, Touche1_key)
image_Z_brute = crop_touch(I, Touche2_key)

# 2. Convertir en niveau de gris
image_A_gray = skim.color.rgb2gray(image_A_brute)
image_Z_gray = skim.color.rgb2gray(image_Z_brute)

# Définir une taille cible commune pour toutes les images de comparaison
TARGET_SIZE = (64, 64) 

# Redimensionner l'image A et Z
image_A_resized = resize(image_A_gray, TARGET_SIZE, anti_aliasing=True)
image_Z_resized = resize(image_Z_gray, TARGET_SIZE, anti_aliasing=True)

thresh_A = skim.filters.threshold_otsu(image_A_resized)
thresh_Z = skim.filters.threshold_otsu(image_Z_resized)
print(image_A_resized.mean())
if image_A_resized.mean() < 0.5:
    # Cas standard : Texte CLAIR sur fond SOMBRE (texte > seuil)
    image_A_binary = image_A_resized > 0.75
else:
    # Cas inverse : Texte SOMBRE sur fond CLAIR (texte < seuil)
    image_A_binary = image_A_resized < 0.25

# Appliquer la même logique à la Touche 2
if image_Z_resized.mean() < 0.5:
    image_Z_binary = image_Z_resized > 0.75
else:
    image_Z_binary = image_Z_resized < 0.25

if image_A_binary.mean() > 0.5:
    # Si la moyenne est élevée après seuillage, on l'inverse.
    image_A_binary = 1 - image_A_binary
    
if image_Z_binary.mean() > 0.5:
    image_Z_binary = 1 - image_Z_binary

# --- AFFICHAGE des résultats pour la vérification ---
plt.figure(figsize=(10, 4))

# Affichez A

plt.subplot(1, 2, 1)
plt.imshow(image_A_binary, cmap='gray')
plt.title("A (Binarisé)")
plt.axis('off')

# Affichez Z

plt.subplot(1, 2, 2)
plt.imshow(image_Z_binary, cmap='gray')
plt.title("Z (Binarisé)")
plt.axis('off')

plt.suptitle("Préparation des données pour la comparaison algorithmique")
plt.show()
