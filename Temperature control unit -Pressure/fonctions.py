""" 
NOM : SINGARIN-SOLE 
DATE : 16/06/2023
OBJECTIF : Controle de température/pression
"""

#Modules nécessaires------------------------------------#
import time, random
from constantes import DURREE, PUISSANCE_CHAUFFAGE, PUISSANCE_POMPE,TEMPERATURE_DOWN, PRESSION_UP

def Controleur(T_ref : float,P_ref : float, mutex, T, P, bool_pompe, bool_chauffage,keep_running, debut ): 
    """Gère l'activation ou la désaction de la pompe et du chauffage

    Args:
        T_ref (float): température souhaitée
        P_ref (float): pression souhaitée
        mutex (): mutex
        T (): Température au cours du temps
        P (): Pression au cours du temps
        bool_pompe (): Activation/désactivation de la pompe
        bool_chauffage (): Activation/désactivation du chauffage
        keep_running (): programme en cours si True sinon a l'arret
        debut (): temps auquel le programme commence
    """

    mutex.acquire()
    while keep_running.value:
        mutex.release()
        time.sleep(0.3)
        mutex.acquire()

        if T.value > T_ref: 
            bool_chauffage.value = False
            if P.value > P_ref: 
                bool_pompe.value = True
            else: 
                bool_pompe.value = False


        elif T.value < T_ref: 
            bool_chauffage.value = True
            if P.value > P_ref: 
                bool_pompe.value = True
            else: 
                bool_pompe.value = False


        elif T.value == T_ref: 
            bool_chauffage.value = False
            if P.value > P_ref: 
                bool_pompe.value = True
            else: 
                bool_pompe.value == False


        if time.time() - debut > DURREE:
            keep_running.value = False
    mutex.release()



def variation_temperature(mutex, keep_running, T):
    """Simule une diminution de la température

    Args:
        mutex (): mutex
        keep_running (): programme en cours si True sinon a l'arret
        T (): Température au cours du temps
    """
    mutex.acquire()
    while keep_running.value:
        mutex.release()
        time.sleep(0.8)
        mutex.acquire()
        T.value -= TEMPERATURE_DOWN*random.random()
    mutex.release()

def variation_pression(mutex, keep_running,P):
    """Simule une augmentation de la pression

    Args:
        mutex (): mutex
        keep_running (): programme en cours si True sinon a l'arret
        P (): Pression au cours du temps
    """
    mutex.acquire()
    while keep_running.value:
        mutex.release()
        time.sleep(0.8)
        mutex.acquire()
        P.value += PRESSION_UP*random.random()
    mutex.release()

def Chauffer(mutex, keep_running, bool_chauffage, T):
    """Simule le fonctionnement du chauffage.
    Augmente la température lorsqu'elle est trop basse

    Args:
        mutex (): mutex
        keep_running (): programme en cours si True sinon a l'arret
        bool_chauffage (): Activation/désactivation du chauffage
        T (): Température au cours du temps 
    """
    mutex.acquire()
    while keep_running.value:
        mutex.release()
        time.sleep(0.1)
        mutex.acquire()
        if bool_chauffage.value:
            T.value += PUISSANCE_CHAUFFAGE 
    mutex.release()

def Pomper(mutex, keep_running, bool_pompe, P):
    """Simule le fonctionnement de la Pompe.
    Diminue la pression lorsqu'elle est trop haute

    Args:
        mutex (): mutex
        keep_running (): programme en cours si True sinon a l'arret
        bool_pompe (): Activation/désactivation du chauffage
        P (): Pression au cours du temps 
    """

    mutex.acquire()
    while keep_running.value:
        mutex.release()
        time.sleep(0.1)
        mutex.acquire()
        if bool_pompe.value:
            P.value -= PUISSANCE_POMPE 
    mutex.release()

def Afficher(mutex, keep_running, T, P):
    """Gère l'affichage des informations
    Args:
        mutex (): mutex
        keep_running (): programme en cours si True sinon a l'arret
        T (): Température au cours du temps 
        P (): Pression au cours du temps 
    """
    mutex.acquire()
    CL_RED="\033[22;31m"                    #  Rouge
    CL_GREEN="\033[22;32m"
    CL_RESET = "\033[0m"  
    while keep_running.value:
        mutex.release()
        time.sleep(1)
        mutex.acquire()
        print(CL_GREEN,end='')
        print("\nTempérature : " +str(T.value)+ " °C")
        print(CL_RED,end='')
        print("Pression : " +str(P.value)+ " Bar\n")
    print(CL_RESET,end='')

