# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx 
from summit import Summit
from user import User
from page import Page
from files import Files

class Graph:
    """
    La classe qui représente le graphe en lui même, le tracera.
    Cette classe contiendra toutes les informations de tout les sommets présents dans le graphe.
    On le tracera via le module networkx et matplotlib.pyplot.
    
    @cons:
        graph = nx.DiGraph()
        infoGraph = dict() avec la clé le nom du sommet et contiendra les informations suivantes
            account -> le compte associé au nom soit de type User ou de type Page pour accéder à leur informations si besoin
            degrees -> le numéro représentant le degrés sortant du compte 
            links -> la liste de tout les liens responsable de ce compte (C -> X) X étant un autre compte
    """
    
    # CONSTRUCTEUR
    
    def __init__(self):
        self._graph = nx.DiGraph()
        self._info = dict()
        self._file = Files()
        
        
    # REQUETES
    
    def graph(self):
        """
        Retourne le graphe.
        """
        return self._graph
    
    
    def info_dico(self):
        """
        Retourne le dictionnaire associée a ce graphe.
        """
        return self._info
    
    
    def files(self):
        """
        Retourne le fichier.
        """
        return self._file
     
     
    # DIGRAPH
    
    def look_graph(self, x : int):
        """ 
        Affiche le graphe orienté via pyplot et networkx.
        """
        if x in [1, 2, 3, 4, 5]:
            # Initialisation
            colorsSu = ["cyan"] * len(self._info)
            
            # Modification pour certains sommets
            value = 0
            for i in self._info:
                if isinstance(self._info[i]["account"], Page):
                    colorsSu[value] = "pink"
                value += 1
                
            options = {'node_color' : colorsSu,
                    'node_size' : 100,
                    'with_labels' : True
                    }
            
            version = ""
            if x == 1:
                options['pos'] = nx.shell_layout(self._graph)
                version = "Shell"
            elif x == 2:
                options['pos'] = nx.spring_layout(self._graph)
                version = "Spring"
            elif x == 3:
                options['pos'] = nx.random_layout(self._graph)
                version = "Random"
            elif x == 4:
                options['pos'] = nx.spiral_layout(self._graph)
                version = "Spiral"
            elif x == 5:
                options['pos'] = nx.planar_layout(self._graph)
                version = "Planar"
                
            """
            Les affichage selong un algo déjà définis 
                - spiral_layout(G) représentation sous forme de spirale
                - shell_layout(G) représentation sous forme de cercle
                - circular_layout(G) représentation sous forme de cercle
                - random_layout(G) représentation aléatoire
                - spring_layout(G) représentation en fonction des labels
                - planar_layout(G) représentation en forme de triangle 
            """ 
            
            # Affichage 
            plt.figure()
            
            plt.title("Représentation du graphe en version {}".format(version))
            nx.draw(self._graph, **options)
            plt.show()
            
    
    # LIST
    
    def list_summit(self):
        """
        Retourne la liste de tous les sommets de types confondus présent dans le graphe.
        """
        summit = []
        for i in self._info:
            summit.append(self._info[i]["account"])
        return summit
    
    
    def list_user(self):
        """
        Retourne la liste des comptes de type Utilisateurs.
        """
        users = []
        for i in self._info:
            if isinstance(self._info[i]["account"], User):
                users.append(self._info[i]["account"])
        return users
    
    
    def list_page(self):
        """
        Retourne la liste des comptes de type Page.
        """
        pages = []
        for i in self._info:
            if isinstance(self._info[i]["account"], Page):
                pages.append(self._info[i]["account"])
        return pages
        
        
    def list_admin(self):
        """
        Retourne la liste des noms des utilisateurs qui sont admins des pages.
        """
        admin = []
        for i in self.list_page():
            if i.get_name_admin() not in admin:
                admin.append(i.get_name_admin())
        return admin

    
    def list_summit_name(self):
        """
        Retourne les noms de tous les sommets de types confondus présent dans le graphe.
        """
        names = []
        for i in self._info:
            names.append(i)
        return names
    
    
    def list_summit_name_sorted(self):
        return sorted(self.list_summit_name())
    
    
    def list_links(self):
        """
        Retourne la liste de tous les liens.
        """
        links = []
        for i in self._info:
            links.extend(self._info[i]["links"])
        return links
        
    
    def list_degrees_sorted_name(self):
        """
        Retourne la liste des nom des différents comptes selon le tri des degrés sortant.        
        """
        l = sorted(self._info, key = lambda k: self._info[k]["degrees"])
        nl = []
        index = 0
        while index < len(l):
            t = (l[index], self._info[l[index]]["degrees"])
            nl.append(t)
            index += 1
        del l
        return nl
    
    
    # SUMMIT
    
    def ieme_summit(self, i : int):
        """
        Retourne le i-ème sommet.
        
        pre condition : 
            i >= 0 et i < nombre de compte existant.
        """
        if i >= 0 and i < self.number_summit():
            return self._info[self.list_summit_name()[i]]["account"]
        
        
    def name_summit(self, key : str):
        """
        Retourne le sommet dont la clé est key.
        """
        if name in self._info:
            return self._info[key]["account"]
    
    
    # BOOLEAN
    
    def link_is_possible(self, x : Summit, y : Summit):
        """
        Teste si le lien entre les sommets x et y est possible à se réaliser et retourne un booléen.
            les liens suivants sont possibles
                U -> P
                U -> U
            Les liens suivants ne sont pas possible 
                P -> U   
                P -> P 
        """
        if isinstance(x, Page):
            return False
        return True


    def is_user(self, x : Summit):
        """
        Retourne un booleen selon si c'est un user ou non.
        """
        return isinstance(x, User)
    
    
    def is_page(self, x : Summit):
        """
        Retourne un booleen selon si c'est une page ou non.
        """
        return isinstance(x, Page)
    
    
    # INT
    
    def number_summit(self):
        """
        Retourne le nombre de sommets existant dans le graphe.
        """
        return len(self._info)
    
    
    def number_arc(self):
        """
        Retourne le nombre de connexions existante dans le graphe.
        """
        links = 0
        for i in self._info:
            links += len(self._info[i]["links"])
        return links
    
    
    def number_user(self):
        """
        Retourne le nombre de compte de types User existant dans le graphe.
        """
        users = 0
        for i in self._info:
            if isinstance(self._info[i]["account"], User):
                users += 1
        return users
    
    
    def number_page(self):
        """
        Retourne le nombre de compte de type Page existant dans le graphe.
        """
        pages = 0
        for i in self._info:
            if isinstance(self._info[i]["account"], Page):
                pages += 1
        return pages
        
        
    def average_age(self):
        """
        Retourne l'age moyen des utilisateurs.
        """
        if len(self.list_user()) > 0:
            age = 0
            for u in self.list_user():
                age += u.get_age()
            return age / self.number_user()
            
            
    def average_liker(self):
        """
        Retourne le nombre d'abonnés moyen pour les pages.
        """
        if len(self.list_page()) > 0:
            followers = 0
            for p in self.list_page():
                followers += p.get_number_liker()
            return followers / self.number_page()
        
        
    # COMMANDES
            
    def reset_graph(self):
        """
        Remettre tout les informations a vide.
        """
        self._graph = nx.DiGraph()
        self._info = dict()
        
        
    def add_summit(self, x : Summit):
        """
        On ajoute un nouveau sommet sans lien seulement 
        dans le cas ou ce sommet n'existe pas dans le graphe.
        """
        # Dans le cas ou l'on ajoute une page sans avoir ajouter le compte de l'admin
        if isinstance(x, Page):
            if x.get_name_admin() not in self._info:
                self.add_summit(x.get_admin())
            
        if not(x.get_name() in self._info):
            name = x.get_name()
            self._graph.add_node(name) 
            self._info[name] = {
                "account" : x,
                "degrees" : 0,
                "links"   : []
            }
    
    
    def add_arc(self, x : Summit, y : Summit):
        """ 
        On ajoute un nouveau lien entre les sommets x et y et 
        seulement dans le cas ou cette arête n'existe pas dans le graphe.
        """     
        if x in self.list_summit() and y in self.list_summit():
            # Récupération des noms
            xname = x.get_name()
            yname = y.get_name()
            
            # Test de possibilité du lien
            testsLink = self.link_is_possible(x, y)
            
            # Test d'existence du lien x vers y 
            if not((xname, yname) in self._info[xname]["links"]) and testsLink:
                self._graph.add_edge(xname, yname)
                self._info[xname]["degrees"] += 1
                self._info[xname]["links"].append((xname, yname))
                x.add_neighbours_out(y)
                y.add_neighbours_in(x)
        
    
    def add_arc_by_name(self, x : str, y : str):
        self.add_arc(self._info[x]["account"], self._info[y]["account"])
    
    
    def remove_summit(self, x : Summit):
        """
        Supprime un sommet et les connexions associées seulement dans le cas ou x est existant.
        """
        if x.get_name() in self._info:
            
            admin_on = []    
            if isinstance(x, User):
                for i in self.list_page():
                    if i.get_name_admin() == x.get_name():
                        admin_on.append(i)
                        
            if len(admin_on) > 0:
                for i in admin_on:
                    self.remove_summit(i)
                    
            del admin_on
            
            # On récupère les liens existantes 
            links = self.list_links()
            
            # On cible les sommets a éliminer
            list_remove = []
            for i in links:
                if i[0] == x.get_name() or i[1] == x.get_name():
                    list_remove.append(i)
            
            # On supprime les connexions associés au sommet x
            xname = x.get_name()
            for i in list_remove:
                if i[0] == xname:
                    self._info[xname]["degrees"] -= 1
                    self._info[xname]["links"].remove(i)
                    x.remove_neighbours_out(self._info[i[1]]["account"])
                    self._info[i[0]]["account"].remove_neighbours_in(x)
                elif i[1] == xname:
                    self._info[i[0]]["degrees"] -= 1
                    self._info[i[0]]["links"].remove(i)
                    self._info[i[0]]["account"].remove_neighbours_out(self._info[i[1]]["account"])
                    x.remove_neighbours_in(self._info[i[0]]["account"])
            del list_remove
            
            # SUPPRESSION du sommet  
            del self._info[xname]
            self._graph.remove_node(x.get_name())
    
    
    def remove_summit_by_name(self, x : str):
        """
        Supprime un sommet et les connexions associées seulement dans le cas ou x est existant via le nom.
        """
        self.remove_summit(self._info[x]["account"])
    
    
    def remove_arc(self, x : Summit, y : Summit):
        """
        Supprime une connexion existante entre les sommets x et y.
        """
        if (x.get_name(), y.get_name()) in self.list_links():
            self._info[x.get_name()]["degrees"] -= 1
            self._info[x.get_name()]["links"].remove((x.get_name(), y.get_name()))
            self._graph.remove_edge(x.get_name(), y.get_name())
            x.remove_neighbours_out(y)
            y.remove_neighbours_in(x)
    
    
    def remove_arc_by_name(self, x : str, y : str):
        """
        Supprime une connexion existante entre les sommets x et y via leur nom.
        """
        self.remove_arc(self._info[x]["account"], self._info[y]["account"])
    
    
    def write_file(self):
        """
        Ecris dans un fichier une liste d'adjacence qui sera stocké dans un fichier qui se nommera adjacence.txt.
        Si le fichier existe, la réecriture effacera l'ancienne sauvegarde.
        """
        # Ciblons dans l'ordre les comptes utilisateurs et pages
        l = []
        for i in self._info:
            if self.is_user(self._info[i]["account"]):
                l.append("U")
            elif self.is_page(self._info[i]["account"]):
                l.append("P")
                
        # Ecriture
        self._file.writes(self._info, l)
    
    
    def read_file(self):
        """
        Lis le fichier seulement s'il existe un fichier.
        Le fichier sera toujours du nom adjacence.txt.
        """
        # Mise a Zero des élements du graphe
        if len(self._info) != 0:
            self.reset_graph()
        
        # Lecture
        self._file.reads()
        
        # Récupération des résultats
        dico_adj = self._file.adjacency_dict()
        for i in dico_adj:
            
            # Déclaration des sommets
            if dico_adj[i]["type"] == "U":
                f = dico_adj[i]["identity"][0]
                self.add_summit(User(f, i))
            elif dico_adj[i]["type"] == "P":
                n = dico_adj[i]["identity"][2]
                f = dico_adj[i]["identity"][1]
                # Test d'existence de l'utilisateur
                if n in self._info:
                    self.add_summit(Page(i, self._info[n]["account"]))
                else:
                    self.add_summit(Page(i, User(f, n)))
                
        # Déclaration des connexions entre les sommets
        for i in dico_adj:
            for l in dico_adj[i]["connexion"]:
                self.add_arc(self._info[i]["account"], self._info[l]["account"])