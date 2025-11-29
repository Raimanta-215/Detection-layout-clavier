import cv2
import numpy as np
from pathlib import Path

def ordonner_points(points: np.ndarray) -> np.ndarray:
    rectangle = np.zeros((4, 2), dtype="float32")

    somme = points.sum(axis=1)
    rectangle[0] = points[np.argmin(somme)]  # haut-gauche
    rectangle[2] = points[np.argmax(somme)]  # bas-droite

    diff = np.diff(points, axis=1)
    rectangle[1] = points[np.argmin(diff)]   # haut-droite
    rectangle[3] = points[np.argmax(diff)]   # bas-gauche

    return rectangle

def detecter_et_recadrer_clavier(image: np.ndarray) -> np.ndarray | None:
    hauteur, largeur = image.shape[:2]
    aire_image = largeur * hauteur

    # 1. Passage en niveaux de gris + réduction de bruit
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    # 2. Détection des contours
    contours_img = cv2.Canny(gris, 50, 150)

    noyau = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    contours_img = cv2.dilate(contours_img, noyau, iterations=2)
    contours_img = cv2.erode(contours_img, noyau, iterations=1)

    # 4. Recherche des contours les plus importants
    contours, _ = cv2.findContours(contours_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    meilleur_quad = None
    meilleure_aire = 0
    meilleur_rect = None 

    print(f"Nombre de contours trouvés : {len(contours)}")


    for contour in contours:
        aire = cv2.contourArea(contour)

        if aire < 0.02 * aire_image:
            continue

        perimetre = cv2.arcLength(contour, True)
        if perimetre == 0:
            continue

        approxim = cv2.approxPolyDP(contour, 0.02 * perimetre, True)
        
        if aire >= meilleure_aire:
            meilleure_aire = aire
            meilleur_rect = cv2.boundingRect(contour)

        if len(approxim) == 4 and aire > meilleure_aire:
            meilleure_aire = aire
            meilleur_quad = approxim


    if meilleur_quad is not None:
        points = meilleur_quad.reshape(4, 2).astype("float32")
        rect = ordonner_points(points)

        (hg, hd, bd, bg) = rect

        largeurA = np.linalg.norm(bd - bg)
        largeurB = np.linalg.norm(hd - hg)
        largeur_finale = int(max(largeurA, largeurB))

        hauteurA = np.linalg.norm(hd - bd)
        hauteurB = np.linalg.norm(hg - bg)
        hauteur_finale = int(max(hauteurA, hauteurB))

        destination = np.array([
            [0, 0],
            [largeur_finale - 1, 0],
            [largeur_finale - 1, hauteur_finale - 1],
            [0, hauteur_finale - 1]], dtype="float32")

        matrice = cv2.getPerspectiveTransform(rect, destination)
        clavier_recadre = cv2.warpPerspective(image, matrice, (largeur_finale, hauteur_finale))

        print("Quadrilatère trouvé → correction de perspective.")
        return clavier_recadre
    
    if meilleur_rect is not None:
        x, y, w, h = meilleur_rect
        print("Pas de quadrilatère, utilisation du rectangle englobant.")
        clavier_simple = image[y:y + h, x:x + w]
        return clavier_simple
    
    print("Aucune zone de clavier détectée.")
    return None
    
def recadrer_clavier_depuis_fichier(chemin_entree: str | Path,
                                    chemin_sortie: str | Path | None = None) -> np.ndarray | None:
    
    chemin_entree = Path(chemin_entree)
    image = cv2.imread(str(chemin_entree))

    if image is None:
        raise FileNotFoundError(f"Impossible de lire l'image : {chemin_entree}")

    clavier = detecter_et_recadrer_clavier(image)

    if clavier is not None and chemin_sortie is not None:
        chemin_sortie = Path(chemin_sortie)
        chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(chemin_sortie), clavier)

    return clavier

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Détection et recadrage de clavier")
    parser.add_argument("image", help="Chemin de l'image d'entrée")
    parser.add_argument("-o", "--sortie", help="Chemin pour sauvegarder l'image recadrée")
    args = parser.parse_args()

    resultat = recadrer_clavier_depuis_fichier(args.image, args.sortie)

    if resultat is None:
        print("Aucun clavier détecté.")
    else:
        print("Clavier recadré avec succès.")
    