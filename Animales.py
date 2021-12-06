
import random as rdm
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
        if list_posiciones_validas:
            index = rdm.randint(0, long_list-1)
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
        return str(self.tipo.value)+str(self.manada.id)+'-'+str(self.id)

    def get_posiciones_validas(self, posicion: tuple):
        pos_validas = []
        for movimiento in self.vector_movimiento:
            destino = self.sumatuplas(posicion, movimiento)
            if ((not self.esta_bloqueada(destino)) and self.esta_vacia(destino) and self.en_rango(destino)):
                pos_validas.append(destino)
                self.bloquear_casilla(destino)
        return pos_validas

    def esta_vacia(self, posicion: tuple):
        animal = self.sabana.get_mapa().get_animal(posicion)
        if animal is None:
            return True
        return False

    def bloquear_casilla(self, posicion: tuple):
        self.sabana.get_mapa().get_casilla(posicion).bloquear()

    def desbloquear_casilla(self, posicion: tuple):
        self.sabana.get_mapa().get_casilla(posicion).desbloquear()

    def en_rango(self, posicion: tuple):
        leng = self.sabana.get_mapa().get_tammapa()
        if(posicion[0] < leng[0]) and (posicion[1] < leng[1]):
            return True
        return False

    def hay_ganador(self):
        return self.sabana.ganador.get_victoria() == True

    def set_posicion(self, posicion: tuple):
        self.posicion = posicion

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
        self.velocidad = rdm.randint(7, 10)

    def run(self):
        if self.posicion != None:
            self.movimiento()
            time.sleep(self.velocidad)

    def __str__(self):
        return 'Cebra'+' '+str(self.id)+'-'+str(self.manada.id)


class Leon(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'L', posicion, manada)
        self.velocidad = rdm.randint(1, 3)

    def run(self):
        while not self.hay_ganador():
            self.movimiento()
            time.sleep(self.velocidad)

    def __str__(self):
        return 'Leon '+str(self.id)+'-'+str(self.manada.id)


class Hiena(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'H', posicion, manada)
        self.velocidad = rdm.randint(4, 6)

    def run(self):
        while not self.hay_ganador():
            if self.posicion != None:
                self.cazar()
                time.sleep(self.velocidad)

    def cazar(self):
        self.bloquear_casilla(self.posicion)
        posb_movimientos = []
        moverme = True
        hay_hienas = False
        hay_cebras = False

        for movimiento in self.vector_movimiento:
            destino = self.sumatuplas(self.posicion, movimiento)
            if ((not self.esta_bloqueada(destino)) and self.en_rango(destino)):
                self.bloquear_casilla(destino)
                posb_movimientos.append(destino)
        lista_cebras = []
        lista_hienas = []
        for casilla in posb_movimientos:
            if not self.esta_vacia(casilla):
                if self.get_tipo(casilla) == 'L':
                    self.desbloquear_casilla(casilla)
                    posb_movimientos.remove(casilla)
                if self.get_tipo(casilla) == 'C':
                    lista_cebras.append(casilla)
                    hay_cebras = True
                if self.get_tipo(casilla) == 'H':
                    lista_hienas.append(casilla)
                    hay_hienas = True
        if hay_hienas and hay_cebras:
            self.cazar_cebra(posb_movimientos, lista_hienas)
        else:
            for e in lista_hienas:
                self.desbloquear_casilla(e)
            for e in lista_cebras:
                self.desbloquear_casilla(e)
            for e in lista_hienas:
                posb_movimientos.remove(e)
            for e in lista_cebras:
                posb_movimientos.remove(e)

            if posb_movimientos != []:
                index = rdm.randint(0, len(posb_movimientos)-1)
                destino = posb_movimientos[index]
                self.sabana.get_mapa().get_casilla(self.posicion).set_animal(None)
                self.desbloquear_casilla(self.posicion)
                self.sabana.get_mapa().get_casilla(destino).set_animal(self)
                self.posicion = destino
                self.desbloquear_casilla(destino)

    def cazar_cebra(self, posb_movimientos: list, lista_hienas: list):
        for hiena in lista_hienas:
            posb_movimientos.remove(hiena)
        for hiena in lista_hienas:
            self.desbloquear_casilla(hiena)
        index = rdm.randint(0, len(posb_movimientos)-1)
        destino = posb_movimientos[index]
        posb_movimientos.remove(destino)
        for pos in posb_movimientos:
            self.desbloquear_casilla(pos)
        self.sabana.get_mapa().get_casilla(self.posicion).set_animal(None)
        self.desbloquear_casilla(self.posicion)
        self.sabana.get_mapa().get_casilla(destino).set_animal(self)
        self.manada.incremento_contador()
        if self.manada.get_contador() > 19:
            self.sabana.ganador.set_ganador(self.__str__)
        self.posicion = destino
        self.desbloquear_casilla(destino)

    def __str__(self):
        return 'Hiena'+' '+str(self.id)+'-'+str(self.manada.id)

    def get_tipo(self, posicion):
        return self.sabana.get_mapa().get_casilla(posicion).get_animal().tipo.value
