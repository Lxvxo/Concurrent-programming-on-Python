""" 
NOM : SINGARIN-SOLE 
DATE : 12/06/2023
OBJECTIF : FONCTIONS UTILES AU PROGRAMME RESTAURANT
"""

def search_zero(L : list):
    """Retourne le premier le zéro de la liste sinon renvoie la longueur de la liste

    Args:
        L (list): liste à étudier

    Returns:
        int : indice de la première occurence du zéro
    """
    n = len(L)
    for i, elt in enumerate(L):
        if elt == 0:
            n = i
            break
    return n

def array_to_list(tab):
    """Convertit un tableau en 2D en un tableau à 1D par rapport à une des deux variables
    Args:
        tab (list): tableau en deux dimensions 

    Returns:
        list : liste d'éléments
    """
    list_ = []
    for i, elt in enumerate(tab):
        list_.append(elt)
    return list_

# Fonction qui 
def update_list(L : list):
    """
    Décale les éléments de la liste vers la gauche et insère un 0 si la liste est vide
    Args:
        L (list): liste d'éléments

    Returns:
        list: liste décalée
    """
    for i in range (len(L)-1):
        L[i] = L[i+1]
    L[len(L)-1] = 0
    return L

def reset_list(L : list):
    """Met tous les éléments de la liste à la valeur 0.

    Args:
        L (list): liste d'éléments

    Returns:
        list: liste contenant des zéros
    """
    for i in range (len(L)):
        L[i] = 0
    return L
