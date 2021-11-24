import random as rdm
import threading
import time
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
        string = [
            ('--------------------------------------SIMULACION---------------------------------------------------')]
        for e_c in self.matriz_mapa:
            for e_f in e_c:
                string += ['['+e_f.get_animal.__str__+']']
                string += ['\n']
        string += [('--------------------------------------SIMULACION---------------------------------------------------')]

        return ' '.join(string)


class Simulacion():

    def __init__(self, n_columnas=75, n_filas=75, n_animales=100, n_manadas=2):
        self.mapa = Mapa(n_columnas, n_filas)
        self.n_animales = n_animales
        self.n_manadas_total = n_manadas
        self.n_hienas = 1/3*n_animales
        self.n_leones = 1/6*self.n_hienas
        self.n_cebras = n_animales-self.n_leones-self.n_hienas
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
                animales_por_manada = animales_por_manada-1
                dic_animal[manada] = lista_animales
        lista_animales = []
        for _ in n_animal_copia:
            lista_animales.append(self.generar_animal(tipo, manada))
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
        long_mapa=self.mapa.get_tammapa()
        lista_cebras=dic_cebras[1]
        cont_cebras=len(lista_cebras)-1
        cuad_cebra=cont_cebras/2
        #Comocamos las cebras en el tablero
        for c in range(cuad_cebra):
            for f in range(cuad_cebra):
                self.mapa.set_animal((c,f),lista_cebras[cont_cebras])
                cont_cebras=cont_cebras-1
        #Colocamos al resto de animales en el tablero
        for manada, hienas in dic_hienas:
            tope_hienas=len(hienas)-1
            cont_hienas=tope_hienas
            pos_inic=get_pos_valida(tope_hienas)
            for c in range(pos_inic[0],pos_inic[0]+tope_hienas):
                for f in range(pos_inic[1],pos_inic[1]+tope_hienas):
                    self.mapa.set_animal((c,f),hienas[cont_hienas])
                    cont_hienas=cont_hienas-1
                    
        #Abstraer metodo para colocar cada uno de los tipoos de animales. Simplificar codigo
                
        
    def get_pos_valida(self, lista_animales):
        pass


# Una vez acabe el juego se hace un join de todos los hilos del juego y se cierra
# While not ganador se ejecuta el juego
# hacer una clase manada que tenga un mutex en el contador de victoria
