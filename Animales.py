import threading
import itertools
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
    id_animal = itertools.count
    vector_movimiento = [(-1, 1), (0, 1), (1, 1), (1, 0),
                         (1, -1), (0, -1), (-1, -1)]

    def __init__(self, sabana: simulacion, tipo: Tipo, posicion: tuple, manada):
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
        self.tipo = tipo
        self.posicion = posicion
        # CAMBIAR POR UNA CLASE Y UN MUTEX
        self.manada = manada

    def sumatuplas(self, tp_origen: tuple, tp_movimiento: tuple):
        return(tp_origen[0]+tp_movimiento[0], tp_origen[1]+tp_movimiento[1])

    def movimiento(self):
        self.sabana

    def __str__(self):
        return str(self.tipo)+'(ID:'+self.id_animal + ')'+' (M:' + str(self.manada)+')'

    # SI CAZO BLOQUEO TODO, LUEGO ELIJO LAS POTENCIALES PRESAS, SUELTO LO QUE NO USO, ME DESPLAZO Y LIBERO LOS MUTEX
    # EN EL MOVIMIENTO HAGO MUTEX EN TODO Y ME MUEVO
    # ID DE LOS ANIMALES AUTOINCREMENTAL.
    # PREGUNTAR A LAS CASILLAS SI TIENEN EL MUTEX ACTIVADO
    # Si una cebra se despierta, y la han cazado hace todo y  crea una nueva cebra y lo matas Peor soy una cebra fantasma
    # Si te cazan no te puedes mover la posicion es nula


class Cebra(Animal):
    pass


class Leon(Animal):
    pass


class Hiena(Animal):
    pass
