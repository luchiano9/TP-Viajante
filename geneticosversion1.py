import random
import time
import numpy
import xlsxwriter
from operator import attrgetter
import os
import pandas as pd
import matplotlib.pyplot as plt

"Datos de las ciudades"

#por ahora, esta harcodeado:
cantCiudades = 24

"EJERCICIO: Método de Selección: Ruleta. Método de Crossover: CROSSOVER CICLICO. Método de Mutación: invertida."
"Datos del algoritmo genetico (para distintos ejercicios, a menos que cambie el metodo de crossover y mutacion, solo hay que modificar estos datos y f(x))"
pCrossover = 0.75
pMutacion = 0.05
cantIndividuos = 50
cantGenes = 24
ciclos = 200
tamanoElite = 2


"Variables globales"


class Poblacion:
    def __init__(self,cromosomas):
        self.cromosomas = cromosomas
        
        self.cromMaxCiclo = Cromosoma() #Inicializamos el cromosoma maximo del ciclo un cromosoma con objetivo 0 (para fxMax usamos el objeto del cromosoma maximo)
        self.fxMin = 100
        self.fxSum = 0
        self.fxProm = 0
    
    #Etapa 2: Guardado de datos
    def calcularYSetearDatos(self):
        for cromosoma in self.cromosomas:
            
            #Calculo del fxMax
            if(cromosoma.fx > self.cromMaxCiclo.fx):
                self.cromMaxCiclo = cromosoma

            #Calculo del fxMin
            if(cromosoma.fx < self.fxMin):
                self.fxMin = cromosoma.fx
            
            #Calculo de la suma
            self.fxSum += cromosoma.fx
        
        #Calculo del promedio
        self.fxProm = (self.fxSum/len(self.cromosomas))

        #Calculo del fitness de cada cromosoma
        for cromosoma in self.cromosomas:
            cromosoma.calcularFitness(self.fxSum)

    #Etapa 3: Seleccion
    def seleccionRuleta(self,elitismo):
        individuos = cantIndividuos
        if(elitismo): 
            individuos -= 2

        pares = []
        for i in range(int(individuos/2)):
            pares.append([])
            for j in range(2):
                pares[i].append(random.choices(self.cromosomas,self.getListaFtn())[0])

        return pares

    #Etapa 4: Crossover y mutación

    def aplicarCrossoverMutacion(self,pares):

     "Cambiar esta parte del código"

     "2 padres. Primer digito del primer padre se conserva para el hijo. Luego buscar primer digito del segundo padre en el primero"
     "y tomarlo para el hijo. Luego utilizar el digito que esta en la misma posicion pero en el segundo padre, y asi sucesivamente."

     sigPoblacion = []       

     for par in pares:

            if (self.realizar(pCrossover)):

                for i in range(2):

                    bits = []                           #cambiar nombre a bits por recorrido?
                    bits.append(par[i].bits[0])
                    numAbuscar = int(par[abs(i-1)][0])

                    for j in range(24):
                        if (par[i][j] == numAbuscar):
                            bits[j] = numAbuscar
                            break

                    cromosoma = Cromosoma(bits)
                    sigPoblacion.append(cromosoma)

     return sigPoblacion                        

    #     #Aplica tanto el crossover como la mutacion (solo en caso de que hayan sido aprobados)
    #     sigPoblacion = []
    #     for par in pares:
    #         if(self.realizar(pCrossover)):
    #             puntoCorte = random.randint(0,cantGenes)
    #         else:
    #             puntoCorte = cantGenes
            
    #         for i in range(2):
    #             bits = []
    #             for j in range(puntoCorte):
    #                 bits.append(par[i].bits[j])
    #             for j in range(puntoCorte,cantGenes):
    #                 bits.append(par[abs(i-1)].bits[j])
                
    #             if(self.realizar(pMutacion)):
    #                 puntoAMutar = random.randint(0,cantGenes-1)
    #                 bits[puntoAMutar] = abs(bits[puntoAMutar]-1)

    #             cromosoma = Cromosoma(bits)

    #             sigPoblacion.append(cromosoma)
    #     return sigPoblacion


    def realizar(self,probabilidadTrue):
        #Recibe una probabilidad para realizar algo y devuelve True si se debe realizar o False si no (usado para decidir crossover y mutacion)
        return (random.choices([0,1],[1-probabilidadTrue,probabilidadTrue])[0] == 1)

    #Helpers
    def aplicarElitismo(self,tamanoElite):
        cromosomasElite = []
        for i in range(tamanoElite):
            unMaximo = max(self.cromosomas,key=attrgetter('ftn')) #Sacamos el cromosoma con mayor fitness

            #Lo eliminamos de los cromosomas de la pobl actual y a la vez lo asignamos a la lista de elite (pop elimina el objeto y a su vez lo devuelve)
            cromosomasElite.append(self.cromosomas.pop(self.cromosomas.index(unMaximo))) 
        
        return cromosomasElite
    def getListaFtn(self):
        listaFtn = []
        for cromosoma in self.cromosomas:
            listaFtn.append(cromosoma.ftn)
        return listaFtn

class Cromosoma:
    def __init__(self,bits=None):
        #Para el cromosoma maximo inicial, lo inicializamos con bits = None, en ese caso lo unico que nos interesa es el Fx para luego poder compararlo
        if(bits != None):
            self.bits = bits
            self.x = 1
            self.fx = self.f()
            self.ftn = 0
        else:
            self.fx = 0
    
    def calcularFitness(self,sumaFx):
        self.ftn = (self.fx/sumaFx)

    def f(self):
        #Evalua la x del cromosoma en una funcion
        return (self.x/(pow(2,30) - 1))
    
    def getBinario(self):
        #Concatena en un string todos los elementos del cromosoma (genes) y los devuelve
        binario = ""
        for gen in self.bits:
            binario += str(gen)

        return binario

def empezar():
    global poblacion,cromosomaMaximoCorrida
    #Inicializaciones
   
    cromosomaMaximoCorrida = Cromosoma() #Inicializamos el cromosoma maximo como un cromosoma con objetivo 0
    elitismo = preguntarElitismo()
    poblacion = Poblacion(getPoblacionInicial())

    print("Comenzando algoritmo con "+str(ciclos)+" ciclos solicitados")

    for i in range(ciclos):
        print()
        print()
        sigCromosomas = [] #Lista de cromosomas siguientes (utilizados cuando se activa elitismo)
        poblacion.calcularYSetearDatos() 

        #Actualizacion del cromosoma maximo de la corrida
        if(poblacion.cromMaxCiclo.fx > cromosomaMaximoCorrida.fx):
            cromosomaMaximoCorrida = poblacion.cromMaxCiclo

        if(elitismo):
            #Sacamos los cromosomas con mejor fitness
            sigCromosomas = poblacion.aplicarElitismo(tamanoElite)

        pares = poblacion.seleccionRuleta(elitismo)

        #Final del ciclo actual
       
        finCiclo(i+1) 

        poblacion = Poblacion(poblacion.aplicarCrossoverMutacion(pares))
        poblacion.cromosomas += sigCromosomas #Si hay elitismo, sigCromosomas va a tener cromosomas y aca se agregan, sino va a estar vacio y no se va a agregar nada 

    
  

#Etapa 1: Generación de la población inicial
def getPoblacionInicial():
    cromosomas = []
    for bits in generarPoblacionInicial():
        cromosomas.append(Cromosoma(bits))
    return cromosomas
def generarPoblacionInicial():
    return [generarCromosomaInicial() for i in range(cantIndividuos)]
def generarCromosomaInicial():
    return [random.sample(range(1,24),23) for i in range(cantGenes)]   

#Etapa 5: Mensaje final con los datos de la generacion
def finCiclo(numCiclo):
    #Muestra los datos finales de la generacion que acaba de finalizar
    print("CICLO "+str(numCiclo)+" COMPLETADO. Datos del mismo:")
    print("FX --> SUMA = "+str(poblacion.fxSum)+" - VALOR MAXIMO = "+str(poblacion.cromMaxCiclo.fx)+" - VALOR MINIMO = "+str(poblacion.fxMin)+" - VALOR PROMEDIO = "+str(poblacion.fxProm))
    print("CROMOSOMA MAXIMO --> "+str(poblacion.cromMaxCiclo.bits))

    if(numCiclo == ciclos):
        print("Algoritmo finalizado: se cumplieron los ciclos solicitados")
        print("Cromosoma maximo de toda la corrida: "+str(cromosomaMaximoCorrida.bits))
        print("Funcion objetivo del cromosoma maximo de toda la corrida: "+str(cromosomaMaximoCorrida.fx))

#Helpers
def esperarEntrada():
    #Pide un input para continuar la ejecucion del algoritmo
    print("Presione enter para continuar")
    input()

def ingresarOpcion(min,max):
    resp = -1
    while(resp < min or resp > max):
        try:
            resp = int(input())
        except:
            print("Entrada no valida")
            resp = -1
    return resp

def preguntarElitismo():
    print("Desea incluir elitismo en el algoritmo? (0 no, 1 si)")
    return (ingresarOpcion(0,1) == 1)

empezar()


# 1 = Cdad. de Bs.As
# 2 = Córdoba
# 3 = Corrientes
# 4 = Formosa
# 5 = La Plata
# 6 = La Rioja
# 7 = Mendoza
# 8 = Neuquén
# 9 = Paraná
# 10 = Posadas
# 11 = Rawson
# 12 = Resistencia
# 13 = Río Gallegos
# 14 = S.F.d.V.d. Catamarca
# 15 = S.M de Tucumán
# 16 = S.S de Jujuy
# 17 = Salta
# 18 = San Juan
# 19 = San Luis
# 20 = Santa Fe
# 21 = Santa Rosa
# 22 = Sgo. Del Estero
# 23 = Ushuaia
# 24 = Viedma
