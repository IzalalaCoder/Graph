# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod 

class Summit(ABC):
    """
    Classe représente des Sommets. 
    Elle contient les attributs suivant ->
        - name = le nom
        - outgoing_neighbours = la liste des voisins sortant
                                par défaut liste vide
        - incoming_neighbours = la liste des voisins entrant 
                                par défaut liste vide
    """
    
    # CONSTRUCTEUR
    
    def __init__(self, n : str): 
        self._name = n.replace(' ', '')
        self._outgoing_neighbours = []
        self._incoming_neighbours = []

    # REQUETE 
         
    def list_out_neighbours(self):
        """
        Retourne la liste des voisins sortant.
        """
        return self._outgoing_neighbours
    
    
    def list_in_neighbours(self):
        """
        Retourne la liste des voisins entrant.
        """
        return self._incoming_neighbours
        
    
    def get_name(self): 
        """
        Retourne le nom du sommet.
        """
        return self._name


    # COMMANDES
    
    def rename_name(self, n : str):
        """
        Modifie le nom de famille de l'utilisateur.
        """
        if n != self._name :
            self._name = n.replace(' ', '')
    
    
    @abstractmethod
    def add_neighbours_out(self, x):
        """
        Ajoute le sommet x.
        """
        pass
    
    
    @abstractmethod
    def remove_neighbours_out(self, x):
        """
        Retire le sommet x.
        """
        pass
        
    @abstractmethod
    def add_neighbours_in(self, x):
        """
        Ajoute le sommet x.
        """
        pass
    
    
    @abstractmethod
    def remove_neighbours_in(self, x):
        """
        Retire le sommet x.
        """
        pass