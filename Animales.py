import threading
import time
import Simulacion as simulacion
from enum import Enum


class Tipo(Enum):
    cebra = 'Cebra'
    hiena = 'Hiena'
    leon = 'Leon'


class Animal(threading.Thread):
    '''
    Clase animales, hereda de threads y es la clase padre de todos los animales del juego 

    '''

    def __init__(self, sabana: simulacion, threadID: int, tipo: Tipo, posicion: tuple, manada):
        '''[summary]

        Parameters
        ----------
        sabana : simulacion
            [description]
        threadID : int
            [description]
        tipo : Tipo
            [description]
        posicion : tuple
            [description]
        manada : [type]
            [description]
        '''
        self.sabana = sabana
        self.threadID = threadID
        self.tipo = tipo
        self.posicion = posicion
        self.manada = manada
    
    def __str__(self):
        return str(self.tipo)+' (M:' +str(self.manada)+')'