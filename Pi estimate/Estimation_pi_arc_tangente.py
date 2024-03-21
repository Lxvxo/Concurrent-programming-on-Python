""" 
NOM : SINGARIN-SOLE 
DATE : 05/06/2023
OBJECTIF : Algorithme d'estimation de pi par la méthode arc tangente
Chaque process va calculer une somme de même taille et l'ajouter dans la variable pi
"""
#Modules nécessaires------------------------------------#
import multiprocessing as mp
import time
from fonctions import arc_tangente
from constantes import NB_PROCESS, NB_ITERATION

if __name__ == "__main__":
    DEBUT = time.time() 
    # On divise le nombre d'itération par le nombre de process pour l'approximation de pi
    iteration_process = int(NB_ITERATION/NB_PROCESS)
    listProcess = []
    mutex = mp.Lock()
    pi = mp.Value('f', 0)

    print("Temps d'éxecution: ", time.time() - DEBUT)

    # Génération des processus
    for i in range (NB_PROCESS):
        intervalle = [k for k in range(i*iteration_process, iteration_process*(i+1))]
        process = mp.Process(target = arc_tangente, args = (NB_ITERATION, intervalle,pi, mutex))
        listProcess.append(process)
        process.start()

    for p in listProcess:
        p.join()

    print("Valeur de pi :", pi.value)