import matplotlib.pyplot as plt
import numpy as np
import skimage as skim
from skimage.transform import resize


def preprocess_image(I_gray):
  LUMINOSITE_MOYENNE = I_gray.mean()
  print(f"Luminosité moyenne : {LUMINOSITE_MOYENNE:.2f}")

  # Inversion selon luminausite
  if LUMINOSITE_MOYENNE < 0.3:
      I_inverted = 1 - I_gray
      print("Image inversée pour le traitement.")
  else:
      I_inverted = I_gray
      print("Image non inversée.")

  # Binarisation avec un seuil local
  block_size = 51 
  local_thresh = skim.filters.threshold_local(I_inverted, block_size, offset=0.01) 
  binary = I_inverted > local_thresh

  # Nettoyage Dynamique
  L_initial, N_initial = skim.measure.label(binary, return_num = True)
  regions_initial = skim.measure.regionprops(L_initial)

  initial_areas = [props.area for props in regions_initial if props.area > 50] 
  if initial_areas:
      median_area = np.median(initial_areas)
      print(f"Taille médiane des régions détectées : {median_area} pixels")
      
      DYNAMIC_MIN_SIZE = int(median_area * 0.6) 
      
      if DYNAMIC_MIN_SIZE < 100: 
          DYNAMIC_MIN_SIZE = 150
  else:
      DYNAMIC_MIN_SIZE = 300 
      
  binary = skim.morphology.remove_small_objects(binary, min_size=DYNAMIC_MIN_SIZE)
  
  # Labeliser les régions
  L, N = skim.measure.label(binary, return_num = True)
  regions = skim.measure.regionprops(L)
  print(f'Nombre de régions détectées: {N}')
  return regions, binary

def filter_touches(regions):
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
  y_coords_unique = sorted(list(set(centreY)))

  # Regrouper les centres Y qui sont proches
  y_groups_centres = []
  if not y_coords_unique: return None, None
  current_group = [y_coords_unique[0]]
  for y in y_coords_unique[1:]:
    if y - current_group[-1] > 15: 
        y_groups_centres.append(np.median(current_group))
        current_group = [y]
    else:
        current_group.append(y)
  y_groups_centres.append(np.median(current_group))

  # Chercher la PREMIÈRE rangée (la plus haute) avec au moins 5 touches
  target_row_y_chiffre = None
  valid_row_count_chiffre = 0 
  if len(y_groups_centres) == 5 :
      TARGET_INDEX_chiffre = 1 
  else:
      TARGET_INDEX_chiffre = 2 
  for y_center in sorted(y_groups_centres):
      count_in_row_chiffre = sum(1 for y in centreY if abs(y - y_center) < 25)
      
      if count_in_row_chiffre >= 5: 
          valid_row_count_chiffre += 1
          
          if valid_row_count_chiffre == TARGET_INDEX_chiffre: 
              target_row_y_chiffre = y_center
              break # On a trouvé la rangée cible
  if target_row_y_chiffre is None: return None, None

  # Sélectionner les touches proches de cette rangée
  row_touches_chiffre = [prop for i, prop in enumerate(touches) if abs(centreY[i] - target_row_y_chiffre) < 25] 
  
  # --- Isolation de la Touche 2 ---
  standard_keys_chiffre = [p for p in row_touches_chiffre if (p.bbox[3]-p.bbox[1]) < 50] 
  standard_keys_chiffre_sorted = sorted(standard_keys_chiffre, key=lambda p: p.bbox[1])
  
  Touche2_key_digit = None
  if len(standard_keys_chiffre_sorted) >= 2:
      
      # L'index 2 correspond à la 3ème touche de la rangée (touche 2)
        minc_first_key = standard_keys_chiffre_sorted[0].bbox[1]
        maxc_first_key = standard_keys_chiffre_sorted[0].bbox[3]
        
        # Calculer le centre X de la première touche
        center_x_first_key = (minc_first_key + maxc_first_key) / 2
                
        # Définition de l'index à utiliser
        indexe_cible = 1 # Par défaut, on suppose que l'accent est ignoré et que le '1' est à l'index 0
                
        # Si la première touche est très proche du bord gauche (par ex. min_col < 100), 
        # on considère que l'accent grave a été inclus, et l'index 2 est le bon.
        if minc_first_key < 50: 
             indexe_cible = 2 
             print(f"Première touche très à gauche ({minc_first_key}): Index 2 utilisé.")
        else:
             indexe_cible = 1 
             print(f"Première touche décalée ({minc_first_key}): Index 1 utilisé.")


        if len(standard_keys_chiffre_sorted) > indexe_cible:
            Touche2_key_digit = standard_keys_chiffre_sorted[indexe_cible]
  # Chercher la DEUXIÈME rangée (la plus haute) qui a au moins 5 touches
  target_row_y = None
  valid_row_count = 0 
  if len(y_groups_centres) == 5 :
      TARGET_INDEX = 2 
  else:
      TARGET_INDEX = 3 
  for y_center in sorted(y_groups_centres):
      count_in_row = sum(1 for y in centreY if abs(y - y_center) < 25)
      
      if count_in_row >= 5: 
          valid_row_count += 1
          
          if valid_row_count == TARGET_INDEX: 
              target_row_y = y_center
              break # On a trouvé la rangée cible
  if target_row_y is None: return None, None

  # Sélectionner les touches proches de cette rangée
  row_touches = [prop for i, prop in enumerate(touches) if abs(centreY[i] - target_row_y) < 25] 
  
  return row_touches, row_touches_chiffre, Touche2_key_digit

def identify_A_Z_keys(row_touches):
  if row_touches is None: return None, None
  
  standard_keys_in_row = [p for p in row_touches if (p.bbox[3]-p.bbox[1]) < 50] 

  #Trie de gauche à droite
  row_touches_sorted = sorted(standard_keys_in_row, key=lambda p: p.bbox[1])
  if len(row_touches_sorted) >= 2:
    return row_touches_sorted[0], row_touches_sorted[1]
      
  return None, None

def crop_and_process(image, prop):
  minr, minc, maxr, maxc = prop.bbox
  img_brute = image[minr:maxr, minc:maxc]
  img_gray = skim.color.rgb2gray(img_brute)
  img_resized = resize(img_gray, (64, 64), anti_aliasing=True)
  
  # Logique de seuillage de caractère
  if img_resized.mean() < 0.5:
      img_binary = img_resized > 0.75
  else:
      img_binary = img_resized < 0.25
      
  if img_binary.mean() > 0.5:
      img_binary = 1 - img_binary
  return img_binary

######SCRIPT
I = skim.img_as_float(plt.imread('img/Querty_UK.jpg'))
I_gray = skim.color.rgb2gray(I)

# 1. Prétraitement et Nettoyage
regions, binary = preprocess_image(I_gray)
print(f'Régions détectées: {len(regions)}')

# 2. Ciblage de la rangée (retourne les touches de la rangée)
row_touches_lettre, _, Touche2_key_digit = filter_touches(regions)

# 3. Identification des touches
Touche1_key, Touche2_key = identify_A_Z_keys(row_touches_lettre)

if Touche1_key is None or Touche2_key is None:
    print("Erreur: Impossible d'identifier la Touche 1 ou la Touche 2.")
    exit()


# --- AFFICHAGE des résultats ---
""" 
plt.figure(figsize=(12,3))
plt.subplot(1,3,1)
plt.imshow(crop_and_process(I, Touche1_key), cmap='gray')
plt.title("Touche 1 (Q ou A)")
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(crop_and_process(I, Touche2_key), cmap='gray')
plt.title("Touche 2 (W ou Z)")
plt.axis('off')

plt.subplot(1,3,3)
plt.imshow(crop_and_process(I, Touche2_key_digit), cmap='gray')
plt.title("Touche Chiffre 2")
plt.axis('off')

plt.show()
"""

