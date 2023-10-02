'''
Name:        jupduino
Version      V 1.0
Purpose:     Réalisation d'interfaces de mesure simples utilisant une carte arduino sous jupyter
             liaison simplifiée avec la bibliothèque pduino
             Mode 1: acquisition temporelle
             Mode 2: acquisition point par point

 Created:    28/04/2023
 Licence     CC BY-SA 4.0
 Copyright (C) 2023 Philippe Campion
 License    GNU GENERAL PUBLIC LICENSE Version 3
'''
import sys
sys.path.insert(0, "..")

import ipywidgets as widgets
from IPython.display import display, clear_output
from pduino import *
from copy import deepcopy

class Interface:
    '''
    La classe implémente sous jupyter une interface d'acquisition pour arduino utilisant le module pduino
    '''
    def __init__(self, p_port='', p_grandeurs=[], p_mode='points', p_temps_reel=True): # temporel ou points
        '''
        initialise la classe
        entrée : p_port -> str : port série auquel est connecté arduino (voir la documentation de pduino)
                 p_grandeurs -> list : tableau de tuple contenant les grandeurs à mesurer et leurs unités
                                       par exemple:  [('t', 's'), ('E', 'V'), ('uc', 'V')]
                                                     [('V', 'mL'), ('P', 'Pa')]
                 p_mode -> str : 'temporel' ou 'points'
                 p_temps_reel -> bool :  Si p_temps_reel vaut True, le graphe est réaffiché à chaque nouvelle mesure. A utiliser dans le cas de mesures lentes.
                                         Si p_temps_reel vaut False, le graphe est affiché à la fin des mesures. A utiliser dans le cas de mesures rapides.

                 exemple : mon_interface = Interface('COM21', [('t', 's'), ('θ', '°C')], 'temporel', True)
        '''
        assert p_mode in ['temporel', 'points'], 'p_mode doit être égal à "temporel" ou "point"'
        # assert len(p_grandeurs)>=2, 'grandeurs doit contenir au moins 2 éléments'
        self.port = p_port
        self.mode = p_mode
        self.grandeurs = p_grandeurs
        # pour stocker les mesures envoyées par self.affichage
        self.voies_mesures = [[] for i in range(len(self.grandeurs))]
        self.voies = [[] for i in range(len(self.grandeurs))]
        l_connexion = widgets.Button(value=False, description='Arduino', disabled=False,
                                           button_style='danger', # 'success', 'info', 'warning', 'danger' or '',
                                           icon='')
        l_connexion.on_click(self.connecte)
        self.arduino = None
        self.widgets = [l_connexion]
        self.zone_affichage = widgets.Output(layout=widgets.Layout(margin='20px 0 0 20px', max_width='800px'))
        self.zone_barre = widgets.IntProgress(value=0, min=0, max=10, step=1, description='Loading:',
                                              bar_style='', # 'success', 'info', 'warning', 'danger' or ''
                                              orientation='horizontal')
        self.zone_graphique = widgets.Output()
        self.taille_graphique = (9, 7)
        self.nouvelles_mesures = False
        self.affichage = None
        self.graphe_temps_reel = p_temps_reel
        #print(self.zone_affichage.layout.keys)

    def add_bouton(self, p_texte, p_command):
        '''
        méthode publique
        ajoute un bouton à la classe
        entrée : p_texte -> str : le texte qui s'affiche sur le bouton
                 p_command -> function : la fonction à exécuter lorsqu'on clique sur le bouton
        sortie -> ipywidgets.widgets.widget_button.Button : widget contenant le bouton

        exemple :
        mon_interface = Interface('COM21', [('t', 's'), ('θ', '°C')], 'temporel')
        ...
        def mesure():
            # exécuté lorsque l'utilisateur clique sur le bouton 'Mesure'
            global t, θ
            t, θ = mon_interface.mesures_tempo('mesure', 1)
        ...

        # --- programme principal
        mon_interface.add_bouton('Mesure', mesure)
        ...
        mon_interface.affiche()

        '''
        l_widget = widgets.Button(description=p_texte)
        l_widget.on_click(lambda p: self.execute_command(p_command))
        self.widgets.append(l_widget)
        return l_widget

    def add_saisie(self, p_description, p_valeur=""):
        '''
        méthode publique
        ajoute un une zone de saisie à la classe
        entrée : p_description -> str : le texte de description de la zone de saisie
                 p_valeur -> str : la valeur par défaut dans la zone de saisie
        sortie -> ipywidgets.widgets.widget_string.Text : widget contenant la zone de saisie
        exemple : saisie = mon_interface.add_saisie('Nom Fichier', 'temperatures')
        '''
        l_widget = widgets.Text(value=p_valeur, description=p_description, disabled=False,
                                style ={'description_width': 'initial'}, layout=widgets.Layout(width='200px'))
        self.widgets.append(l_widget)
        return l_widget

    def update(self, T):
        '''
        méthode privée
        mise à jour des données affichées par l'interface
         - dans le cas de mesure temporelles, est passée par défaut comme argument à la fonction mesure_tempo de pduino
           par la fonction self.mesures_tempo
         - dans le cas de mesures par points, doit être appelée à chaque mesure par les fonctions self.ajoute_point
           et self.supprime_dernier_point
        entrée : T -> list ou int : tableau contenant le dernier point de mesure pour chacune des voies
                                    -1 provoque la suppression du dernier point dans le cas de mesures par points
        '''
        if T != -1:
            for i in range(len(T)):
                self.voies_mesures[i].append(T[i])
            if self.mode == 'temporel':
                if self.zone_barre.value == 10:
                    self.zone_barre.value = 0
                else:
                    self.zone_barre.value += 1
            if self.affichage != None:
                self.affichage(T)
            '''modifé pour essayer d'afficher le graphique en temps réel'''
            if self.graphe_temps_reel:
                with self.zone_graphique:
                    clear_output(wait=True)
                    chaine_abscisse = self.grandeurs[0][0] + ' ({})'.format(self.grandeurs[0][1])
                    chaine_ordonnee = ''
                    for i in range(1, len(self.grandeurs)):
                        chaine_ordonnee += self.grandeurs[i][0] + ' ({}) - '.format(self.grandeurs[i][1])
                    affiche_graphe('Evolution des grandeurs mesurées', chaine_abscisse, chaine_ordonnee[:-2], self.voies_mesures, taille=(9,7))
            # self.nouvelles_mesures a ete traite
            self.nouvelles_mesures = False


        elif self.mode == 'points':
            # suppression du dernier point
            if len(self.voies[0]) > 0:
                self.voies[0].pop()
                self.voies[1].pop()
                # pour forcer le réaffichage du graphique
                self.nouvelles_mesures = True

    def affiche(self):
        '''
        méthode publique
        affiche le widget interface complet

        exemple :
        mon_interface = Interface('COM21', [('t', 's'), ('θ', '°C')], 'temporel')
        ...

        # --- programme principal
        ...
        mon_interface.affiche()
        '''
        if self.mode == 'temporel':
            zone_1 = widgets.HBox(self.widgets + [self.zone_barre])
            zone_2 = widgets.HBox([self.zone_graphique, self.zone_affichage])
        else:
            with self.zone_graphique:
                # affiche un graphe vide
                '''
                x, y = [], []
                clear_output(wait=True)
                chaine_abscisse = self.grandeurs[0][0] + ' ({})'.format(self.grandeurs[0][1])
                chaine_ordonnee = ''
                for i in range(1, len(self.grandeurs)):
                    chaine_ordonnee += self.grandeurs[i][0] + ' ({}) -'.format(self.grandeurs[i][1])
                titre = 'Evolution des grandeurs mesurées'
                fig = plt.figure(titre, figsize=self.taille_graphique)
                ax = fig.add_subplot(1, 1, 1)
                ax.set_title(titre, fontsize=14)
                ax.grid(True)
                ax.set_xlabel(chaine_abscisse)
                ax.set_ylabel(chaine_ordonnee[:-2])
                ax.plot(x, y, linestyle="", marker="o")
                plt.show()
                '''
            zone_1 = widgets.HBox(self.widgets)
            zone_2 = widgets.HBox([self.zone_graphique, self.zone_affichage])
        zone_total = widgets.VBox([zone_1, zone_2])
        display(zone_total)

    def execute_command(self, p_command):
        '''
        méthode privée
        exécute la fonction p_command associée à un bouton lorsque l'utilisateur clique sur celui-ci
        p_command -> function : la fonction à exécuter
        '''
        # efface la sortie zone_affichage en mode temporel
        if self.mode == 'temporel':
            self.zone_barre.value = 0
        # execute la commande (la sortie s'affiche dans self.zone_affichage)
        with self.zone_affichage:
            p_command()
        # en mode temporel si self.voies est plein, on le copie et on le réinitialise (c'est qu'on a fait une mesure)
        self.nouvelles_mesures = self.nouvelles_mesures or (len(self.voies_mesures[0]) != 0)
        if self.nouvelles_mesures:
            if self.mode == 'temporel':
                self.voies = deepcopy(self.voies_mesures)
            else: # self.mode == 'points' obligatoirement
                if len(self.voies_mesures[0]) != 0:
                    for i in range(len(self.voies_mesures)):
                        self.voies[i].append(self.voies_mesures[i][0])
            self.voies_mesures = [[] for i in range(len(self.grandeurs))]
            with self.zone_graphique:
                clear_output(wait=True)
                chaine_abscisse = self.grandeurs[0][0] + ' ({})'.format(self.grandeurs[0][1])
                chaine_ordonnee = ''
                for i in range(1, len(self.grandeurs)):
                    chaine_ordonnee += self.grandeurs[i][0] + ' ({}) - '.format(self.grandeurs[i][1])
                affiche_graphe('Evolution des grandeurs mesurées', chaine_abscisse, chaine_ordonnee[:-2],
                                self.voies, taille=(9,7))
            # self.nouvelles_mesures a ete traite
            self.nouvelles_mesures = False

    def connecte(self, b):
        '''
        méthode privée
        fonction bascule qui effectue ou libère la connexion avec la carte arduino
        entrée : b -> ipywidgets.widgets.widget_button.Button : le bouton qui a appelé la méthode
                      remarque: ce bouton est placé sur l'interface par le constructeur de la classe
                                sans intervention de l'utilisateur
        '''
        if self.arduino == None:
            self.arduino = Arduino(port=self.port)
            self.widgets[0].button_style = 'success'
            self.widgets[0].icon = 'check'
        else:
            # fermeture du port (ne pas oublier)
            self.arduino.close()
            self.arduino = None
            self.widgets[0].button_style = 'danger'
            self.widgets[0].icon = ''

    def mesures_tempo(self, chaine, n, affichage=None, fs=[]):
        '''
        méthode publique
        appelle la fonction mesures_tempo du module pduino
        et récupère les mesures envoyées par Arduino sur la liaison série
        entrée : chaine -> str : la commande à envoyer à Arduino
                fonctions -> list de fonctions (vide par défaut)
                             fonction à appliquer eventuellement sur la grandeur
                             fournie par Arduino
                             par exemple [lambda x: 5.0*x/1023, lambda x: 5.0*x/1023]
            sortie -> tuple : les listes (tableaux) de données
                              le temps sera toujours la première donnée
            exemple: mon_interface = Arduino('COM21', [('t', 's'), ('E', 'V'), ('uc', 'V')], 'temporel')
                     t, E, uc = mon_interface.mesures_tempo('charge', [lambda x: 5.0*x/1023, lambda x: 5.0*x/1023])
        '''
        self.affichage = affichage
        return self.arduino.mesures_tempo(chaine, n, affichage=self.update, fonctions=fs)

    def set_command(self, command=''):
        '''
        méthode publique
        appelle la fonction set_command du module pduino
        et récupère les mesures envoyées par Arduino sur la liaison série

        exemple: mon_interface = Interface('COM21')
                 b = int(mon_interface.set_command('mesure'))
        '''
        return self.arduino.set_command(command)

    def ajoute_point(self, x, y):
        '''
        méthode publique
        ajoute un point de coordonnées x, y dans le cas de mesures ponctuelles

        exemple:
        my_int_ponctuel = Interface('COM8', [('V', 'mL'), ('P', 'Pa')], 'points')

        def mon_acquisition():
            v = int(saisie.value)
            p = float(my_int_ponctuel.set_command('mesure'))
            print('V = {:.1f} mL ; P = {:.2f} hPa'.format(v, p))
            my_int_ponctuel.ajoute_point(v, p)

        def supp_dernier_point():
            if my_int_ponctuel.supprime_dernier_point():
                print("Dernier point supprimé")
            else:
                print('Pas de dernier point')

        def sauvegarde():
            fichier = nom_fic.value + '.csv'
            V, P = my_int_ponctuel.get_valeurs()
            ecrit_fichier_csv(fichier, V, P)
            print('fichier {} créé'.format(fichier))

        # programme principal---
        saisie = my_int_ponctuel.add_saisie('V (mL)', '60')
        my_int_ponctuel.add_bouton('Mesure', mon_acquisition)
        my_int_ponctuel.add_bouton('Supp. dernier point', supp_dernier_point)
        nom_fic = my_int_ponctuel.add_saisie('Nom fichier', 'mesures')
        my_int_ponctuel.add_bouton('Sauvegarde', sauvegarde)
        my_int_ponctuel.affiche()
        '''
        self.update([x, y])

    def supprime_dernier_point(self):
        '''
        méthode publique
        supprime le dernier point ajouté dans le cas de mesures ponctuelles
        exemple : voir Méthode ajoute_point(self, x, y)
        '''
        if len(self.voies[0]) > 0:
            self.update(-1)
            return True
        else:
            return False

    def get_valeurs(self):
        '''
        méthode publique
        renvoir un tuple qui contient les tableaux de valeurs
        utile dans le cas de mesures ponctuelles pour récupérer les tableaux une fois la série terminée
        sortie -> tuple : les listes (tableaux) de données

        exemple:
        my_int_ponctuel = Interface('COM8', [('V', 'mL'), ('P', 'Pa')], 'points')
        ...
        def sauvegarde():
            fichier = nom_fic.value + '.csv'
            V, P = my_int_ponctuel.get_valeurs()
            ecrit_fichier_csv(fichier, V, P)
            print('fichier {} créé'.format(fichier))

        # programme principal---
        ...
        nom_fic = my_int_ponctuel.add_saisie('Nom fichier', 'mesures')
        my_int_ponctuel.add_bouton('Sauvegarde', sauvegarde)
        my_int_ponctuel.affiche()
        '''
        if len(self.voies) == 1:
            return self.voies[0]
        else:
            return tuple(self.voies)