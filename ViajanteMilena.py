import numpy as np 
import matplotlib.pyplot as plt 

import pandas as pd
import os


path = 'C:/Users/Luciano/Desktop/elViajante-main/datos.xlsx'
df = pd.read_excel(path) 
# df contiene los datos de ciudades y distancias

recorrido = []
distancias = []
i=0

df = df.set_index('Distancias en kilómetros')  # columna indice

# aca esta hardcodeado la ciudad de inicio, y eliminar la fila de esa ciudad de inicio
# ciudadIni = 'San Luis'
# df = df.drop(['San Luis'])  #elimina fila de la ciudad
# recorrido.append(ciudadIni)

def menu(df=df):
    print("El problema del viajante")
    print("Ingrese el nombre de la ciudad de inicio")
    ciudadIni = input()
    recorrido.append(ciudadIni)
    return ciudadIni

def getRecorrido(ciudadIni,i=i,recorrido=recorrido,distancias=distancias,df=df):
    if i==0:              
        df = df.drop(ciudadIni)     # El bloque de aca es lo unico que se me ocurrio cuando me empezo a dar errores el drop de la ciudad inicial
        i = 1
    if (len(recorrido)==len(df.columns)):  # si entra por true es porque ya termino

        recorrido.append(ciudadIni) 
        recorrido.append(sum(distancias)) 
        
        return recorrido
    else:
        for col in df.columns:
           
            if recorrido[len(recorrido)-1] == col: # busca columna de el ultimo añadido
                masCercana = df[col].idxmin()  # idxmin devuelve el valor minimo de cada columna
                distancias.append(df[col][masCercana])
                recorrido.append(masCercana)
                if (len(recorrido)==len(df.columns)):           #Este bloque es para agregar la distancia al volver a la ciudad de inicio
                    for colu in df.columns:
                        if colu == ciudadIni:
                            distFinal = df[colu][masCercana]
                            distancias.append(distFinal)

                df = df.drop([masCercana])
                getRecorrido(ciudadIni,i,recorrido, distancias, df)                              
                break
                
ciudadIni = menu()               
getRecorrido(ciudadIni)
print("R: ", recorrido)
