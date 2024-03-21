""" 
NOM : SINGARIN-SOLE 
DATE : 05/06/2023
OBJECTIF : Simuler une course hippique avec arbitre 
"""

#Modules nécessaires 
from constantes import NBPROCESS, LONGEUR_COURSE
import time, random
import multiprocessing as mp






# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

CL_RESET = "\033[0m"
#-------------------------------------------------------

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

# Fonctions utiles pour écrire sur la console
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')
def en_couleur(Coul) : print(Coul,end='')


def tri_insertion_2D(L : list): 
    """Algorithme de tri insertion adapté à une variable d'un tableau à 2 dimensions

    Args:
        L (list): liste des chevaux en cours de course L = [[pos1,n°1], [pos2, n°2],......]

    Returns:
        list: retourne la même liste triée par rapport à la position de tous les chevaux
    """
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j][0] > cle[0]:
            L[j+1] = L[j] # decalage
            j = j-1
        L[j+1] = cle
    L.reverse()
    return L




# La tache d'un cheval
def un_cheval(ma_ligne : int, keep_running : bool ,tab_positions : list, mutex ) :
    """Initialise et simule le comportement d'un cheval à une position donnée

    Args:
        ma_ligne (int): ligne sur laquelle le cheval avance
        keep_running (_type_): booleen affichant True tant que la course n'est pas fini
        tab_positions (_type_): Tableau contenant la position de chaque cheval
        mutex() : mutex
    """
    col=1
    while col < LONGEUR_COURSE and keep_running.value :
        mutex.acquire()
        move_to(ma_ligne+1,col)         # Déplacer le curseur 
        erase_line_from_beg_to_curs()   # effacer la ligne correspondante
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)]) 
        print('('+chr(ord('A')+ma_ligne)+'🎠>')
        mutex.release()

        col+=1
        tab_positions[ma_ligne] = col # mise à jour du tableau

        time.sleep(0.1 * random.randint(1,5)) # pour simuler le déplacement saccadé du cheval

#------------------------------------------------
# La tache de l'arbitre

def arbitre(keep_running : bool,tab_positions : list,pari : str, mutex):
    """Simule le comportement d'un arbitre apportant un classement aux chevaux au cours de la course
        L'arbitre fait la distinction entre les coureurs déja arrivé et les autres afin de trier les bon éléments
        (respectivement la liste classement qui est celle des chevaux déja arrivé et la liste en_course 
         des chevaux entrain de courir )
    Args:
        keep_running (bool): booleen affichant True tant que la course n'est pas fini
        tab_positions (list): Tableau contenant la position de chaque cheval
        pari (str): lettre entre A et T qui permet de parier sur un cheval en début de course
        mutex () : mutex
    """
    classement = []
    mutex.acquire()
    move_to(23,1)
    print("Pari : {}".format(pari))
    mutex.release()
    while keep_running.value :
        en_course = []
        ex_aequo = []
        n = 0
        for k in range(NBPROCESS) :
            if tab_positions[k] >= LONGEUR_COURSE:
                if k in classement :
                    pass
                else :
                    n+=1
                    classement.append(k)
            else :
                en_course.append([tab_positions[k],k])
        if n > 1 :
            liste_ex_aequo = []
            for i in range(n) :
                liste_ex_aequo.append(classement[-(i+1)])
            ex_aequo.append(liste_ex_aequo)
                

        tri_insertion_2D(en_course)

        for i in range(len(en_course)):
            classement.append(en_course[i][1])

        for k in range(len(classement)) :
            mutex.acquire()
            move_to(24+k,1)
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[classement[k]%len(lyst_colors)])
            print("n°{} : {}".format(k+1,chr(classement[k]+65)))
            mutex.release()
        
        for i in range(len(en_course)):
            del classement[-1]


        # comportement de l'arbitre en fin de course
        if len(en_course) == 0:
            mutex.acquire()
            print("Le gagnant est {}".format(chr(classement[0]+65)))
            
            if len(ex_aequo) == 0 :
                move_to(45, 1)
                en_couleur(CL_WHITE)
                print("Pas d'ex aequo")
            else : 
                move_to(45, 1)
                en_couleur(CL_WHITE)
                print("Les ex aequos sont les suivants :\n ")
                for elt in ex_aequo :
                    texte = ""
                    for cheval in elt : 
                        texte += chr(cheval+65) + "; "
                    texte += "sont ex aequos."
                    move_to(46, 1)
                    print(texte+"\n")

            if pari == chr(classement[0]+65) : 
                move_to(48, 1)
                en_couleur(CL_WHITE)
                print("Tu as fini 1er 🥇")
            elif pari == chr(classement[1]+65) :
                move_to(48, 1)
                en_couleur(CL_WHITE)
                print("Tu as fini 2ème 🥈")
            elif pari == chr(classement[2]+65) :
                move_to(48, 1)
                en_couleur(CL_WHITE)
                print("Tu as fini 3ème 🥉")
            else :
                move_to(48, 1)
                en_couleur(CL_WHITE)
                print("Tu as perdu ")
            keep_running.value = False
            mutex.release()

        
        

#------------------------------------------------
# Fonction principale :
def course_hippique(keep_running : bool ,tab_positions: list ,pari : str, mutex) :
    """Fonctions permettant d'initialiser tous nos processus et ainsi reliant tous 
        les objets de notre programme

     Args:
        keep_running (bool): booleen affichant True tant que la course n'est pas fini
        tab_positions (list): Tableau contenant la position de chaque cheval
        pari (str): lettre entre A et T qui permet de parier sur un cheval en début de course
        mutex () : mutex
    """

    # 
    mes_process = [0 for i in range(NBPROCESS)] # initialisation des chevaux
    referee = mp.Process(target=arbitre,args=(keep_running,tab_positions,pari, mutex)) #initialisation de l'arbitre

    effacer_ecran()
    curseur_invisible()

    for i in range(NBPROCESS):  # Lancer processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,tab_positions, mutex))
        mes_process[i].start()

    referee.start()
    move_to(NBPROCESS+1, 1)
    print("Debut de la course !!!")

    for i in range(NBPROCESS): mes_process[i].join()

    mutex.acquire()
    move_to(50, 1)
    curseur_visible()
    print(CL_RESET)
    print("Fin de la course ...")
    mutex.release()
    
