""" 
NOM : SINGARIN-SOLE 
DATE : 10/06/2023
OBJECTIF :Gestion des billes 
"""

#Modules nécessaires------------------------------------#
import multiprocessing as mp
from fonctions import travailleur, controleur
from constantes import MAX_BILLES, NB_PROCESS

if __name__=='__main__':
    # Initialisation des différentes variables qui seront appelés dans les différentes fonctions codées plus haut
    Sem = mp.Semaphore(0)
    mutex = mp.Lock()
    nbr_disponible_billes   = mp.Value('i', MAX_BILLES)
    Control = mp.Value('i', 0)
    billes_process = []
    for i in range(NB_PROCESS):
        valeur = int(input(f"Saisissez le nombre de billes que veut le processus {i+1} : "))
        while valeur > nbr_disponible_billes.value:
            print("La valeur doit être inférieure ou égale à .",MAX_BILLES)
            valeur = int(input(f"Saisissez une nouvelle valeur de k pour le processus {i+1} : "))
        billes_process.append(valeur)

    # Initialisation des Processus
    C = mp.Process(target = controleur, args = (mutex, nbr_disponible_billes, Control))
    list_process = [C]
    for i in range(NB_PROCESS) : 
        process = mp.Process(target = travailleur, args = (billes_process[i],mutex, Control,Sem, nbr_disponible_billes, i))
        list_process.append(process)
    
    
    for process in list_process : process.start()

    for process in list_process : process.join()


