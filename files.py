# -*- coding: utf-8 -*-

import os
import re
from fpdf import FPDF

class Files:
    """
    Cette classe va gérer les manipulations des fichiers.
    Nous avons ici deux attributs 
        -> title = le titre du fichier par défaut adjacence.txt
        -> adj = le dictionnaire qui regroupe toute les informations nécessaire a la création du graphe et
            également celle  de la liste d'adjacence.
                - connexion -> La liste des liens
                - type -> le type du compte
                - identity -> les informations du compte 
    """
    
    # CONSTRUCTEUR
    
    def __init__(self):
        self._title = "adjacence.txt"
        self._adj = dict()
    
    
    # REQUETES
    
    def title(self):
        """ 
        Retourne le titre du fichier.
        """
        return self._title
    
    
    def adjacency_dict(self):
        """
        Retourne la liste d'adjacence.
        """ 
        return self._adj
    
    
    def new_split(self, sep, chain):
        """ 
        Retourne une liste sans les élements qui sont présent dans sep.
        """
        regular = '|'.join(map(re.escape, sep))
        return re.split(regular, chain)
    
    
    def remove_useless(self, l):
        """ 
        Retourne une liste sans les éléments vide ou 'X' qui veut dire pas de liens.
        """
        new_list = []
        index = 0
        for i in l:
            if i == '' or i == 'X':
                continue
            else: 
                new_list.append(i)
        return new_list
    
    
    def is_empty(self):
        """
        Retourne un booléen selon si la liste d'adjacence est vide ou non.
        """
        return len(self._adj) == 0
    
    
    # COMMANDES
    
    def set_title(self, t : str):
        """
        Modifie le titre du fichier seulement s'il est différent de l'ancien titre.
        """
        if t + ".txt" != self._title:
            self._title = "{}.txt".format(t.replace(' ', ''))
    
    
    def reset_files(self):
        """
        Remet le dictionnaire a vide.
        """
        self._adj = dict()
        f = open("files/{}".format(self._title), "w")
        f.close()
        
        
    def open_adjacency_list(self):
        """
        Ouvre le fichier ou stocke la liste d'adjacence.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = "Liste d'adjacence", ln = 5, align = 'C')
        
        # ESPACEMENT
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        pdf.cell(200, 10, txt = "", ln = 5, align = 'C')
        
        is_file = os.path.isfile("files\{}".format(self._title))
        
        if is_file:
            f = open("files\{}".format(self._title))
            
            # Liste 
            pdf.cell(200, 10, txt = "Type - Info - Abonnements ", ln = 10, align = 'L')
            for x in f:
                pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        
        pdf.output("files\Liste_Adjacence.pdf")
        os.startfile('files\Liste_Adjacence.pdf')
        
        
    def reads(self):
        """
        Lire une liste d'adjacence dans un fichier et récupère toute les informations.
        Récupère les données depuis la liste d'adjacence et le stocke dans notre dictionnaire.
        Et enfin lorsque la récupération des données se termine, l'écris dans un fichier à part.
        """
        
        # Ouverture du fichier pour une lecture
        is_file = os.path.isfile("files/{}".format(self._title))
        if is_file:
            f = open("files/{}".format(self._title), "r")
            
            # Récupération des données via la liste d'adjacence écrit sur le fichier
            lignes = f.readlines()
            types = []
            infos = []
            lists = []
            
            # Parcours des différentes lignes 
            for i in lignes:
                info = i.split(" - ")
                separators = ",", "[", "]", "\n", ' '
                
                types.append(info[0]) 
                infos.append(tuple(self.new_split(separators, info[1])))
                lists.append(tuple(self.new_split(separators, info[2])))
            
            # Suppression des données inutile
            linkin = []
            for i in lists:
                x = list(i)
                linkin.append(tuple(self.remove_useless(x)))
            
            inf = []
            for i in infos:
                x = list(i)
                inf.append(tuple(self.remove_useless(x)))
                
            # Suppression des listes existante et qui ne sera plus utilisé
            del(lists)
            del(infos)
            
            # Déclaration des différentes données
            index = len(types)
            i = 0
            while i < index:
                if types[i] == "U":
                    self._adj[inf[i][1]] = {
                        "connexion" : linkin[i],
                        "type" : types[i],
                        "identity" : inf[i]
                    }
                elif types[i] == "P":
                    self._adj[inf[i][0]] = {
                        "connexion" : linkin[i], 
                        "type" : types[i],
                        "identity" : inf[i]
                    }
                i += 1 
                
            # Fermeture du fichier
            f.close()


    def writes(self, d, l):
        """
        Récupère les données du graphe et le stocke dans notre dictionnaire.
        Et enfin lorsque la récupération des données se termine, l'écris dans un fichier à part.
        """
        # Si un dictionnaire est déja plein on le vide
        if not self.is_empty():
            self.reset_files()
        
        # On remplit notre dictionnaire pour en faire une liste d'adjacence
        if d != None and self.is_empty():
            index = 0
            
            # Récupération des données a partir du graphe
            for i in d:
                e = []
                t = ()
                for k in d[i]["links"]:
                    e.append(k[1])
                
                if l[index] == "P":
                    t = (d[i]["account"].get_admin().get_family(), d[i]["account"].get_admin().get_name())
                elif l[index] == "U":
                    t = (d[i]["account"].get_family())
                
                self._adj[i] = {"connexion" : e,
                                "type" : l[index],
                                "identity" : t
                                }
                index += 1
                
        # On crée un fichier au nom de self._title OU on ecrase le fichier du même nom
        f = open("files/{}".format(self._title), "w")
        for i in self._adj:            
            text = "{} - [".format(self._adj[i]["type"])
            
            if self._adj[i]["type"] == "P":
                text += "{}, {}, {}] - [".format(i, d[i]["account"].get_admin().get_family(), d[i]["account"].get_admin().get_name())
            elif self._adj[i]["type"] == "U":
                text += "{}, {}] - [".format(d[i]["account"].get_family(), d[i]["account"].get_name())
            
            # Résultat de liens
            if len(self._adj[i]["connexion"]) == 0:
                text += "X]\n"
            else:
                for k in self._adj[i]["connexion"]:
                    text += k + ", "
                text += "]\n"
            # Ecriture dans le fichier
            f.write(text)
            
        # Fermeture du fichier
        f.close()