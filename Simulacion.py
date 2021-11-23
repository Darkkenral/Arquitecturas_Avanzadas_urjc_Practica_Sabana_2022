import threading
import time
import Animales


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
        self.tam_mapa = (c, f)
        for i_c in range(c):
            self.matriz_mapa.append([])
            for i_f in range(f):
                self.matriz_mapa[i_c].append(Casilla(None, i_c, i_f))

    def get_tammapa(self):
        return self.tam_mapa

    def get_animal(self, posicion: tuple):
        return self.matriz_mapa[posicion[0]][posicion[1]].get_animal()

    def set_animal(self, posicion: tuple, animal):
        self.matriz_mapa[posicion[0]][posicion[1]] = animal

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
        string=[('--------------------------------------SIMULACION---------------------------------------------------')]
        for e_c in self.matriz_mapa:
            for e_f in e_c:
                string+=['['+e_f.get_animal.__str__+']']
                string+= ['\n']
        string+=[('--------------------------------------SIMULACION---------------------------------------------------')]
        
        return ' '.join(string) 


class Simulacion():

    def __init__(self, n_columnas=75, n_filas=75,n_animales=100,n_manadas=2):
        self.n_animales = n_animales
        self.n_manadas = n_manadas
        self.mapa = Mapa(n_columnas, n_filas)
        

    def get_mapa(self):
        return self.mapa

    
# Una vez acabe el juego se hace un join de todos los hilos del juego y se cierra
# While not ganador se ejecuta el juego
# hacer una clase manada que tenga un mutex en el contador de victoria
