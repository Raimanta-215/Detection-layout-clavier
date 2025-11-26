import matplotlib.pyplot as plt
import numpy as np
import skimage as skim
from skimage.transform import resize

#Lire l'image et mettre en niveau de gris
I = skim.img_as_float(plt.imread('img/AZERTY_francais.jpg'))
#I = skim.img_as_float(plt.imread('img/Querty.jpg'))

I_gray = skim.color.rgb2gray(I)


#Binarisation et nettoyage
binary = I_gray > skim.filters.threshold_otsu(I_gray)
binary = skim.morphology.remove_small_objects(binary, min_size=300)
#binary = skim.morphology.binary_closing(binary, skim.morphology.square(5))


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
    if 20 < h < 60 and 20 < w < 150:
      touches.append(prop)
print(f'Nombre de touches filtrées: {len(touches)}')

#calculer le centre Y
centreY = np.array([(props.bbox[0] + props.bbox[2]) //2 for props in touches])
print("Y centers: ", centreY)
second_row_y = np.median(centreY)  

# Sélectionner les touches proches de cette rangée
row_touches = [prop for i, prop in enumerate(touches) if abs(centreY[i] - second_row_y) < 10]

# Identifier Tab : touche la plus large
tab_key = max(row_touches, key=lambda p: p.bbox[3]-p.bbox[1])

# Trier par position X (minc)
row_touches_sorted = sorted([p for p in row_touches if p != tab_key], key=lambda p: p.bbox[1])

# Identifier Tab, A, Z
A_key = row_touches_sorted[0]
Z_key = row_touches_sorted[1]

print("Tab bbox:", tab_key.bbox)
print("A bbox:", A_key.bbox)
print("Z bbox:", Z_key.bbox)

# Extraire les images
def crop_touch(image, prop):
    minr, minc, maxr, maxc = prop.bbox
    return image[minr:maxr, minc:maxc]
# plt.figure(figsize=(15, 6))
# for i, prop in enumerate(touches):
#     plt.subplot(int(np.ceil(len(touches)/15)), 15, i+1) 
#     plt.imshow(crop_touch(I, prop))
#     plt.axis('off')
# plt.show()


plt.figure(figsize=(8,3))
plt.subplot(1,3,1)
plt.imshow(crop_touch(I, tab_key))
plt.title("Tab")
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(crop_touch(I, A_key))
plt.title("A")
plt.axis('off')

plt.subplot(1,3,3)
plt.imshow(crop_touch(I, Z_key))
plt.title("Z")
plt.axis('off')

plt.show()




##################

image_A_brute = crop_touch(I, A_key)
image_Z_brute = crop_touch(I, Z_key)

# 2. Convertir en niveau de gris
image_A_gray = skim.color.rgb2gray(image_A_brute)
image_Z_gray = skim.color.rgb2gray(image_Z_brute)

# Définir une taille cible commune pour toutes les images de comparaison
TARGET_SIZE = (64, 64) 

# Redimensionner l'image A et Z
image_A_resized = resize(image_A_gray, TARGET_SIZE, anti_aliasing=True)
image_Z_resized = resize(image_Z_gray, TARGET_SIZE, anti_aliasing=True)

# Binariser l'image A et Z
thresh_A = skim.filters.threshold_otsu(image_A_resized)
image_A_binary = image_A_resized > thresh_A

thresh_Z = skim.filters.threshold_otsu(image_Z_resized)
image_Z_binary = image_Z_resized > thresh_Z


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
