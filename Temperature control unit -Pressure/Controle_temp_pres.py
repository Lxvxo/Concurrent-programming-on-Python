""" 
NOM : SINGARIN-SOLE 
DATE : 16/06/2023
OBJECTIF : Controle de température/pression
"""

#Modules nécessaires------------------------------------#
import ctypes
import multiprocessing as mp
from fonctions import Controleur, Chauffer, Pomper, variation_pression,variation_temperature,Afficher
from constantes import T_int, P_int
import time

# Programme principale
if __name__=='__main__':

    # Initialisation du mutex
    mutex = mp.Lock()

    # Initialisation des variable partagées
    T = mp.Value('f', T_int) # Température au cours du temps
    P = mp.Value('f', P_int) # Pression au cours du temps
    bool_pompe = mp.Value(ctypes.c_bool, False) # Activation/désactivation de la pompe
    bool_chauffage = mp.Value(ctypes.c_bool, False) # Activation/désactivation du chauffage
    keep_running = mp.Value(ctypes.c_bool, True) # programme en cours si True sinon a l'arret
    debut = time.time()
    # Choix des paramètres
    T_ref = float(input("Température souhaitée :\n"))
    P_ref = float(input("Pression souhaitée :\n"))

    # Initialisation des processus
    controleur_ = mp.Process(target = Controleur, args = (T_ref, P_ref,mutex, T, P, bool_pompe, bool_chauffage,keep_running,debut)) 
    move_temperature = mp.Process(target = variation_temperature, args = (mutex, keep_running, T)) 
    move_pression = mp.Process(target = variation_pression, args = (mutex,keep_running, P)) 
    chauffage = mp.Process(target = Chauffer, args = (mutex, keep_running, bool_chauffage, T)) 
    pompe = mp.Process(target = Pomper, args = (mutex, keep_running, bool_pompe, P)) 
    affichage = mp.Process(target = Afficher, args = (mutex, keep_running, T, P)) 

    list_process = [controleur_, move_temperature, move_pression, chauffage, pompe, affichage]
    
    for process in list_process :
        process.start()

    for process in list_process:
        process.join()