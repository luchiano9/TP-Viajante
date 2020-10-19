#Esto lo usamos para probar la funcion de crossover

cantGenes = 10
pares = [[ [9,8,2,1,7,4,5,10,6,3],[1,2,3,4,5,6,7,8,9,10] ]]

def aplicarCrossoverMutacion(self,pares):
    "Cambiar esta parte del código"

    "2 padres. Primer digito del primer padre se conserva para el hijo. Luego buscar primer digito del segundo padre en el primero"
    "y tomarlo para el hijo. Luego utilizar el digito que esta en la misma posicion pero en el segundo padre, y asi sucesivamente."

    sigPoblacion = []       

    for par in pares:
        if (self.realizar(pCrossover)):            
            for i in range(2):
                index = 0
                numABuscar = int(par[i][0])
                bits = [None]*cantGenes                        #cambiar nombre a bits por recorrido?

                while numABuscar not in bits:
                    bits[index] = numABuscar
                    numABuscar = int(par[abs(i-1)][index])
                    index = par[i].index(numABuscar)

                for j in range(cantGenes):
                    if bits[j] is None:
                        bits[j] = par[abs(i-1)][j]

                sigPoblacion.append(bits)
    return sigPoblacion



print(str(aplicarCrossoverMutacion(pares)))