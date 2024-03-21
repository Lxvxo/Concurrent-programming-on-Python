""" 
NOM : SINGARIN-SOLE 
DATE : 17/06/2023
OBJECTIF : Merge sort version finale
"""

#Modules nécessaires------------------------------------#
import random, time
from array import array
import multiprocessing as mp

def merge(list_tranche: list, N : int):
    """S'utilise avec merge_sort pour trier des listes en les séparant par tranches

    Args:
        list_tranche (list): liste contenant les tranches
        N (int): valeur maximal qu'un nombre de la liste peut prendre

    Returns:
        list: list triée
    """
    tableau = array('i', [])  # tableau vide qui reçoit les résultats
    while condition_liste_tranches(list_tranche):
        minimum = N+1
        indice = -1
        for k in range(len(list_tranche)) :
            if len(list_tranche[k]) > 0 :
                if minimum > list_tranche[k][0] :
                    minimum = list_tranche[k][0]
                    indice = k
        tableau.append(list_tranche[indice].pop(0))

    for tranche in list_tranche :
        tableau += tranche    
    return tableau

def condition_liste_tranches(list_tranche : list):
    """Gère les conditions nécessaires pour que la boucle dans merge s'effectue 
    En effet, il faut qu'il reste au maximum deux listes non vides

    Args:
        list_tranche (list): liste des tranches

    Returns:
        bool: True ou False
    """
    n = 0
    for tranche in list_tranche:
        if len(tranche) > 0 :
            n+=1
    if n >= 2 :
        return True
    else :
        return False
    
def merge_sort(Tableau: list, nb_tranches : int, N : int ,send_end=None):
    """_summary_

    Args:
        Tableau (list): liste des valeurs initiales 
        nb_tranches (int): nombre de tranches choisies pour séparer la liste
        N (int): valeur maximal qu'un nombre de la liste peut prendre
        send_end (, optional): . envoi dans le pipe.

    Returns:
        : tableau triée
    """
    
    length_Tableau = len(Tableau)

    if length_Tableau < nb_tranches :
        nb_tranches = length_Tableau
    if length_Tableau <= 1: 
        result = Tableau
    else : 
        separer = length_Tableau // nb_tranches
        list_tranches = []
        for i in range(nb_tranches-1):
            tranche = Tableau[separer*i:separer*(i+1)]
            list_tranches.append(tranche)

        n = separer*(nb_tranches-1)
        list_tranches.append(Tableau[n:len(Tableau)])  

        
        pipes = [mp.Pipe(False) for tranche in list_tranches]

        processes = [mp.Process(target=merge_sort, args=(tranche, nb_tranches, N, send_end))
                    for tranche, (recv_end, send_end) in zip(list_tranches, pipes)]
        for process in processes: process.start()
        for process in processes: process.join()
        results = [recv_end.recv() for recv_end, send_end in pipes]

        result = merge(results,N)
 
    if send_end:
        send_end.send(result)
    else:
        return result


def version_finale(N,nb_tranches):
    Tab = array('i', [random.randint(0,N) for _ in range(N)]) 
    print("Avant : ", Tab)
    start = time.time()
    Tab = merge_sort(Tab, nb_tranches, N)
    end = time.time()
    print("Après : ", Tab)
    print("Le temps avec plusieurs Process = %f pour un tableau de %d éléments " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end = '')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")
