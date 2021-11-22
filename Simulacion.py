import threading
import time
from Animales import *


class Casilla():
    def __init__(self, animal, c, f):
        '''
        Constructor de la clase casilla

        Parameters
        ----------
        animal : [Animal]  
            Animal que se ubica en la casilla 
        c : [int]
            [indice de columnas ]
        f : [int]
            [indice de filas]
        '''
        self.animal = animal
        self.posicion = (f, c)
        self.mutex = threading.Lock()

    def get_animal():
        return self.animal

    def get_position():
        return self.posicion

    def get_mutex(args):
        return self.mutex

    def __str__(self):
        return self.animal.__str__()


class Mapa():
    mapa = []

    def __init__(self, c, f):
        '''
        Constructor de la clase mapa

        Parametros
        ----------
        c : [int]
            Numero de columnas de la matriz
        f : [int]
            Numero de filas de la matriz
        '''
        for i_c in range(c):
            self.mapa.append(list())
            for i_f in range(f):
                self.mapa[i_c].append(Casilla(None, i_c, i_f))
    

    def get_Animal(self, posicion: tuple):
        return self.mapa[posicion[0]][posicion[1]].get_animal()

    def set_Animal(self, posicion: tuple, animal: Animal):
        self.mapa[posicion[0]][posicion[1]] = animal

    def delete_Animal(self, posicion: tuple):
        self.mapa[posicion[0]][posicion[1]] = None

    def popAnimal(self, posicion):
        animal = self.get_Animal()
        self.delete_Animal()
        return animal

    def __str__(self):
        pass


class Simulacion():
    def __init__(self, n_columnas=75, n_filas=75, n_manadas=2):
        self.n_manadas = n_manadas
        self.mapa = Mapa(n_columnas, n_filas)
