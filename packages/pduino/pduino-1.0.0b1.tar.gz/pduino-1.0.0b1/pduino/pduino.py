'''
Name:       pduino
Version     V 1.0.0
Purpose:    utilitaires de mesures arduino
            Mode 1: acquisition temporelle
              Il est possible de mesurer une ou plusieurs voies en fonction
              du temps et d'appliquer éventuellement une fonction de transfert.
               - en mode lent (arduino envoi des données entre chaque mesure)
               - en mode rapide (arduino envoi des données à la fin des mesures)
              Les mesures peuvent être stockées dans un fichier csv pour
              exploitation utérieure
              Démo avec, par exepmple, les programmes mesures_condensateur.py,
              condo.ino et condo_rapide.ino

            Mode 2: point par point
              - la méthode set_command() permet d'envoyer n'importe quelle commande
                à Arduino et de recevoir la réponse. Elle permet donc d'utiliser
                toutes les possibilités de commande et de mesure d'Arduino.
                Le programme mariotte_mesure.py est un bon exemple d'utilisation.
              - la methode mesure_points() fournit un protocole de mesure rapide
                et par défaut (voir programme mariotte_simple.py)

Copyright (C) 2023 Philippe Campion
License    GNU GENERAL PUBLIC LICENSE Version 3
'''
import matplotlib.pyplot as plt
import time
import serial
import serial.tools.list_ports

def liste_ports():
    '''liste les ports COM connectés
    '''
    liste = [comport.device for comport in serial.tools.list_ports.comports()]
    return liste

def ecrit_fichier_csv(fichier, *args):
    ''' écrit les données dans un fichier csv
        entrées : fichier -> str nom du fichier (avec extension .csv)
                  args -> list :  les listes (tableaux) de données à enregistrer
        exemple : ecrit_fichier_csv('condensateur.csv', t, E, uc)
    '''
    with open(fichier,'w') as f :
        for i in range(len(args[0])):
            s = ''
            for e in args:
                s += '{};'.format(e[i])
            s = s[:-1] + '\n'
            f.write(s)
    f.close()

def lit_fichier(fichier):
    ''' Lit le fichier de mesures et le stocke dans des tableaux
        entrée : fichier -> str : nom du fichier (avec extension .csv)
        sortie -> tuple :  les listes (tableaux) de données
        exemple: t, E, u = lit_fichier('condensateur.csv')
    '''
    sortie = []
    with open(fichier,'r') as f :
        for ligne in f:
            result = ligne.replace('\n', '').split(';')
            if len(sortie) == 0:
                 for i in range(len(result)):
                        sortie.append([])
            for i in range(len(result)):
                sortie[i].append(float(result[i]))
    f.close()
    return tuple(sortie)

def liste_valeurs(nom, tab, n=0):
    ''' renvoie une chaine de caractères du type 'nom = [v1, v2, ...]'
        permettant de récupérer une liste de mesures sous forme de copier-collé
        entrées : nom -> str : le nom du tableau 
                  tab -> list: la liste (tableau) de valeurs
                  n -> int   : le nombre de caractère par ligne d'affichage
                               si n=0, il n' a pas de passage à la ligne lors de l'affichage
        exemple : print(liste_valeurs('E', E))
              ou  print(liste_valeurs('E', E, 70))
    '''
    entete = '{} = ['.format(nom)
    s = entete
    compteur = len(s)
    espaces = ' '*(len(nom) + 4)
    for v in tab:
        ls = '{}, '.format(v)
        s += ls
        if n!=0:
            compteur += len(ls)
            if compteur > n:
                ls = '\n' + espaces
                s += ls
                compteur = len(ls)
    if n!=0 and compteur == len(ls):
        return s[:-(len(s) - s.rfind(','))] + ']'
    else:
        return s[:-2] + ']'

def affiche_graphe(titre, label_x, label_y, donnees, taille=None):
    ''' affiche le graphe
        entrée : titre -> str : le titre du graphe
                 lable_x et label_y : les labels des axes
                 donnees : une liste de listes (tableaux) de données
                 le premier tableau contient la donnée en abscisse
                 taille -> tuple : taille du graphique (None par defaut) - par exemple taille = (9, 7)
        sortie : affichage du graphe
        exemple: affiche_graphe('Evolution des tensions E et uc', 't (s)', 'u (V)', [t, E, uc])
    '''
    if taille == None:
        fig = plt.figure(titre)
    else:
        fig = plt.figure(titre, figsize=taille)
    ax = fig.add_subplot(1, 1, 1)
    #fig, ax = plt.subplots(constrained_layout=True, figsize=(4, 3))
    ax.set_title(titre, fontsize=14)
    ax.grid(True)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    for i in range(1, len(donnees)):
        ax.plot(donnees[0], donnees[i], linestyle="", marker="o")
    plt.show()

class Arduino:
    def __init__(self, port='auto'):
        '''crée un orbjet Arduino
           entrée: str: le port COM auquel est connecté auquel est connecté la carte
        '''
        if port == 'auto':
            # expérimental et non documenté : ne fonctionne pas toujours
            # si port = 'auto'(valeur par defaut), tente de le détecter en utilisant la fonction `liste_ports`
            liste = [comport.device for comport in serial.tools.list_ports.comports()]
            self.arduino = serial.Serial(port=liste[-1], baudrate=9600, timeout=1)
        else:
            # méthode à utiliser de préférence
            self.arduino = serial.Serial(port=port, baudrate=9600, timeout=1)

    def mesures_tempo(self, chaine, n, affichage=None, fonctions=[]):
        ''' récupère les mesures envoyées par Arduino sur la liaison série
            entrée : chaine -> str : la commande à envoyer à Arduino
                     n -> int : le nombre de voies mesurées (sans compter le temps)
                     affichage -> fonction (None par défaut)
                              prend en paramètre le temps et un tuple contenant les voies.
                              est appelée pendant les mesures pour afficher les données
                     fonctions -> list de fonctions (vide par défaut)
                              fonction à appliquer eventuellement sur la grandeur fournie par Arduino
                              par exemple [lambda x: 5.0*x/1023, lambda x: 5.0*x/1023]
            sortie -> tuple : les listes (tableaux) de données
                              le temps sera toujours la première donnée
            exemple: arduino = Arduino('COM21')
                     t, E, uc = arduino.mesures_tempo('charge', 2, None, [lambda x: 5.0*x/1023, lambda x: 5.0*x/1023])
        '''
        try:
            n = n + 1 # on ajoute une voie pour le temps
            datas = [[] for i in range(n)]
            # attend que la liaison soit libre et envoie la commande
            while self.arduino.readline().decode() != '' : {}
            self.arduino.write(chaine.encode())
            # attend la reponse
            ligne = self.arduino.readline().decode()
            while ligne == '':
                ligne = self.arduino.readline().decode()[:-2]
            while ligne != 'end':
                if ligne != '':
                    valeurs = ligne.split(",")
                    # la première valeur est nécessairement le temps en ms
                    datas[0].append(float(valeurs[0])/1000) # t en s
                    if fonctions == []:
                        for i in range(1, n):
                            datas[i].append(float(valeurs[i]))
                    else:
                        for i in range(1, n):
                            datas[i].append(fonctions[i-1](float(valeurs[i])))
                    #  affichage
                    if affichage != None:
                        T = [datas[0][-1]]
                        for i in range(1, n):
                            T.append(datas[i][-1])
                        affichage(tuple(T))
                    else:
                        print('.', end='')
                ligne = self.arduino.readline().decode()[:-2]
            return datas
        except:
            pass

    def set_command(self, command=''):
        ''' effectue une mesure ponctuelle sur Arduino ou envoie une commande
            entrée : command -> str : la commande à envoyer à Arduino
                                      'mesure' par défaut si non renseigné
            sortie -> str : la valeur renvoyée par Arduino
                                     (à surtyper en int ou float selon les cas)
            exemple: arduino = Arduino('COM21')
                     b = int(arduino.set_command('mesure'))
        '''
        while self.arduino.readline().decode() != '' : {}
        if command =='':
            command = 'mesure'
        else:
            self.arduino.write('{}'.format(command).encode())
        time.sleep(1)
        try:
            data = self.arduino.readline()
            mesure = data.decode()[:-2]
        except:
            mesure = None
        return mesure

    #--- pour les débutants (voir le programme 'mariotte_simple.py') mais n'offre pas toutes les fonctionnalités
    def mesures_points(self, message, affichage=None):
        ''' effectue des mesures point par point sur Arduino
            entrée : message -> str : le message à afficher à la saisie de chaque point
                     affichage -> fonction (None par défaut)
                              prend en paramètre le temps et un tuple contenant
                              les voies.
                              est appelée pendant les mesures pour afficher
                              les données
            sortie -> tuple : les listes (tableaux) de données mesurées

            exemple : def affiche(T):
                        print('V = {:.1f} mL ; P = {:.2f} hPa'.format(T[0], T[1]))

                      try:
                        arduino = Arduino('COM21')
                        V, P = arduino.mesures_points('Valeur de V (de 20 à 60 mL)\n',
                                                       affichage = affiche)
                      finally:
                        arduino.close()
        '''
        voie1, voie2  = [], []
        saisie = True
        # vide la ligne serie
        while self.arduino.readline().decode() != '' : {}
        while saisie:
            try:
                v =input('{}(-1 pour supprimer dernier point)'.format(message))
                if v != '-1':
                    v1 = int(v)
                    # mesure de la pression
                    self.arduino.write('mesure'.encode())
                    time.sleep(1)
                    data = self.arduino.readline()
                    v2 = float(data.decode()[:-2])
                    if affichage != None:
                        affichage((v1, v2))
                    else:
                        print('Voie 1 = {:.2f} ; Voie2 = {:.2f}'.format(v1, v2))
                    voie1.append(v1)
                    voie2.append(v2)
                else:
                    if len(voie1) > 0:
                        voie1.pop()
                        voie2.pop()
                        print('Dernier point supprimé\n')
                    else:
                        print('Pas de dernier point\n')
            except KeyboardInterrupt:
                saisie = False
            except ValueError:
                print('Erreur de saisie\n')
        return voie1, voie2

    def close(self):
        '''libère le port série
           à utiliser dans un bloc try ... finally pour éviter les problèmes de connection au port série

           exemple:
               arduino = Arduino(port)
               try:
                  ...
               finally:
                  arduino.close()
        '''
        self.arduino.close()

# ---
if __name__ == '__main__':
    pass