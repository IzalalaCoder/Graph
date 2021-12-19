# -*- coding: utf-8 -*-

import random
from summit import Summit
from page import Page

# Classe représentant des utilisateurs
class User(Summit):
    """
    Classe représentant des utilisateurs.
    
    cons :
        family -> Nom de famille 
        name -> Prénom
        age -> Age de la personne (randomisé pour plus de réalisme)
    """  
    # CONSTRUCTEUR
    
    def __init__(self, f: str, n: str):
        super().__init__(n)
        self._family = f.replace(' ', '')
        self._age = random.randint(10, 100)
        self._friends = []
        
        
    # REQUETES
    
    def get_family(self):
        """ 
        Retourne le nom de famille de l'utilisateur.
        """
        return self._family
    
    
    def get_age(self):
        """ 
        Retourne l'age de l'utilisateur.
        """
        return self._age

    
    def get_friends(self):
        """
        Retourne la liste des amis de self.
        """
        return self._friends
    
        
    # COMMANDES

    def set_family(self, f : str):
        """
        Modifie le nom de famille de l'utilisateur.
        """
        if f != self._family :
            self._family = f.replace(' ', '')

    
    def set_name(self, n : str):
        """
        Modifie le nom de l'utilisateur.
        """
        if n != super().get_name():
            super().rename_name(n)
            
            
    def add_neighbours_out(self, x):
        if x not in super().list_out_neighbours():
            self._outgoing_neighbours.append(x)
            self.add_friends(x)
    
    
    def add_neighbours_in(self, x):
        if x not in super().list_in_neighbours():
            self._incoming_neighbours.append(x)
            self.add_friends(x)
            
    def add_friends(self, x):
        """
        Ajoute un utilisateur si réciprocité.
        """
        if isinstance(x, self.__class__):
            if x in super().list_in_neighbours() and x in super().list_out_neighbours():
                self._friends.append(x)  
                
                      
    def remove_neighbours_out(self, x):
        if x in super().list_out_neighbours():
            self._outgoing_neighbours.remove(x)
        self.remove_friends(x)
    
    
    def remove_neighbours_in(self, x):
        if x in super().list_in_neighbours():
            self._incoming_neighbours.remove(x)
            self.remove_friends(x)
    
    
    def remove_friends(self, x):
        """
        Retire un utilisateur si non réciprocité.
        
        CAS OU ON RETIRE
            IN ---- OUT
            X
                    X
        
        CAS OU L'ON RETIRE PAS
            IN ---- OUT
            X       X
        """
        if isinstance(x, self.__class__) and x in self._friends: 
            if (x in super().list_in_neighbours() and x not in super().list_out_neighbours()):
                self._friends.remove(x)
            elif (x not in super().list_in_neighbours() and x in super().list_out_neighbours()):
                self._friends.remove(x)