import threading
import time
import Animales as animales


class Casilla():
    def __init__(self, animal, f, c):
        self.animal = animal
        self.posicion = (f, c)


class Mapa():

    def __init__(self, f, c):
        Self.mapa = [threading.Lock()] * f
        for e in range(f):
            e.append([threading.Lock()]*c)
        return mapa


class Simulacion():
    def __init__(self, n_columnas=75, n_filas=75, n_manadas=2):
        self.n_manadas = n_manadas
        self.mapa = Mapa(n_columnas, n_filas)
