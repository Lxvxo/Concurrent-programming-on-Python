""" 
NOM : SINGARIN-SOLE 
DATE : 17/06/2023
OBJECTIF : Merge sort version 1 en décomposant par tranche sans utiliser plusieurs process
"""
import  random, time
from array import array

def merge(list_tranche, N):
    print("1fois \n")
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
    print(tableau)
    return tableau

def condition_liste_tranches(list_tranche):
    n = 0
    for tranche in list_tranche:
        if len(tranche) > 0 :
            n+=1
    if n >= 2 :
        return True
    else :
        return False
    
def merge_sort(Tableau, nb_tranches, N):
    
    length_Tableau = len(Tableau)
    if length_Tableau < nb_tranches :
        nb_tranches = length_Tableau
    if length_Tableau <= 1: 
        return Tableau
    separer = length_Tableau // nb_tranches
    list_tranches = []
    for i in range(nb_tranches-1):
        tranche = Tableau[separer*i:separer*(i+1)]
        list_tranches.append(tranche)

    n = separer*(nb_tranches-1)
    list_tranches.append(Tableau[n:len(Tableau)])   
    
    for k in range(len(list_tranches)) :
        list_tranches[k] = merge_sort(list_tranches[k] , nb_tranches, N)
    return merge(list_tranches, N)


def version_de_base(N,nb_tranches):
    Tab = array('i', [random.randint(0,N) for _ in range(N)]) 
    print("Avant : ", Tab)
    start = time.time()
    Tab = merge_sort(Tab, nb_tranches, N)
    end = time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d éléments " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end = '')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")

if __name__ == "__main__" :
    version_de_base(100,7)