""" 
NOM : SINGARIN-SOLE 
DATE : 05/06/2023
OBJECTIF : Simuler une course hippique avec arbitre 
"""
#Modules nécessaires------------------------------------#
import multiprocessing as mp
import ctypes
from constantes import NBPROCESS
from fonctions import course_hippique


# ---------------------------------------------------
# Programme principale :
if __name__ == "__main__" :
         
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)

    mutex = mp.Lock()  # exclusion mutuelle 
    keep_running=mp.Value(ctypes.c_bool, True)

    tableau = mp.Array("i",[0]*NBPROCESS)

    pari = input("Parier sur un cheval entre A et T : \n") # permet au joueur de parier en début de partie
    course_hippique(keep_running,tableau,pari, mutex)
    
 
