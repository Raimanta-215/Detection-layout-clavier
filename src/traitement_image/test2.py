import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage import img_as_float
from skimage.measure import label, regionprops
from skimage.feature import canny

#Lire l'image.
I = img_as_float(plt.imread('img/AZERTY_francais.jpg'))
h, w, _ = I.shape

#Convertir en niveaux de gris.
I_gray = rgb2gray(I)

#Detection des coutours avec canny
edges = canny(I_gray, sigma=3)
plt.imshow(edges, interpolation='nearest', cmap='gray')
plt.show()

#Fermeture des contours (dilatation)
from skimage.morphology import dilation, square, binary_closing
closed_edges = dilation(edges, square(3))
closed_edges = binary_closing(closed_edges, square(5))
plt.imshow(closed_edges, interpolation='nearest', cmap='gray')
plt.show()

#Retirer petits objets parasites
from skimage.morphology import remove_small_objects
cleaned = remove_small_objects(closed_edges, min_size=150)
plt.imshow(cleaned, interpolation='nearest', cmap='gray')
plt.show()

#Labelisation 
labels = label(cleaned)
props = regionprops(labels)
print(f'Nombre de régions détectées: {len(props)}')
# Extraction des touches 
touches = []
for prop in (props):
    minr, minc, maxr, maxc = prop.bbox
    h = maxr - minr
    w = maxc - minc
    if 25 < h < 500 and 20 < w < 500:
      touches.append(prop)
      #touche = I_gray[minr:maxr, minc:maxc]
      #plt.imshow(touche, interpolation='nearest', cmap='gray')
      #plt.show()


# Trouver la touche Tab
tab_key = max(props, key=lambda p: p.bbox[3] - p.bbox[1])
tab_minr, tab_minc, tab_maxr, tab_maxc = tab_key.bbox
tab_row_center = (tab_minr + tab_maxr) // 2


# Trouver les touches de toute la rangée
same_row = []
for prop in (props):
    minr, minc, maxr, maxc = prop.bbox
    row_center = (minr + maxr) // 2
    if abs(row_center - tab_row_center) < 20:  # Tolérance de 20 pixels
        same_row.append(prop)

# Tri des touches par position horizontale
props_sorted = sorted(same_row, key=lambda p: p.bbox[1])

#Extraire les 2 touches après la touche Tab (A et Z)
lettre1 = props_sorted[0]   
lettre2 = props_sorted[1]

minr, minc, maxr, maxc = lettre1.bbox
lettre1_zone = I_gray[minr:maxr, minc:maxc]

minr, minc, maxr, maxc = lettre2.bbox
lettre2_zone = I_gray[minr:maxr, minc:maxc]
print(lettre1_zone.shape)

#Affichage des touches A et Z
plt.imshow(lettre1_zone, cmap='gray'); plt.title("Touche A"); plt.show()
plt.imshow(lettre2_zone, cmap='gray'); plt.title("Touche Z"); plt.show()