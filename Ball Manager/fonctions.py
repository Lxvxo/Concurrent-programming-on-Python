""" 
NOM : SINGARIN-SOLE 
DATE : 10/06/2023
OBJECTIF :Gestion des billes 
"""

#Modules nécessaires------------------------------------#
import time
from constantes import NB_PROCESS

def demander(billes_process, mutex, Sem, nbr_disponible_billes,numero):
    """ Cette fonction permet au processus appelé de faire une demande d'un nombre 
    de billes qui se bloque si le nombre de billes disponibles est plus faible 
    que le nombre de billes demandées

    Args:
        billes_process (int): nombre de billes demandées par le processus
        mutex (): mutex
        Sem (): sémaphore
        nbr_disponible_billes (): nombre de billes disponibles
        numero (int) : numero du processus
    """
    mutex.acquire()
    while nbr_disponible_billes  .value <= billes_process:
        print(numero," : ","J'attends, je demande " +str(billes_process)+ " billes\n")
        mutex.release()
        Sem.acquire()
        mutex.acquire()
        

    print(numero," : ""C'est bon j'ai " +str(billes_process)+ " billes\n" )
    nbr_disponible_billes  .value -= billes_process
    mutex.release()
    Sem.release()
    

def rendre(billes_process, mutex, nbr_disponible_billes):
    """Cette fonction permet de rendre les ressources en fonction du nombre de billes qui est demandé

    Args:
        billes_process (int): nombre de billes rendues par le processus
        mutex (): mutex
        nbr_disponible_billes (): nombre de billes demandés
        numero (int) : numero du processus
    """
    mutex.acquire()
    nbr_disponible_billes  .value += billes_process
    mutex.release()

def travailleur(billes_process, mutex, Control, Sem, nbr_disponible_billes, numero):
    """Cette fonction annonce la séquence: "demander des billes, utiliser les billes, 
    rendre les billes" pour chaque processus appelé

    Args:
        billes_process (int): billes demandées par le processus
        mutex (): mutex
        Control (): variable partagée définissant le nombre de process ayant terminé avec leur travail
        Sem (): semaphore
        nbr_disponible_billes (): nombre de billes disponibles
        numero (int) : numero du processus
    """
    # 
    demander(billes_process,mutex, Sem, nbr_disponible_billes, numero)
    time.sleep(billes_process)
    rendre(billes_process, mutex, nbr_disponible_billes)
    
    mutex.acquire()
    Control.value += 1
    mutex.release()
    print(numero," : ""J'avais besoin de " +str(billes_process)+ " billes, j'ai fini\n")

def controleur(mutex, nbr_disponible_billes, Control):
    """Cette fonction permet de vérifier en permanence si le nombre 
    de billes disponible est dans l'intervalle

    Args:
        mutex (): _description_
        nbr_disponible_billes (): nombres de billes disponibles
        Control (): variable partagée définissant le nombre de process ayant terminé avec leur travail
    """
    controle = 0
    while controle < NB_PROCESS:
        time.sleep(0.5)
        mutex.acquire()
        print("Controleur : ", "Il y a " + str(nbr_disponible_billes  .value) + " billes disponibles\n")
        mutex.release()
        mutex.acquire()
        controle = Control.value
        print(controle)
        mutex.release()
    print("\nTout le monde a terminé !!!")
