import threading
import time
import Simulacion as simulacion
from enum import Enum


class Tipo(Enum):
    cebra = 'Cebra'
    hiena = 'Hiena'
    leon = 'Leon'


class Animales(threading.Thread):
    def __init__(self, sabana: simulacion, threadID, tipo: Tipo, posicion: tuple, manada):
        self.sabana = sabana
        self.threadID = threadID
        self.tipo = tipo
        self.posicion = posicion
        self.manada = manada
