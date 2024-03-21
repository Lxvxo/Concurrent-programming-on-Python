""" 
NOM : SINGARIN-SOLE 
DATE : 12/06/2023
OBJECTIF : Simule un restaurant
"""
#Modules nécessaires------------------------------------#
import multiprocessing as mp
import time, random, ctypes
from fonctions import update_list, reset_list, array_to_list, search_zero
from constantes import PLATS, TAILLE_TAMPON, NB_SERVEUR, DURREE


def Serveur (keep_running : bool ,num_serveur : int, tampon : list, serveur_en_cours : list , service : list):
    """Initialise et simule le comportement d'un serveur

    Args:
        keep_running (bool)
        num_serveur (int): numéro propre au serveur
        tampon (list): liste contenant les commandes de chaques clients ainsi que leur numéros 
        serveur_en_cours (list): liste contenant les numéros des serveurs les commandes en cours de traitement
        service (list): liste associé aux numéro de chaque serveur, si le serveur a fini il affiche 1 sinon il affiche 0.
    """
    while keep_running:
        sem_tampon.acquire()
        mutex.acquire()
        num_client = tampon[1][0]
        lettre_commande = tampon[0][0]

        if num_client != 0 :
            tampon[0] = update_list(tampon[0])
            tampon[1] = update_list(tampon[1])
        
        mutex.release()
        sem_tampon.release()

        if num_client == 0 :
            time.sleep(0.8) 
        else:
            sem_serveur.acquire()
            serveur_en_cours[0][num_serveur] = lettre_commande
            serveur_en_cours[1][num_serveur] = num_client
            sem_serveur.release()

            time.sleep(random.randint(2, 8)) # temps de préparation de la commande

            sem_serveur.acquire()
            serveur_en_cours[0][num_serveur] = 0
            serveur_en_cours[1][num_serveur] = 0
            service[num_serveur] = 1
            sem_serveur.release()
            
def Clients(keep_running : bool ,tampon : list, TAILLE_TAMPON : int):
    """Initialise un nouveau client 

    Args:
        keep_running (bool)
        tampon (list): liste contenant les commandes de chaques clients ainsi que leur numéros
        TAILLE_TAMPON (int): taille du tampon
    """
    while keep_running:
        sem_tampon.acquire()
        indice = search_zero(tampon[1]) # trouve le premier zero de la liste

        if indice <= TAILLE_TAMPON - 1:
            lettre_commande = random.randint(1,len(PLATS)-1) #choix aléatoire de la commande
            if len(tampon[1]) == 0 :
                num_client = 0
            else : 
                num_client = tampon[1][indice-1] + 1 #permet à tous les clients d'avoir un numéros differents

            tampon[0][indice] = lettre_commande
            tampon[1][indice] = num_client
        
        sem_tampon.release()
        time.sleep(1)

def major_dHomme (keep_running : bool ,DEBUT, tampon : list, serveur_en_cours : list, service : list):
    """Gestion de l'affichage des informations sur l'écran

    Args:
        keep_running (bool)
        DEBUT() : temps de début du service
        tampon (list): liste contenant les commandes de chaques clients ainsi que leur numéros
        serveur_en_cours (list): liste contenant les numéros des serveurs les commandes en cours de traitement
        service (list): liste associé aux numéro de chaque serveur, si le serveur a fini il affiche 1 sinon il affiche 0.
    """
    CL_RED="\033[22;31m"                    #  Rouge
    CL_GREEN="\033[22;32m"                  #  Vert
    CL_BROWN = "\033[22;33m"                #  Brun
    CL_BLUE="\033[22;34m"                   #  Bleu
    CL_GRAY="\033[22;37m"                   #  Gris
    
    while keep_running:
        sem_serveur.acquire()
        sem_tampon.acquire()
        mutex.acquire()

        tampon_plats = array_to_list(tampon[0])
        for i in range(len(tampon_plats)):
            tampon_plats[i] = PLATS[tampon_plats[i]] # tampon_plats stocke les differents plats

        tampon_numero = array_to_list(tampon[1]) #stocke les numéro des clients

        serveur_plats = array_to_list(serveur_en_cours[0])
        for i in range(len(serveur_plats)):
            serveur_plats[i] = PLATS[serveur_plats[i]] # stocke les commandes en cours

        serveur_numero = array_to_list(serveur_en_cours[1]) #stocke les numéro des serveur en cours 

        service_en_cours = array_to_list(service)

        service = reset_list(service)

        sem_serveur.release()
        sem_tampon.release()
        mutex.release()

        for i in range(NB_SERVEUR):
            if serveur_numero[i] == 0:
                print(CL_RED,end='')
                print(f"Le serveur {i+1} prépare déja une commande\n")
            else:
                print(CL_BLUE,end='')
                print(f"Le serveur {i+1} prépare la commande {(serveur_plats[i],serveur_numero[i])}\n")
        
        NB_commandes = search_zero(tampon_numero)
        List_commande = []
        for i in range(NB_commandes):
            List_commande.append((tampon_plats[i],tampon_numero[i]))
            print(CL_BROWN,end='')
            print(f"Commandes en attente: {List_commande}")
            print(CL_GRAY,end='')
            print(f"Nombre de commandes en attente: {NB_commandes}\n")

        for i, elt in enumerate(service_en_cours):
            if elt == 1:
                print(CL_BLUE,end='')
                print(f"Le serveur {i+1} a fini de servir son client\n")
        
        time.sleep(0.8)

        if time.time() - DEBUT > DURREE :
            keep_running.value = False
            print("\033[0m",end='') # reset





if __name__ == "__main__":
    # Debut du programme 

    # initialisation des sémaphores-------------------------#
    sem_tampon = mp.Semaphore(1)
    sem_serveur = mp.Semaphore(1)
    mutex = mp.Lock()


    DEBUT = time.time()
    keep_running = mp.Value(ctypes.c_bool, True) # True si le programme est en cours
    LIST_SERVEUR = [0 for i in range(NB_SERVEUR)]

    tampon_plats = mp.Array('i', TAILLE_TAMPON)
    tampon_numero = mp.Array('i', TAILLE_TAMPON)
    serveur_plats = mp.Array('i', NB_SERVEUR)
    serveur_numero = mp.Array('i', NB_SERVEUR)
    service = mp.Array('i', NB_SERVEUR)

    tampon = [tampon_plats, tampon_numero]
    serveur_en_cours = [serveur_plats, serveur_numero]

    # initialisation des processus
    Client = mp.Process(target = Clients, args = (keep_running, tampon, TAILLE_TAMPON))
    Major_dHomme = mp.Process(target = major_dHomme, args = (keep_running,DEBUT, tampon, serveur_en_cours, service))
    for k in range (NB_SERVEUR):
        LIST_SERVEUR[k] = mp.Process(target = Serveur, args = (keep_running, k, tampon, serveur_en_cours, service))

    # Lancement des processus

    Client.start()
    Major_dHomme.start()
    for i in range (NB_SERVEUR):
        LIST_SERVEUR[i].start()

    Client.join()
    Major_dHomme.join()
    for i in range (NB_SERVEUR):
        LIST_SERVEUR[i].join()