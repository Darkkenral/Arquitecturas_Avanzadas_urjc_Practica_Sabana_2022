from random import random
import threading
import itertools
import time
import Simulacion as simulacion
from enum import Enum


class Tipo(Enum):
    Cebra = 'C'
    Hiena = 'H'
    Leon = 'L'


class Animal(threading.Thread):
    '''
    Clase animales, hereda de threads y es la clase padre de todos los animales del juego 

    '''

    def __init__(self, id, sabana: simulacion, tipo, posicion: tuple, manada):
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
        self.vector_movimiento = [
            (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        super().__init__()
        self.id = id
        self.sabana = sabana
        self.tipo = Tipo(tipo)
        self.posicion = posicion
        # CAMBIAR POR UNA CLASE Y UN MUTEX
        self.manada = manada

    def sumatuplas(self, tp_origen: tuple, tp_movimiento: tuple):
        return(tp_origen[0]+tp_movimiento[0], tp_origen[1]+tp_movimiento[1])

    def movimiento(self):
        self.bloquear_casilla(self.posicion)
        list_posiciones_validas = self.get_posiciones_validas(self.posicion)
        long_list = len(list_posiciones_validas)
        if(long_list != 0):
            index = random(0, long_list-1)
            destino = list_posiciones_validas[index]
            list_posiciones_validas.remove(destino)
            for e in list_posiciones_validas:
                self.desbloquear_casilla(e)
            self.sabana.get_mapa().get_casilla(self.posicion).set_animal(None)
            self.desbloquear_casilla(self.posicion)
            self.sabana.get_mapa().get_casilla(destino).set_animal(self)
            self.posicion = destino
            self.desbloquear_casilla(destino)

    def __str__(self):
        return str(self.tipo.value)+str(self.manada)+'-'+str(self.id)

    def get_posiciones_validas(self,posicion: tuple):
        pos_validas=[]
        for movimiento in self.vector_movimiento:
            destino=self.sumatuplas(posicion,movimiento)
            if not(self.esta_bloqueada(destino)) and not(self.esta_ocupada(destino)):
                pos_validas.append(destino)
        return pos_validas

    def esta_ocupada(self,posicion:tuple):
        return self.sabana.get_mapa().get_casilla(posicion).get_animal()is not None
    
    def blockear_casilla(self, posicion: tuple):
        self.sabana.get_mapa().get_casilla(posicion).bloquear()

    def desbloquear_casilla(self, posicion: tuple):
        self.sabana.get_mapa().get_casilla(posicion).desbloquear()

    def esta_bloqueada(self, posicion: tuple):
        return self.sabana.get_mapa().get_casilla(posicion).es_bloqueada()

    # SI CAZO BLOQUEO TODO, LUEGO ELIJO LAS POTENCIALES PRESAS, SUELTO LO QUE NO USO, ME DESPLAZO Y LIBERO LOS MUTEX
    # EN EL MOVIMIENTO HAGO MUTEX EN TODO Y ME MUEVO
    # ID DE LOS ANIMALES AUTOINCREMENTAL.
    # PREGUNTAR A LAS CASILLAS SI TIENEN EL MUTEX ACTIVADO
    # Si una cebra se despierta, y la han cazado hace todo y  crea una nueva cebra y lo matas Peor soy una cebra fantasma
    # Si te cazan no te puedes mover la posicion es nula


class Cebra(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'C', posicion, manada)

    def run(self):
        while True:
            self.movimiento()

            time.sleep(1)

    def __str__(self):
        return 'Cebra'+' '+str(self.manada)


class Carnivoro(Animal):
    def __init__(self, id, sabana: simulacion, tipo, posicion: tuple, manada):
        super().__init__(id, sabana, tipo, posicion, manada)

    def Cazar(self):
        pass


class Leon(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'L', posicion, manada)

    def __str__(self):
        return 'Leon '+str(self.manada)


class Hiena(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'H', posicion, manada)

    def __str__(self):
        return 'Hiena'+' '+str(self.manada)
