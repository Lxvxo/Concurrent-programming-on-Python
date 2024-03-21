""" 
NOM : SINGARIN-SOLE 
DATE : 
OBJECTIF : Merge sort version 2 en utilisant des processus mais sans succes 
"""
import multiprocessing as mp
import random, time
from array import array


def search_zero(L : list):
    """Retourne le premier le zéro de la liste sinon renvoie la longueur de la liste

    Args:
        L (list): liste à étudier

    Returns:
        int : indice de la première occurence du zéro
    """
    n = len(L)
    k = 0
    for elt in L:
        
        if elt == 0:
            n = k
            break
        k +=1
    return n
def merge(list_tranche, N,k,Tab_triee):
    #tableau = array('i', [])  # tableau vide qui reçoit les résultats
    #mutex.acquire()
    while condition_liste_tranches(list_tranche):
        minimum = N+1
        indice = -1
        for k in range(len(list_tranche)) :
            if len(list_tranche[k]) > 0 :
                if minimum > list_tranche[k][0] :
                    minimum = list_tranche[k][0]
                    indice = k
        index = search_zero(Tab_triee)
        Tab_triee[index] = list_tranche[indice].pop(0)

    for h in range(len(list_tranche)) :
        index = search_zero(Tab_triee)
        if len(list_tranche[h]) != 0:
            Tab_triee[index] = list_tranche[h].pop(0)  
    #mutex.release()
    return print("Process ",k," terminé...")

def tri_global(list_tranche,N,Tableau):
    while condition_liste_tranches(list_tranche):
        minimum = N+1
        indice = -1
        for k in range(len(list_tranche)) :
            if len(list_tranche[k]) > 0 :
                if minimum > list_tranche[k][0] :
                    minimum = list_tranche[k][0]
                    indice = k
        index = search_zero(Tableau)
        Tableau[index] = list_tranche[indice].pop(0)

    for h in range(len(list_tranche)) :
        index = search_zero(Tableau)
        if len(list_tranche[h]) != 0:
            Tableau[index] = list_tranche[h].pop(0)  
    return 
def condition_liste_tranches(list_tranche):
    n = 0
    for tranche in list_tranche:
        if len(tranche) > 0 :
            n+=1
    if n >= 2 :
        return True
    else :
        return False
    
def merge_sort(Tableau, nb_tranches, N,kk,Tab_triee):
    
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

    
    print("\n",list_tranches," ",kk,"\n")
    for k in range(len(list_tranches)) :
        list_tranches[k] = merge_sort(list_tranches[k] , nb_tranches, N,kk,Tab_triee)
     

    return merge(list_tranches, N,kk,Tab_triee)


def version_de_base(N,nb_tranches):
    NB_PROCESS = 4
    Tab = array('i', [random.randint(0,N) for _ in range(N)]) 
    
    print("Avant : ", Tab)
    start = time.time()
    
    list_tranches = []
    separer = len(Tab) // NB_PROCESS

    for i in range(NB_PROCESS-1):
        tranche = Tab[separer*i:separer*(i+1)]
        list_tranches.append(tranche)

    n = separer*(NB_PROCESS-1)
    list_tranches.append(Tab[n:len(Tab)])
    list_process = [] 
    list_tab_triee = []
    for k in range(NB_PROCESS) :
        Tab_triee = mp.Array("i",[0]*N)
        list_tab_triee.append(Tab_triee)
        process = mp.Process(target = merge_sort, args = (list_tranches[k] , nb_tranches, N,k+1,Tab_triee))
        list_process.append(process)

    print(list_tab_triee)
    return "\n \n Etape 1 fini"
    for process in list_process :
        process.start()
    for process in list_process :
        process.join()
    Tab_final = array("i",[])
    process_final = mp.Process(target = tri_global, args=(list_tab_triee,N,Tab_final))
    process_final.start()
    process.join()

    end = time.time()

    print("Après : ", Tab_final)
    print("Le temps avec ",NB_PROCESS," seul Process = %f pour un tableau de %d éléments " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end = '')
    try :
        assert(all([(Tab_final[i] <= Tab_final[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")

if __name__ == "__main__" :
    version_de_base(10,3)