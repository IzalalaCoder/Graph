# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import messagebox as mb
from fpdf import FPDF
from graph import Graph
from summit import Summit
from user import User
from user import Page

class App:
    """
    Cette classe gérera la partie application. 
    Elle utilise le module tkinter.
    
    Constructeur : 
        - graphique = le graphe
        - main_app = l'application de type Tk
        - pos = le type d'affichage compris entre 1 et 5 et est par défaut égale à 1
    """
    
    # CONSTRUCTEUR
    
    def __init__(self, g : Graph):
        self._graphique = g 
        self._main_app = tk.Tk()
        self._pos = 1
        
        # Les différents cadres
        self._label = tk.LabelFrame(self._main_app, bd = 0)
        self._label_add = tk.LabelFrame(self._label, bd = 0)
        self._label_rem = tk.LabelFrame(self._label, bd = 0)


    # REQUETES
    
    def graph(self):
        """
        Retourn le graphique associé.
        """
        return self._graphique
        
    
    def appli(self):
        """
        Retourne l'application de type Tk/
        """
        return self._main_app
        
        
    def create_menu(self):
        """
        Crée le menu en fonction des utilisations de ce projet.
            - Graphe
            - Fichiers
            - Autre
        """
        main_menu = tk.Menu(self._main_app)
        
        # Premier menu déroulant --> GRAPH 
        first_menu = tk.Menu(main_menu, tearoff = 0)
        first_menu.add_command(label = "Voir le graphe", command = lambda self = self:self._graphique.look_graph(self._pos))
        first_menu.add_command(label = "Modifier l'affichage", command = self.modified_layout)
        first_menu.add_command(label = "Supprimer le graphe", command = self._graphique.reset_graph)
        first_menu.add_command(label = "A propos", command = self.information_on_graph)
        main_menu.add_cascade(label = "Graphe", menu = first_menu)
        
        # Second menu déroulant --> FICHIERS
        second_menu = tk.Menu(main_menu, tearoff = 0)
        second_menu.add_command(label = "Lire la liste d'adjacence", command = self._graphique.read_file)
        second_menu.add_command(label = "Ecrire une nouvelle liste d'adjacence", command = self._graphique.write_file)
        second_menu.add_command(label = "Ouvrir la liste d'adjacence", command = self._graphique.files().open_adjacency_list)
        second_menu.add_command(label = "Renommer le fichier de la liste d'adjence", command = self.rename_file)
        second_menu.add_command(label = "Ecraser la liste d'adjacence", command = self._graphique.files().reset_files)
        main_menu.add_cascade(label = "Liste d'adjacence", menu = second_menu)
        
        # Troisème menu déroulant --> Autre
        three_menu = tk.Menu(main_menu, tearoff = 0)
        three_menu.add_command(label = "Aide", command = self.helps)
        three_menu.add_command(label = "Quitter", command = self._main_app.quit)
        main_menu.add_cascade(label = "Autre", menu = three_menu)
        
        # Retourne le menu
        return main_menu
            
            
    # COMMANDES
    
    def add_user(self, family : str, name : str):
        """
        Ajoute un utilisateur dans le graphe en vérifiant bien les données entrées.
        """
        if len(family) > 0 and len(name) > 0:  
            f = family.lower().capitalize().replace(" ", "")
            n = name.lower().capitalize().replace(" ", "")
            u = User(f, n)
            self._graphique.add_summit(u)
        else:
            self.error_message()
    
    
    def add_page(self, name : str, family_u : str, name_u : str):
        """
        Ajoute une page dans le graphe en vérifiant bien les données entrées.
        """
        if len(name) > 0 and len(family_u) > 0 and len(name_u) > 0:
            f = family_u.lower().capitalize().replace(" ", "")
            n = name_u.lower().capitalize().replace(" ", "")
            t = name.lower().capitalize().replace(" ", "")
            p = None
            if n in self._graphique.info_dico():
                p = Page(t, self._graphique.info_dico()[n]["account"])
            else: 
                u = User(f, n)
                p = Page(t, u)
            self._graphique.add_summit(p)
        else:
            self.error_message()
            
    
    def add_arc(self, x : str, y : str):
        """
        Ajouter un lien entre x et y dans le graphe en vérifiant bien les données entrées.
        """
        l_summit = self._graphique.list_summit_name()
        if len(x) > 0 and len(y) > 0:
            a = x.lower().capitalize().replace(" ", "")
            b = y.lower().capitalize().replace(" ", "")
            if a in l_summit and b in l_summit:
                self._graphique.add_arc_by_name(a, b)
            else:
                self.error_message("L'un des comptes {}, {} n'existent pas".format(a, b))
        else:
            self.error_message()
    
        
    def rem_account(self, name : str):
        """
        Supprime un utilisateur ou une page dans le graphe en vérifiant bien les données entrées.
        """
        if len(name) > 0:
            n = name.lower().capitalize().replace(" ", "")
            if n in self._graphique.list_summit_name(): 
                self._graphique.remove_summit_by_name(n)
            else:
                self.error_message("Le compte {} n'existe pas".format(n))
        else:
            self.error_message()
    
    
    def rem_arc(self, x : str, y : str):
        """
        Supprimer un lien entre x et y dans le graphe en vérifiant bien les données entrées.
        """
        l_summit = self._graphique.list_summit_name()
        if len(x) > 0 and len(y) > 0:
            a = x.lower().capitalize().replace(" ", "")
            b = y.lower().capitalize().replace(" ", "")
            if a in l_summit and b in l_summit:
                if (a, b) in self._graphique.list_links():
                    self._graphique.remove_arc_by_name(a, b)
                else:
                    self.error_message("Le lien {} vers {} n'existe pas".format(a, b))
            else:
                self.error_message("Ce compte {} ou {} n'existe pas".format(a, b))
        else:
            self.error_message()
                
     
    def forms_add(self):
        frame_list = [
            tk.LabelFrame(self._label_add, text = "Ajouter un utilisateur", bd = 4, relief = "ridge", padx = 10, pady = 10),
            tk.LabelFrame(self._label_add, text = "Ajouter une page", bd = 4, relief = "ridge", padx = 10, pady = 10),
            tk.LabelFrame(self._label_add, text = "Ajouter un lien", bd = 4, relief = "ridge", padx = 10, pady = 10)
        ]

        widgets = [
            tk.Label(frame_list[0], text = "Nom de famille"),
            tk.Entry(frame_list[0], width = 50),
            tk.Label(frame_list[0], text = "Prénom"),
            tk.Entry(frame_list[0], width = 50),
            tk.Button(frame_list[0], text = "Ajouter", command = lambda self = self:self.add_user(widgets[1].get(), widgets[3].get())),
            tk.Label(frame_list[1], text = "Nom de famille de l'admin"),
            tk.Entry(frame_list[1], width = 50),
            tk.Label(frame_list[1], text = "Prénom de l'admin"),
            tk.Entry(frame_list[1], width = 50),
            tk.Label(frame_list[1], text = "Nom de la page"),
            tk.Entry(frame_list[1], width = 50),
            tk.Button(frame_list[1], text = "Ajouter", command = lambda self = self:self.add_page(widgets[10].get(), widgets[6].get(), widgets[8].get())),
            tk.Label(frame_list[2], text = "Nom du premier compte"),
            tk.Entry(frame_list[2], width = 50),
            tk.Label(frame_list[2], text = "Nom du second compte"), 
            tk.Entry(frame_list[2], width = 50),
            tk.Button(frame_list[2], text = "Ajouter", command = lambda self = self:self.add_arc(widgets[13].get(), widgets[15].get()))
        ]
        
        # Modification du fond
        self.modified_background(frame_list)
        self.modified_background([widgets[0], widgets[2], widgets[5], widgets[7], widgets[9], widgets[12], widgets[14]])
        
        # Enpaquetage
        self.packing(frame_list, 3, 3)
        self.packing(widgets, 1, 1)
        
        
    def forms_rem(self):
        frame_list = [
            tk.LabelFrame(self._label_rem, text = "Supprimer un compte", bd = 4, relief = "ridge", padx = 10, pady = 10),
            tk.LabelFrame(self._label_rem, text = "Supprimer un lien", bd = 4, relief = "ridge", padx = 10, pady = 10)
        ]

        widgets = [
            tk.Label(frame_list[0], text = "Nom du compte"),
            tk.Entry(frame_list[0], width = 50),
            tk.Button(frame_list[0], text = "Supprimer", command = lambda self = self:self.rem_account(widgets[1].get())),
            tk.Label(frame_list[1], text = "Nom du premier compte"),
            tk.Entry(frame_list[1], width = 50),
            tk.Label(frame_list[1], text = "Nom du second compte"),
            tk.Entry(frame_list[1], width = 50),
            tk.Button(frame_list[1], text = "Supprimer", command = lambda self = self:self.rem_arc(widgets[4].get(), widgets[6].get()))
        ]
        
        # Modification du fond
        self.modified_background(frame_list)
        self.modified_background([widgets[0], widgets[3], widgets[5]])
        
        # Enpaquetage
        self.packing(frame_list, 30, 30)
        self.packing(widgets, 5, 5)    

    
    def rename_file(self):
        """
        Formulaire qui modifie le nom du fichier de la liste d'adjacence.
        """
        top = tk.Toplevel()
        top.geometry("350x250")
        top.resizable(False, False)
        top.iconbitmap("image/graph_icon.ico")
        w = [
            tk.Label(top, text = "Nom du fichier"),
            tk.Entry(top, width = 30),
            tk.Label(top, text = ".txt"),
            tk.Button(top, text = "Renommer", command = lambda self = self:self._graphique.files().set_title(w[1].get()))
        ]
        
        self.modified_background([top, w[0], w[2]])
        self.packing(w, 6, 6)
        
        
    def helps(self):
        """
        Affiche l'aide dans une nouvelle fenêtre.
        (Chaque ligne sera expliquée dans un nouveau LabelFrame)
            - Comment ajouter, supprimer un compte
            - Comment ajouter, supprimer un lien
            - Comment lire le graphe
            - Comment créer une nouvelle liste d'adjacence
        """
        os.startfile("files\\read_me.pdf")
    
    
    def information_on_graph(self) :
        """
        Affiche la liste de toute les informations du graphique
        (Chaque ligne sera expliquée dans un nouveau LabelFrame)
            - Les utilisateurs
            - Les pages
            - Le plus influents
            etc....
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = "Information sur le graphe", ln = 5, align = 'C')
        
        # VALEURS NUMERIQUES
        """
        Liste toutes les valeurs numériques liés au graphe : 
            - Nombre de sommets
            - Nombre de comptes de type page et utilisateurs
            - Nombre d'administrateur
            - Age moyen des utilisateurs
            - Nombre moyen des abonnées
        """
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(300, 10, txt = "I. Informations globales sur le graphe", ln = 10, align = 'L')
        num_summit = str(self._graphique.number_summit())
        num_user = str(self._graphique.number_user())
        num_pages = str(self._graphique.number_page())
        num_admin = str(len(self._graphique.list_admin()))
        num_arc = str(self._graphique.number_arc())
        avg_age = str(self._graphique.average_age())
        avg_liker = str(self._graphique.average_liker())
    
        pdf.cell(200, 5, txt = "Nombre de comptes -> {}".format(num_summit), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Nombre d'utilisateurs -> {}".format(num_user), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Nombre de pages -> {}".format(num_pages), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Nombre d'administrateurs -> {}".format(num_admin), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Nombre d'arcs -> {}".format(num_arc), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Age moyen des utilisateurs -> {}".format(avg_age), ln = 2, align = 'L')
        pdf.cell(200, 5, txt = "Nombre moyen d'abonnées -> {}".format(avg_liker), ln = 2, align = 'L')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        
        s_maxi = None
        s_mini = None
        pr = algo_pagerank(self._graphique)
        maxi = 0.0
        mini = pr[self._graphique.list_summit_name()[0]]
        for i in pr:
            if pr[i] > maxi:
                maxi = pr[i]
                s_maxi = i
            elif pr[i] < mini:
                mini = pr[i]
                s_mini = i;
        pdf.cell(200, 10, txt = "L'algorithme de PageRank", ln = 5, align = 'L')
        pdf.cell(200, 10, txt = "-> Le compte le plus influent est {}".format(s_maxi), ln = 5, align = 'L')
        pdf.cell(200, 10, txt = "-> Le compte le moins influent est {}".format(s_mini), ln = 5, align = 'L')
        
        # SORTE DE BASES DE DONNEES
        """
        Pour chaque sommet, ses informations sont listés.
        """
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(300, 10, txt = "II. Les comptes", ln = 10, align = 'L')
        d = self._graphique.info_dico()
        for i in d:
            text = ""
            pdf.cell(200, 5, txt = "", ln = 5, align = 'C')
            if self._graphique.is_user(d[i]["account"]):
                f = d[i]["account"].get_family()
                a = d[i]["account"].get_age()
                m = len(d[i]["account"].get_friends())
                pdf.cell(200, 5, txt = "__________________________________________________________" , ln = 3, align = 'L')
                pdf.cell(200, 5, txt = "Nom de famille : {}".format(f), ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "Prénom : {}".format(i), ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "Age : {}".format(a) , ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "Nombre d'amis : {}".format(m) , ln = 2, align = 'L')
                if m > 0:
                    pdf.cell(200, 5, txt = "La liste des amis : " , ln = 2, align = 'L')
                    for x in d[i]["account"].get_friends():
                        pdf.cell(200, 5, txt = "    - {}".format(x.get_name()) , ln = 2, align = 'L')
            else:
                f = d[i]["account"].get_admin().get_family()
                n = d[i]["account"].get_name_admin()
                a = d[i]["account"].get_admin().get_age()
                l = d[i]["account"].get_number_liker()
                pdf.cell(200, 5, txt = "__________________________________________________________" , ln = 3, align = 'L')
                pdf.cell(200, 5, txt = "Nom de la page : {}".format(i) , ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "Nombre d'abonnées : {}".format(l) , ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "Concernant l'administrateur -> ", ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "    Nom de famille de l'administrateur : {}".format(f), ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "    Prénom de l'administrateur : {}".format(n), ln = 2, align = 'L')
                pdf.cell(200, 5, txt = "    Age de l'administrateur : {}".format(a) , ln = 2, align = 'L')
        
        # LES LISTES
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(300, 10, txt = "III. Les ensembles", ln = 10, align = 'L')
        
        # DEGRE SORTANT
        pdf.cell(300, 10, txt = " - Ensemble des sommets trié par degré sortant", ln = 10, align = 'L')
        pdf.cell(200, 10, txt = "NOM           - DEGRE SORTANT", ln = 10, align = 'L')
        for i in self._graphique.list_degrees_sorted_name():
            text = "{}      ->                  {}".format(str(i[0]), str(i[1]))
            pdf.cell(200, 5, txt = text, ln = 2, align = 'L')
            
        # RETOUR A LA LIGNE
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        
        # ENSEMBLE DES ARCS
        pdf.cell(300, 10, txt = " - Ensemble des ars", ln = 10, align = 'L')
        pdf.cell(300, 10, txt = "Le lien se fait du COMPTE 1 vers le COMPTE 2", ln = 10, align = 'L')
        pdf.cell(200, 10, txt = "COMPTE 1       ---->     COMPTE 2", ln = 10, align = 'L')
        for i in self._graphique.list_links():
            text = "{}                  ---->        {}".format(str(i[0]), str(i[1]))
            pdf.cell(200, 5, txt = text, ln = 2, align = 'L')
        
        # RETOUR A LA LIGNE
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        
        # ENSEMBLE D'ADMINISTRATEUR
        pdf.cell(300, 10, txt = " - Ensemble d'administrateurs ", ln = 10, align = 'L')
        for i in self._graphique.list_admin():
            text = "{}".format(i)
            pdf.cell(200, 5, txt = text, ln = 2, align = 'L')
        
        
        pdf.output("files\information_graph.pdf")
        os.startfile('files\information_graph.pdf')
    
    
    def error_message(self, msg = "Aucune saisie n'a été faite"):
        """
        Affiche un message d'erreur.
        """
        mb.showerror("ERREUR", msg)
    
    
    def modified_background(self, listing : list):
        """
        Modifie la couleur de fond.
        """
        for i in listing:
            i.config(background = "#c2d6d9")
    
    
    def modified_layout(self):
        """
        Modifie l'affichage du graphe:
            - 1 -> représente le shell
            - 2 -> représente le spring
            - 3 -> représente le random
            - 4 -> représente le spiral
            - 5 -> représente le planar
        """
        if self._pos == 1:
            self._pos = 2
        elif self._pos == 2:
            self._pos = 3
        elif self._pos == 3:
            self._pos = 4
        elif self._pos == 4:
            self._pos = 5
        else:
            self._pos = 1    
    
    
    def modified_geometry(self):
        """
        Modifie la position et la taille de la fenêtre.
        On veut la centrer au maximum.
        """
        # On interdit le changement de la taille de la fenêtre
        self._main_app.resizable(width = False, height = False)    
        
        # Coordonnees de la fenêtre
        window_x = 800
        window_y = 650
        
        # Coordonnees de l'ecran
        screen_x = self._main_app.winfo_screenwidth()
        screen_y = self._main_app.winfo_screenheight()
        
        """
          Centrage de la fenêtre
            - Position de x = (largeur_ecran // 2) - (largeur_fenetre // 2)
            - Position de y = (hauteur_ecran // 2) - (hauteur_fenetre // 2)
        """
        # Coordonnees de la position qui nous interesse
        pos_x = (screen_x // 2) - (window_x // 2) - 25
        pos_y = (screen_y // 2) - (window_y // 2) - 25
        
        info_geo = "{}x{}+{}+{}".format(window_x, window_y, pos_x, pos_y)
        self._main_app.geometry(info_geo)
    
    
    def packing(self, listing : list, x = 0, y = 0):
        """
        Exécute l'enpaquetage sur la fenêtre.
        """
        for i in listing:
            i.pack(padx = x, pady = y)
    
    
    def start_app(self):
        """
        Démarre l'application.
        Affiche la fenêtre avec toutes les composantes associés.
        """
        # Modification des paramètres de la fenêtre 
        self.modified_geometry()
        
        # Le titre du logiciel et son icone
        self._main_app.title("Network Graph App")
        self._main_app.iconbitmap("image/graph_icon.ico")
        
        title = tk.Label(self._main_app, text = "Network Graph App", pady = 10)
        title.config(background = "#c2d6d9")
        title.pack()
        
        """
        Paramètre de l'application
            - Ajout du menu sur la fenêtre
            - Spécification du background
            
        """
        self._main_app.config(menu = self.create_menu())
        self.modified_background([self._main_app, self._label_add, self._label_rem])
        
        # Ajout des boites pour pouvoir mieux les placer
        self._label.pack(padx = 25, pady = 25)
        self._label_add.pack(side = "left", ipadx = 0, ipady = 0)
        self._label_rem.pack(side = "right", ipadx = 0, ipady = 0, fill = "y")
        
        self.forms_add()
        self.forms_rem()

        # Affichage de la fenêtre
        self._main_app.mainloop()
    

# Fonctions pour les deux algos
def algo_pagerank(g : Graph):
    """
    Execute l'algorithme du PageRank.
    """
    # Initialisation de PageRank a 1 pour tous les sommets
    page_rank = {}
    for v in g.list_summit():
        page_rank[v.get_name()] = 1
    
    # Calcul du PageRank
    i = 0
    while i <= 100:
        # Pour tous les sommets du graphe
        for v in g.list_summit():
            # On calcul le PageRank du sommet
            page_rank[v.get_name()] = update_pr(g.list_summit(), v.list_in_neighbours(), page_rank)
        i += 1
    return page_rank
        
        
def update_pr(list_s : list, entrant : list, pr : dict):
    """
    Calcule la somme Pr(u) / N+(u) puis retourne le calcul suivant:
    (0.85 / |v|) + 0.85 * somme de Pr(u) / N+(u).
    """
    somme = 0
    for e in entrant:   
        # if len(e.list_in_neighbours()) != 0:
        somme += pr[e.get_name()] / len(e.list_out_neighbours())
    return (0.85 / len(list_s)) + 0.85 * somme
            
    
def algo_short_dist(g : Graph, s : Summit):
    """
    Execute l'algo de la plus courtes distances entre la source s et les sommets de V.
    """
    # Initialisation des distances entre chaque sommet et la source s a 10000000
    dist_summit_to_source = dict()
    for i in g.info_dico():
        dist_summit_to_source[i] = 10000000
        print("{} --> {}".format(i, dist_summit_to_source[i]))
    # Inititalisation de la distance du sommet source a 
    dist_summit_to_source[s.get_name()] = 0
    # P prend l'ensemble des sommets du graphes
    P = g.list_summit_name()
    u = P[0]
    # Calcule de la plus petite distance entre chaque sommet et la source 
    while len(P) > 0:
        print("BOUCLE")
        # On prend le sommet u de P le plus proche de la source
        for i in s.list_out_neighbours():
            if i.get_name() in P:
                u = i.get_name()
                break
        if u not in P:
            break
        P.pop(P.index(u))
        # Pour tous les voisins sortant de ce sommet u 
        print("nombre de voisins sortant de ", u, "est ", g.info_dico()[u]["degrees"])
        if g.is_user(g.info_dico()[u]["account"]):
            for v in g.info_dico()[u]["account"].list_out_neighbours():
                alt = dist_summit_to_source[u] + 1
                if alt <= dist_summit_to_source[v.get_name()]:
                    dist_summit_to_source[v.get_name()] = alt
    return dist_summit_to_source


# Fonction principale
if __name__ == "__main__":
    app = App(Graph())
    app.start_app()