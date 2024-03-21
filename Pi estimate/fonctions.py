""" 
NOM : SINGARIN-SOLE 
DATE : 05/06/2023
OBJECTIF : Algorithme d'estimation de pi par la méthode arc tangente
Chaque process va calculer une somme de même taille et l'ajouter dans la variable pi
"""

def arc_tangente(NB_ITERATION : int , range : list ,pi, mutex):
    """Réalise une approxamation de pi en divisant des les calculs entre les processus

    Args:
        NB_ITERATION (int): nombre d'itération totale
        range (_type_): intervalle de calcul du processus
        pi (float): valeur approchée de pi
        mutex (sem): exclusion mutuelle
    """
    for i in range:
        mutex.acquire()
        pi.value += (4/(1+((i+0.5)/NB_ITERATION)**2))/NB_ITERATION
        mutex.release()
