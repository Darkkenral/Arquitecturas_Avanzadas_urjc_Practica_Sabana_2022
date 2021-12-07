import random as rdm
import threading
import itertools
import time
import os

import Animales as animales


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

    def get_animal(self):
        return self.animal

    def get_position(self):
        return self.posicion

    def bloquear(self):
        return self.mutex.acquire()

    def desbloquear(self):
        return self.mutex.release()

    def es_bloqueada(self):
        return self.mutex.locked()

    def set_animal(self, animal):
        self.animal = animal

    def get_mutex(self):
        return self.mutex

    def __str__(self):
        if self.animal is None:
            return '            '
        return self.animal.__str__()


class Mapa():
    matriz_mapa = []

    def __init__(self, c, f):
        '''
        Constructor de la clase mapas

        Parametros
        ----------
        c : [int]
            Numero de columnas de la matriz
        f : [int]
            Numero de filas de la matriz
        '''
        self.tam_mapa = (c-1, f-1)
        for i_c in range(c):
            self.matriz_mapa.append([])
            for i_f in range(f):
                self.matriz_mapa[i_c].append(Casilla(None, i_c, i_f))

    def get_tammapa(self):
        return self.tam_mapa

    def get_casilla(self, posicion: tuple):
        return self.matriz_mapa[posicion[0]][posicion[1]]

    def get_animal(self, posicion: tuple):
        return self.get_casilla(posicion).get_animal()

    def casilla_es_vacia(self, posicion: tuple):
        return self.matriz_mapa[posicion[0]][posicion[1]].animal == None

    def set_animal(self, posicion: tuple, animal):
        self.matriz_mapa[posicion[0]][posicion[1]].set_animal(animal)

    def __str__(self):
        '''
            Genera el to string del mapa completo.
        '''
        string = [
            ('--------------------------------------SIMULACION---------------------------------------------------')]
        string += ['\n']
        for e_c in range(self.tam_mapa[0]+1):
            aux = []
            for e_f in range(self.tam_mapa[1]+1):
                aux += ['['+str(self.matriz_mapa[e_c]
                                [e_f])+']']
            aux += ['\n']
            string += ' '.join(aux)
        string += ['\n']
        string += [('--------------------------------------SIMULACION---------------------------------------------------')]

        return ''.join(string)


class Manada():
    def __init__(self, id: int):
        self.id = id
        self._contador_ = 0
        self.valor_Contador = 0
        self.mutex = threading.Lock()

    def incremento_contador(self):
        self.bloquear()
        self.valor_Contador += 1
        self.desbloquear()

    def get_contador(self):
        return self.valor_Contador

    def bloquear(self):
        self.mutex.acquire()

    def desbloquear(self):
        self.mutex.release()


class Ganador():
    def __init__(self):
        self.nombre = ""
        self.victoria = False
        self.mutex = threading.Lock()

    def set_ganador(self, nombre: str):
        self.bloquear()
        self.victoria = True
        self.nombre = nombre
        self.desbloquear()

    def bloquear(self):
        self.mutex.acquire()

    def desbloquear(self):
        self.mutex.release()

    def esta_bloqueado(self):
        return self.mutex.locked()

    def get_victoria(self):
        return self.victoria

    def __str__(self):
        return str(self.nombre) + ' HA GANADO EL JUEGO'


class Simulacion():

    def __init__(self, n_columnas=10, n_filas=10, n_animales=60, n_manadas=5):
        self.mapa = Mapa(n_columnas, n_filas)
        self.n_animales = n_animales
        self.ids_animal = itertools.count(1000)
        self.n_manadas_total = n_manadas
        self.n_hienas = int(n_animales/3)
        self.n_leones = int(self.n_hienas/6)
        self.n_cebras = self.n_animales-(self.n_leones+self.n_hienas)
        aux = rdm.randint(1, n_manadas-1)
        self.n_manadas_leones = aux
        self.n_manadas_hienas = n_manadas - aux
        self.n_manadas_cebra = 1
        self.ganador = Ganador()
        self.dic_leones = self.generar_diccionario(
            self.n_leones, self.n_manadas_leones, 'L')
        self.dic_hienas = self. generar_diccionario(
            self.n_hienas, self.n_manadas_hienas, 'H')
        self.dic_cebras = self.generar_diccionario(
            self.n_cebras, self.n_manadas_cebra, 'C')
        self.colocar_animales(
            self.dic_cebras, self.dic_hienas, self.dic_leones)
        self.nuevas_threads = []

    def inicialzar_threads(self):
        self.inicializar_diccionario(self.dic_cebras)
        self.inicializar_diccionario(self.dic_hienas)
        self.inicializar_diccionario(self.dic_leones)

    def finalizar_threads(self):

        self.finalizar_diccionario(self.dic_leones)
        self.finalizar_diccionario(self.dic_hienas)
        self.finalizar_diccionario(self.dic_cebras)
        for thread in self.nuevas_threads:
            while thread.is_alive():
                thread.join()

    def finalizar_diccionario(self, dic_canimal: dict):
        for manada in dic_canimal.keys():
            animales = dic_canimal[manada]
            for animal in animales:
                while animal.is_alive():
                    animal.join()

    def inicializar_diccionario(self, dic_canimal: dict):
        for manada in dic_canimal.keys():
            animales = dic_canimal[manada]
            for animal in animales:
                animal.start()

    def run(self):
        '''Por el momento solo imprime el tablero actual, faltan cosas por crear
        '''
        t_print = threading.Thread(target=self.print_table)
        t_print.start()
        self.inicialzar_threads()
        self.finalizar_threads()
        while t_print.is_alive():
            t_print.join()
        print(str(self.ganador))
        # aqui iria la variable ganador

    def get_mapa(self):
        return self.mapa

    def generar_diccionario(self, n_animal, n_manadas_animal, tipo):
        '''
        Genera un diccionario con las manadas como claves y las listas de animales de cada manada como valor de la

        Parameters
        ----------
        n_animal : [int]
            [Numero de animales pertenecientes a un tipo]
        n_manadas_animal : [int]
            [Numero de las manadas que hay para este animal]
        tipo : [str]
            [String que codifica el tipo de animal]
        Returns
        -------
        [Dic]
            [Diccionaro generado]
        '''
        dic_animal = {}
        # genero la lista vacia
        cont_animal_restantes = n_animal
        cont_manadas_animal = n_manadas_animal
        while cont_manadas_animal > 0:

            # de 0 a n-1, 0 1 recorro las manadas
            objeto_manada = Manada(cont_manadas_animal)
            cont_manadas_animal -= 1
            # genero un unumero random de la lista
            if cont_animal_restantes >= 1:
                animales_por_manada = rdm.randint(1, cont_animal_restantes)
            else:
                animales_por_manada = 1
            cont_animal_restantes = cont_animal_restantes-animales_por_manada
            # lo resto para llevar la cuenta
            lista_animales = []
            while animales_por_manada > 0:
                lista_animales.append(self.generar_animal(tipo, objeto_manada))
                animales_por_manada -= 1
                dic_animal[objeto_manada] = lista_animales
        if cont_animal_restantes > 0:
            objeto_manada_final = list(dic_animal.keys())[-1]
            while cont_animal_restantes > 0:
                dic_animal[objeto_manada_final].append(
                    self.generar_animal(tipo, objeto_manada_final))
                cont_animal_restantes -= 1

        return dic_animal

    def generar_animal(self, tipo: str, manada: Manada):
        '''
        Dado un tipo y una manada genera un objeto animal de dicho tipo y dicha manada

        Parameters
        ----------
        tipo : str
            [Tipo de animal a generar]
        manada : int
            [Manada a la que pertenece el animal]
        Returns
        -------
        [Animal]
            [Objeto del animal correspondiente]
        '''
        id = next(self.ids_animal)
        if(tipo == 'L'):
            return animales.Leon(id, self, None, manada)
        if(tipo == 'H'):
            return animales.Hiena(id, self, None, manada)
        return animales.Cebra(id, self, None, manada)

    def colocar_animales(self, dic_cebras, dic_hienas, dic_leones):
        '''
        Coloca los animales de manera aleatoria en el mapa.

        Parameters
        ----------
        dic_cebras : [Dict]
            [description]
        dic_hienas : [Dict]
            [description]
        dic_leones : [Dict]
            [description]
        '''

        self.colocar_manadas(dic_cebras)
        self.colocar_manadas(dic_hienas)
        self.colocar_manadas(dic_leones)

    def colocar_manadas(self, dic_animales: dict):
        '''
        Dado un diccionario con todos los animales coloca cada una de las manadas en un punto aleatorio formando un cuadrado

        Parameters
        ----------
        dic_animales : dict
            [description]
        '''
        print()
        for manada in dic_animales.keys():
            animales = dic_animales[manada]
            print(len(animales))
            vector_esquinas = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
            posicion_inicial = self.get_pos__ini_valida()
            es_vacia = True
            lista_pos_validas = []
            for animal in animales:

                if lista_pos_validas == []:
                    while lista_pos_validas == []:
                        lista_pos_validas = self.get_lista_pos_validas(
                            posicion_inicial, vector_esquinas)
                        vector_esquinas = self.incremento_vector(
                            vector_esquinas)
                pos_valida = lista_pos_validas.pop(0)
                self.get_mapa().get_casilla(pos_valida).set_animal(animal)
                animal.set_posicion(pos_valida)

    def incremento_vector(self, vector_esquinas: list):

        izq_superior = vector_esquinas[0]
        der_superior = vector_esquinas[1]
        izq_inferior = vector_esquinas[2]
        der_inferior = vector_esquinas[3]
        izq_superior = (izq_superior[0]-1, izq_superior[1]+1)
        der_superior = (der_superior[0]+1, der_superior[1]+1)
        izq_inferior = (izq_inferior[0]-1, izq_inferior[1]-1)
        der_inferior = (der_inferior[0]+1, der_inferior[1]-1)

        return [izq_superior, der_superior, izq_inferior, der_inferior]

    def get_lista_pos_validas(self, posicion: tuple, vector_esquinas: list):
        list_posiciones_validas = []
        esq_izq_sup = self.sumatuplas(posicion, vector_esquinas[0])
        esq_der_sup = self.sumatuplas(posicion, vector_esquinas[1])
        esq_izq_inf = self.sumatuplas(posicion, vector_esquinas[2])
        esq_der_inf = self.sumatuplas(posicion, vector_esquinas[3])

        for x in range(esq_izq_sup[0], esq_der_sup[0]+1):
            temp_pos = (x, esq_izq_sup[1])
            if self.en_rango(temp_pos) is True:
                if self.get_mapa().casilla_es_vacia(temp_pos) is True:
                    list_posiciones_validas.append(temp_pos)

        for x in range(esq_izq_inf[0], esq_der_inf[0]+1):
            temp_pos = (x, esq_izq_inf[1])
            if self.en_rango(temp_pos):
                if self.get_mapa().casilla_es_vacia(temp_pos):
                    list_posiciones_validas.append(temp_pos)

        for y in range(esq_izq_inf[1], esq_izq_sup[1]):
            temp_pos = (esq_izq_sup[0], y)
            if self.en_rango(temp_pos):
                if self.get_mapa().casilla_es_vacia(temp_pos):
                    list_posiciones_validas.append(temp_pos)

        for y in range(esq_der_inf[1], esq_der_sup[1]):
            temp_pos = (esq_izq_sup[0], y)
            if self.en_rango(temp_pos):
                if self.get_mapa().casilla_es_vacia(temp_pos):
                    list_posiciones_validas.append(temp_pos)

        return list(set(list_posiciones_validas))

    def get_pos__ini_valida(self):
        tam_max = self.get_mapa().get_tammapa()
        while True:
            posicion = (rdm.randint(0, tam_max[0]), rdm.randint(0, tam_max[1]))
            if self.get_mapa().get_animal(posicion) is None:
                return posicion

    def sumatuplas(self, tp_origen: tuple, tp_movimiento: tuple):
        return(tp_origen[0]+tp_movimiento[0], tp_origen[1]+tp_movimiento[1])

    def en_rango(self, posicion: tuple):
        leng = self.get_mapa().get_tammapa()
        if(posicion[0] <= leng[0]) and (posicion[1] <= leng[1]) and (posicion[0] >= 0) and (posicion[1] >= 0):
            return True
        return False

    def print_table(self):
        while not self.ganador.get_victoria():
            self.clear()
            print(self)
            time.sleep(1)

    def __str__(self):
        return str(self.mapa)+'\n'+' Numero de manadas activas: ' + str(self.n_manadas_total) + '\n' + ' Manadas de Leones: ' + str(self.n_manadas_leones)+' Numero de Leones: ' + str(self.n_leones) + ' Manadas de Hienas: ' + str(self.n_manadas_hienas)+' Numero de Hienas: ' + str(self.n_hienas) + ' Manadas de Cebras: ' + str(self.n_manadas_hienas) + ' Numero de cebras: ' + str(self.n_cebras)

    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


# Una vez acabe el juego se hace un join de todos los hilos del juego y se cierra
