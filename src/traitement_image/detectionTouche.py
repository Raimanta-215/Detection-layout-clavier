import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.filters import sobel, threshold_otsu
from skimage import img_as_float
from skimage.measure import label, regionprops

#Lire l'image.
I = img_as_float(plt.imread('img/AZERTY_francais.jpg'))
h, w, _ = I.shape

#Redimensionner toutes les images à une taille fixe.
print(I.shape)
I_redim = I[0:int(0.7*h), 0:int(0.25*w)]
plt.imshow(I_redim, interpolation='bilinear', cmap='gray')
plt.show()
#Convertir en niveaux de gris.
I_gray = rgb2gray(I_redim)

#Découper la zone contenant la rangée des lettres (coordonnées fixes).
rows, cols = I_gray.shape
print(I_gray.shape)

I_ligne = I_gray[int(0.5*rows):int(0.72*rows), 0:int(0.6*cols)]
plt.imshow(I_ligne, interpolation='nearest', cmap='gray')
plt.show()
#Appliquer Sobel pour faire ressortir les bords.

edges = sobel(I_ligne)
plt.imshow(edges, interpolation='nearest', cmap='gray')
plt.show()

#Découper les sous-zones correspondant aux touches A et Z.

seuil = threshold_otsu(edges)
binary = edges > seuil
plt.imshow(binary, cmap='gray')
plt.show()

labels = label(binary)
props = regionprops(labels)
print(f'Nombre de régions détectées: {len(props)}')
touches = []

for prop in (props):
    minr, minc, maxr, maxc = prop.bbox
    if 57 < prop.area < 70:
      touche = I_ligne[minr:maxr, minc:maxc]

      touches.append(prop)

props_sorted = sorted(touches, key=lambda p: p.bbox[1])
lettre1 = props_sorted[0]   
lettre2 = props_sorted[1]

minr, minc, maxr, maxc = lettre1.bbox
lettre1_zone = I_ligne[minr:maxr, minc:maxc]

minr, minc, maxr, maxc = lettre2.bbox
lettre2_zone = I_ligne[minr:maxr, minc:maxc]
print(lettre1_zone.shape)

plt.imshow(lettre1_zone, cmap='gray'); plt.title("Touche A"); plt.show()
plt.imshow(lettre2_zone, cmap='gray'); plt.title("Touche Z"); plt.show()

