from pathlib import Path
import cv2
from src.traitement_image.recadrage_clavier import recadrer_clavier_depuis_fichier


def traiter_image_fichier(chemin_entree, chemin_sortie):
    """
    Fonction appelée par Flask.
    chemin_entree : image uploadée par l'utilisateur (input.jpg)
    chemin_sortie : image processed.jpg
    Retourne :
        - un booléen True/False
        - un message texte
    """

    chemin_entree = Path(chemin_entree)
    chemin_sortie = Path(chemin_sortie)

    # Lecture de l'image
    image_originale = cv2.imread(str(chemin_entree))

    if image_originale is None:
        return False, "Impossible de lire l'image."

    # Appel du CODE
    clavier = recadrer_clavier_depuis_fichier(
        chemin_entree,
        chemin_sortie
    )

    if clavier is None:
        return False, "Aucun clavier détecté."

    # Succès
    return True, "Clavier détecté et recadrage !"