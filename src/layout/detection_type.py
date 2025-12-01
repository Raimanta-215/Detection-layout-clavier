from layout.identifier_touche import identifier_une_touche
from traitement_image.detectionTouche import detec_key_image



def classification (t1 , t2):



    premiere_touche = t1
    deuxieme_touche = t2

    premiere_lettre = identifier_une_touche(premiere_touche)
    deuxieme_lettre = identifier_une_touche(deuxieme_touche)



    match (premiere_lettre, deuxieme_lettre):
            case ('A', 'Z'):
                return "AZERTY"
            case ('Q', 'W'):
                return "QWERTY"
            case ('A', _): 
                return "AZERTY"
            case ('Q', _):
                return "QWERTY" 
            case (_, 'Z'):
                return "AZERTY" 
            case (_, 'W'):
                return "QWERTY" 
            case _:
                return "Inconnu"

    





