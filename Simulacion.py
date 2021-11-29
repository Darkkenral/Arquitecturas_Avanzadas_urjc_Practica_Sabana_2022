import random as rdm
import threading
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

    def set_animal(self, animal):
        
        self.animal = animal

    def get_mutex(self):
        return self.mutex

    def __str__(self):
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
        for i_c in range(0, c):
            self.matriz_mapa.append([])
            for i_f in range(f):
                self.matriz_mapa[i_c].append(Casilla(None, i_c, i_f))

    def get_tammapa(self):
        return self.tam_mapa

    def get_animal(self, posicion: tuple):
        return self.matriz_mapa[posicion[0]][posicion[1]].get_animal()

    def casilla_es_vacia(self, posicion: tuple):
        return self.get_animal(posicion) == None

    def set_animal(self, posicion: tuple, animal):
        self.matriz_mapa[posicion[0]][posicion[1]].set_animal(animal)

    def delete_animal(self, posicion: tuple):
        self.matriz_mapa[posicion[0]][posicion[1]] = None

    def pop_animal(self, posicion):
        animal = self.get_animal(posicion)
        self.delete_animal(posicion)
        return animal

    def __str__(self):
        '''
            Genera el to string del mapa completo.
        '''
        string = [
            ('--------------------------------------SIMULACION---------------------------------------------------')]
        string += ['\n']
        for e_c in range(self.tam_mapa[0]):
            aux = []
            for e_f in range(self.tam_mapa[1]):
                aux += ['['+str(self.matriz_mapa[e_c]
                                [e_f].get_animal())+']']
            aux += ['\n']
            string += ' '.join(aux)
        string += ['\n']
        string += [('--------------------------------------SIMULACION---------------------------------------------------')]

        return ''.join(string)


class Simulacion():

    def __init__(self, n_columnas=20, n_filas=20, n_animales=20, n_manadas=2):
        self.mapa = Mapa(n_columnas, n_filas)
        self.n_animales = n_animales
        self.n_manadas_total = n_manadas
        self.n_hienas = int(n_animales/3)
        self.n_leones = int(self.n_hienas/6)
        self.n_cebras = self.n_animales-(self.n_leones+self.n_hienas)
        aux = rdm.randint(1, n_manadas-1)
        self.n_manadas_leones = aux
        self.n_manadas_hienas = n_manadas - aux
        self.n_manadas_cebra = 1
        self.dic_leones = self.generar_diccionario(
            self.n_leones, self.n_manadas_leones, 'L')
        self.dic_hienas = self. generar_diccionario(
            self.n_hienas, self.n_manadas_hienas, 'H')
        self.dic_cebras = self.generar_diccionario(
            self.n_cebras, self.n_manadas_cebra, 'C')
        self.colocar_animales(
            self.dic_cebras, self.dic_hienas, self.dic_leones)

    def run(self):
        '''Por el momento solo imprime el tablero actual, faltan cosas por crear
        '''
        while True:
            self.clear()
            print (self)
            time.sleep(1)

    
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
        n_animal_copia = n_animal
        for manada in range(n_manadas_animal-1):
            animales_por_manada = rdm.randint(1, n_animal_copia)
            n_animal_copia = n_animal_copia-animales_por_manada
            lista_animales = []
            while n_animal_copia > 1 and animales_por_manada > 0:
                lista_animales.append(self.generar_animal(tipo, manada))
                animales_por_manada -= 1
                dic_animal[manada] = lista_animales
        lista_animales = []
        for _ in range(n_animal_copia):
            lista_animales.append(
                self.generar_animal(tipo, n_manadas_animal-1))
        dic_animal[n_manadas_animal] = lista_animales
        return dic_animal

    def generar_animal(self, tipo: str, manada: int):
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
        if(tipo == 'L'):
            return animales.Leon(self, tipo, None, manada)
        if(tipo == 'H'):
            return animales.Leon(self, tipo, None, manada)
        return animales.Cebra(self, tipo, None, manada)

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

        for manada, animales in dic_animales.items():
            tope_lista = len(animales)
            if tope_lista !=1:
                tope_cuadricula = int(tope_lista/2)
            else:
                tope_cuadricula = tope_lista
            pos_inic = self.get_pos__ini_valida(tope_lista)
            print(tope_lista)
            print(tope_cuadricula)
            c = pos_inic[0]
            f = pos_inic[1]
            for a in animales:
                self.mapa.set_animal((c, f), a)
                c += 1
                if((c % tope_cuadricula) == 0):
                    c = pos_inic[0]
                    f += 1
           


    def get_pos__ini_valida(self, long_lista_animales):
        max_leng = self.mapa.get_tammapa()
        reintentar = True
        vacia = True
        while (reintentar):
            posicion = (rdm.randint(0, max_leng[0]-1),
                        rdm.randint(0, max_leng[1]-1))
            if self.mapa.casilla_es_vacia(posicion):
                if long_lista_animales==1:
                    return posicion
                c = posicion[0]
                top_c = c + int(long_lista_animales/2)
                f = posicion[1]
                if (top_c <= max_leng[0]-1):
                    vacia = True
                    while(c <= top_c) and (vacia):
                        if not self.mapa.casilla_es_vacia((c, f)):
                            vacia = False
                        if (f >= max_leng[1]-1):
                            vacia=False
                        c += 1
                        if((c % top_c) == 0):
                            
                            f += 1
                    if vacia is True:
                        return posicion
        return posicion

    def __str__(self):
        return str(self.mapa)+'\n'+' Numero de manadas activas: ' + str(self.n_manadas_total) + '\n' + ' Manadas de Leones: '+ str(self.n_manadas_leones)+' Numero de Leones: ' +  str(self.n_leones) +\
             ' Manadas de Hienas: '+ str(self.n_manadas_hienas)+' Numero de Hienas: ' +  str(self.n_hienas) + \
            ' Manadas de Cebras: '+ str(self.n_manadas_hienas)+' Numero de cebras: ' +  str(self.n_cebras)
    
    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


# Una vez acabe el juego se hace un join de todos los hilos del juego y se cierra
# While not ganador se ejecuta el juego
# hacer una clase manada que tenga un mutex en el contador de victoria
