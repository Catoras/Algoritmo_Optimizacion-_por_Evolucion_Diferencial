import copy
import numpy as np
from matplotlib import pyplot as plt

import rosenbrock
import sphere
import rastrigin
import quartic

class Individuo:
    def __init__(self, solucion):
        self._solucion = solucion
        self._fitness = np.inf

class DEO:
    def __init__(self, cantidad_individuos, dimensiones, F, Cr, problema, generaciones):
        self._cantidad_individuos = cantidad_individuos
        self._dimensiones = dimensiones
        self._Cr = Cr
        self._F = F
        self._problema = problema
        self._generaciones = generaciones
        self._individuosX = []
        self._individuosV = []
        self._individuosU = []
        self._rango = self._problema.MAX_VALUE - self._problema.MIN_VALUE
        self._mejor = np.inf

    def crearIndividuos(self):
        for i in range(self._cantidad_individuos):
            solucion = np.random.random(size = self._dimensiones) * self._rango + self._problema.MIN_VALUE
            individuo = Individuo(solucion)
            individuo._fitness = self._problema.fitness(individuo._solucion)
            self._individuosX.append(individuo)
            self._individuosV.append(Individuo(np.empty(self._dimensiones)))
            self._individuosU.append(Individuo(np.empty(self._dimensiones)))

    def mejorIndividuo(self):
        for i in self._individuosX:
            fitness = self._problema.fitness(i._solucion)
            if fitness < self._mejor:
                self._mejor = fitness

    def run(self): 
        mejoresHistoricos = []                    
        self.crearIndividuos()  
        self.mejorIndividuo()      
        num_generacion = 0
        while(num_generacion <= self._generaciones):
            for i in range(self._cantidad_individuos):

                r1 = np.random.randint(self._cantidad_individuos)
                while(r1 == i):
                    r1 = np.random.randint(self._cantidad_individuos)

                r2 = np.random.randint(self._cantidad_individuos)
                while(r2 == i or r2 == r1):
                    r2 = np.random.randint(self._cantidad_individuos)

                r3 = np.random.randint(self._cantidad_individuos)
                while(r3 == i or r3 == r1 or r3 == r2):
                    r3 = np.random.randint(self._cantidad_individuos)

                self._individuosV[r1]._solucion = self._individuosX[r1]._solucion + self._F * (self._individuosX[r2]._solucion - self._individuosX[r3]._solucion)

                jrand = np.random.randint(self._dimensiones)  
                
                for j in range(self._dimensiones):
                    if (np.random.random() < self._Cr or j == jrand):
                        self._individuosU[i]._solucion[j] = self._individuosV[i]._solucion[j]
                    else:
                        self._individuosU[i]._solucion[j] = self._individuosX[i]._solucion[j]

            for i in range(self._cantidad_individuos):
                self._individuosU[i]._fitness = self._problema.fitness(self._individuosU[i]._solucion)
                self._individuosV[i]._fitness = self._problema.fitness(self._individuosV[i]._solucion)
                if self._individuosU[i]._fitness < self._individuosX[i]._fitness:
                    self._individuosX[i]._solucion = self._individuosU[i]._solucion
                    self._individuosX[i]._fitness = self._individuosU[i]._fitness
            
                if(self._individuosX[i]._fitness < self._mejor):
                    self._mejor = self._individuosX[i]._fitness
                    
            if num_generacion % 100 == 0:
                print('Generación ', num_generacion, ':', self._mejor)
                mejoresHistoricos.append(self._mejor)
            num_generacion += 1 
        return mejoresHistoricos      



def main():
    titulo = ""

    print("1.- Sphere")
    print("2.- Rosenbrock")
    print("3.- Rastrigin")
    print("4.- Quartic")
    opc = input("Seleccione que funcion desea realizar: ")

    if opc == "1":
        titulo = "Sphere"
        print("Ejecutando funcion Sphere")
        func = sphere.Sphere()

    elif opc == "2":
        titulo = "Rosenbrock"
        print("Ejecutando funcion Rosenbrock")
        func = rosenbrock.Rosenbrock()

    elif opc == "3":
        titulo = "Rastrigin"
        print("Ejecutando funcion Rastrigin")
        func = rastrigin.Rastrigin()

    else:
        titulo = "Quartic"
        print("Ejecutando funcion Quartic")
        func = quartic.Quartic()

    dimension = 2
    promedios_matriz =[]
    x = np.arange(0, 2001, 100)

    while dimension<=8:
        mejores_matriz = []
        print(f"{dimension} dimensiones")
        for i in range(5):
            print(f"Ejecucion {i+1}")

            deo = DEO(40, dimension, 0.6, 0.7, func, 2000)
            mejor_array = deo.run()

            mejores_matriz.append([abs(ele) for ele in mejor_array])

        promedio_mejores = np.mean(mejores_matriz, axis = 0)
        promedios_matriz.append(promedio_mejores)
        plt.plot(x,promedio_mejores)
        plt.title(f"{dimension} dimensiones")
        plt.show()
        dimension*=2

    for array in promedios_matriz:
        plt.plot(x,array)

    plt.title(titulo)
    plt.legend(["2 Dimensiones", "4 Dimensiones", "8 Dimensiones"])
    plt.show()

if  __name__ == '__main__':
    main()
