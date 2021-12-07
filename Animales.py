
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

    def __init__(self, id, sabana: simulacion, tipo, posicion, manada):
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
            if (self.en_rango(destino) and (self.esta_bloqueada(destino) is False) and self.esta_vacia(destino)):
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
        if(posicion[0] <= leng[0]) and (posicion[1] <= leng[1] and (posicion[0] >= 0) and (posicion[1] >= 0)):
            return True
        return False

    def hay_ganador(self):
        return self.sabana.ganador.get_victoria() is True

    def set_posicion(self, posicion):
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
    def __init__(self, id, sabana: simulacion, posicion, manada):
        super().__init__(id, sabana, 'C', posicion, manada)
        self.velocidad = rdm.randint(7, 10)

    def run(self):
        condicion = True
        while (self.hay_ganador() is False) and condicion:
            if self.posicion is None:
                posicion = self.posicion_valida()
                self.bloquear_casilla(posicion)
                nueva_cebra = Cebra(self.id, self.sabana,
                                    posicion, self.manada)
                self.sabana.get_mapa().set_animal(posicion, nueva_cebra)
                self.sabana.nuevas_threads.append(nueva_cebra)
                self.desbloquear_casilla(posicion)

                nueva_cebra.start()
                condicion = False
            else:
                if self.esta_bloqueada(self.posicion) is False:
                    self.movimiento()
                    time.sleep(self.velocidad)

    def posicion_valida(self):
        tope = self.sabana.get_mapa().get_tammapa()

        while True:
            pos_random = (rdm.randint(0, tope[0]), rdm.randint(0, tope[1]))
            if (self.esta_bloqueada(pos_random) is False) and self.esta_vacia(pos_random):
                return pos_random

    def __str__(self):
        return 'Cebra'+' '+str(self.id)+'-'+str(self.manada.id)


class Leon(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'L', posicion, manada)
        self.velocidad = rdm.randint(1, 3)

    def run(self):
        while (self.hay_ganador() is False):
            # self.movimiento()
            self.cazar()
            time.sleep(self.velocidad)

    def cazar(self):
        self.bloquear_casilla(self.posicion)
        posb_movimientos = []
        lista_cebras = []
        lista_hienas = []
        lista_leones = []
        for movimiento in self.vector_movimiento:
            destino = self.sumatuplas(self.posicion, movimiento)
            if (self.en_rango(destino) and (self.esta_bloqueada(destino) is False)):
                self.bloquear_casilla(destino)
                posb_movimientos.append(destino)
                if not self.esta_vacia(destino):
                    if self.get_tipo(destino) == 'L':
                        lista_leones.append(destino)

                    if self.get_tipo(destino) == 'C':
                        lista_cebras.append(destino)

                    if self.get_tipo(destino) == 'H':
                        lista_hienas.append(destino)

        if (len(lista_leones) >= len(lista_hienas)) and len(lista_hienas) > 0:
            # liberar cebrasu casillas que no vaya a mirar
            for cebra in lista_cebras:
                posb_movimientos.remove(cebra)
                self.desbloquear_casilla(cebra)
            for leon in lista_leones:
                posb_movimientos.remove(leon)
            for hiena in lista_hienas:
                posb_movimientos.remove(hiena)
            for movimiento in posb_movimientos:
                self.desbloquear_casilla(movimiento)
            self.cazar_hiena(lista_leones, lista_hienas)

        elif lista_cebras:
            # liberar hienas  u casillas que no vaya a mirar
            for cebra in lista_cebras:
                posb_movimientos.remove(cebra)
            for movimiento in posb_movimientos:
                self.desbloquear_casilla(movimiento)
            self.cazar_cebra(lista_cebras)
        else:
            for hiena in lista_hienas:
                posb_movimientos.remove(hiena)
                self.desbloquear_casilla(hiena)
            if posb_movimientos != []:
                index = rdm.randint(0, len(posb_movimientos)-1)
                destino = posb_movimientos[index]
                posb_movimientos.remove(destino)
                for casilla in posb_movimientos:
                    self.desbloquear_casilla(casilla)
                pos_actual = self.posicion
                self.sabana.get_mapa().get_casilla(pos_actual).set_animal(None)
                self.desbloquear_casilla(pos_actual)
                self.sabana.get_mapa().get_casilla(destino).set_animal(self)
                self.posicion = destino
                self.desbloquear_casilla(destino)

    def cazar_hiena(self, lista_leones: list, lista_hienas: list):
        if len(lista_hienas) > 1:
            index = rdm.randint(0, len(lista_hienas)-1)
        else:
            index = 0
        destino = lista_hienas[index]
        lista_hienas.remove(destino)
        for hiena in lista_hienas:
            self.desbloquear_casilla(hiena)
        for leone in lista_leones:
            self.desbloquear_casilla(leone)
        pos_actual = self.posicion
        self.sabana.get_mapa().set_animal(pos_actual, None)
        self.desbloquear_casilla(pos_actual)
        animal = self.sabana.get_mapa().get_casilla(destino).get_animal()
        animal.set_posicion(None)
        print(str(animal)+"-Cazada")
        self.sabana.get_mapa().set_animal(destino, None)
        self.sabana.get_mapa().set_animal(destino, self)
        self.manada.incremento_contador()
        self.manada.incremento_contador()
        if self.manada.get_contador() > 7:
            self.sabana.ganador.set_ganador(
                'Leon '+str(self.id)+'-'+str(self.manada.id))
        self.posicion = destino
        self.desbloquear_casilla(destino)

    def cazar_cebra(self, lista_cebras: list):
        if len(lista_cebras) > 1:
            index = rdm.randint(0, len(lista_cebras)-1)
        else:
            index = 0
        destino = lista_cebras[index]
        lista_cebras.remove(destino)
        for pos in lista_cebras:
            self.desbloquear_casilla(pos)
         # tenemos a la cebra
        pos_actual = self.posicion
        self.sabana.get_mapa().set_animal(pos_actual, None)
        self.desbloquear_casilla(pos_actual)
        animal = self.sabana.get_mapa().get_casilla(destino).get_animal()
        animal.set_posicion(None)
        print(str(animal)+"-Cazada")
        self.sabana.get_mapa().set_animal(destino, None)
        self.sabana.get_mapa().set_animal(destino, self)
        self.manada.incremento_contador()
        if self.manada.get_contador() > 19:
            self.sabana.ganador.set_ganador(
                'Leon '+str(self.id)+'-'+str(self.manada.id))
        self.posicion = destino
        self.desbloquear_casilla(destino)

    def __str__(self):
        return 'Leon '+str(self.id)+'-'+str(self.manada.id)

    def get_tipo(self, posicion):
        return self.sabana.get_mapa().get_casilla(posicion).get_animal().tipo.value


class Hiena(Animal):
    def __init__(self, id, sabana: simulacion, posicion: tuple, manada):
        super().__init__(id, sabana, 'H', posicion, manada)
        self.velocidad = rdm.randint(4, 6)

    def run(self):
        condicion = True
        while (self.hay_ganador() is False) and condicion:
            if self.posicion is not None:
                if self.esta_bloqueada(self.posicion) is False:
                    self.cazar()
                    time.sleep(self.velocidad)

    def cazar(self):
        self.bloquear_casilla(self.posicion)
        posb_movimientos = []
        lista_cebras = []
        lista_hienas = []

        for movimiento in self.vector_movimiento:
            destino = self.sumatuplas(self.posicion, movimiento)
            if (self.en_rango(destino) and (self.esta_bloqueada(destino) is False)):
                self.bloquear_casilla(destino)
                posb_movimientos.append(destino)
                if not self.esta_vacia(destino):
                    if self.get_tipo(destino) == 'L':
                        posb_movimientos.remove(destino)
                        self.desbloquear_casilla(destino)
                    if self.get_tipo(destino) == 'C':
                        lista_cebras.append(destino)

                    if self.get_tipo(destino) == 'H':
                        lista_hienas.append(destino)

        if not (lista_cebras and lista_hienas):
            for e in lista_hienas:
                posb_movimientos.remove(e)
                self.desbloquear_casilla(e)
            for e in lista_cebras:
                posb_movimientos.remove(e)
                self.desbloquear_casilla(e)
            if posb_movimientos != []:
                index = rdm.randint(0, len(posb_movimientos)-1)
                destino = posb_movimientos[index]
                posb_movimientos.remove(destino)
                for e in posb_movimientos:
                    self.desbloquear_casilla(e)
                pos_actual = self.posicion
                self.sabana.get_mapa().get_casilla(pos_actual).set_animal(None)
                self.desbloquear_casilla(pos_actual)
                self.sabana.get_mapa().get_casilla(destino).set_animal(self)
                self.posicion = destino
                self.desbloquear_casilla(destino)
        else:
            self.cazar_cebra(posb_movimientos, lista_hienas, lista_cebras)

    def cazar_cebra(self, posb_movimientos: list, lista_hienas: list, lista_cebras: list):
        for hiena in lista_hienas:
            posb_movimientos.remove(hiena)
            self.desbloquear_casilla(hiena)
        for cebra in lista_cebras:
            posb_movimientos.remove(cebra)
        for casilla in posb_movimientos:
            self.desbloquear_casilla(casilla)
        if len(lista_cebras) > 1:
            index = rdm.randint(0, len(lista_cebras)-1)
        else:
            index = 0
        destino = lista_cebras[index]
        lista_cebras.remove(destino)
        for pos in lista_cebras:
            self.desbloquear_casilla(pos)
        # tenemos a la cebra
        pos_actual = self.posicion
        self.sabana.get_mapa().set_animal(pos_actual, None)
        self.desbloquear_casilla(pos_actual)
        animal = self.sabana.get_mapa().get_casilla(destino).get_animal()
        animal.set_posicion(None)
        print(str(animal)+"-Cazada")
        self.sabana.get_mapa().set_animal(destino, None)
        self.sabana.get_mapa().set_animal(destino, self)
        self.manada.incremento_contador()
        if self.manada.get_contador() > 7:
            self.sabana.ganador.set_ganador(
                'Hiena'+' '+str(self.id)+'-'+str(self.manada.id))
        self.posicion = destino
        self.desbloquear_casilla(destino)

    def __str__(self):
        return 'Hiena'+' '+str(self.id)+'-'+str(self.manada.id)

    def get_tipo(self, posicion):
        return self.sabana.get_mapa().get_casilla(posicion).get_animal().tipo.value
