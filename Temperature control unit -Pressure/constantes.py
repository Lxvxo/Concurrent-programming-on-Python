""" 
NOM : SINGARIN-SOLE 
DATE : 16/06/2023
OBJECTIF : Controle de température/pression
"""

#Constantes nécessaires------------------------------------#
T_int = 25 # Température initiale

P_int = 1.013 # Pression initiale

DURREE = 30 # Durrée de fonctionnement du controleur

PUISSANCE_CHAUFFAGE = 0.5 # augmentation de la température par le chauffage 

PUISSANCE_POMPE = 0.01 # Diminution de la pression par la pompe
 
TEMPERATURE_DOWN = 0.3 # diminution naturelle de la température

PRESSION_UP = 0.005 # augmentation naturelle de la pression