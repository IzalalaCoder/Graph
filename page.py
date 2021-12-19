# -*- coding: utf-8 -*-

from summit import Summit
# from user import User
# import random

class Page(Summit):
    """
    La classe qui représente le compte de type Page en lui même.
    Cette classe contiendra toutes les informations concernant les comptes de type Page.
    Cette classe hérite de la classe Summit.
    
    @cons:
        name -> nom de la page
        admin -> le compte de la page de type User
        liker ->  le nombre d'abonné sur cette page, par défaut un nombre random
    """
    
    # CONSTRUCTEUR 
    
    def __init__(self, n : str, admin):
        super().__init__(n)
        assert isinstance(admin, Summit) and not(isinstance(admin, Page)),  "Oh no! L'asserion est fausse!"
        self._admin = admin
        # self._number_liker = random.randint(0, 1000000)
        self._number_liker = len(super().list_in_neighbours())
    
    
    # REQUETES

    def get_name_admin(self):
        """
        Retourne le nom de l'administrateur de la page.
        """
        return self._admin.get_name()
    
    
    def get_admin(self):
        """
        Retourne l'administrateur de la page de type User.
        """
        return self._admin
    
    
    def get_number_liker(self):
        """
        Retourne le nombre de compte qui aime la page.
        """
        return self._number_liker


    # COMMANDES

    def set_name(self, n : str): 
        """
        Modifie le nom de la page à condition qu'il est différent du précédent.
        """
        if n != super().get_name():
            super().rename_name(n)
    
    
    def set_name_admin(self, n):
        """
        Modifie le nom de l'administrateur de la page.
        """
        self._admin.set_name(n) 
        
        
    def add_neighbours_out(self, x : Summit):
        if x not in super().list_out_neighbours():
            self._outgoing_neighbours.append(x)


    def add_neighbours_in(self, x : Summit):
        if x not in super().list_in_neighbours():
            self._incoming_neighbours.append(x)
            self._number_liker += 1


    def remove_neighbours_in(self, x : Summit):
        if x in super().list_in_neighbours():
            self._incoming_neighbours.remove(x)
            self._number_liker -= 1
    
    
    def remove_neighbours_out(self, x : Summit):
        if x in super().list_out_neighbours():
            self._outgoing_neighbours.remove(x)