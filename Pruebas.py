import numpy as np

matriz = np.zeros((9,5)) #Crear una matriz de 0s
matriz[8][4] = 1
print(matriz)
print(np.flip(matriz,0)) # Darle vuelta a una matriz

"""------Board-------"""
Squaresize = 100

# totalidad de la board
width = numCol * squaresize
heigh = nomFil * squaresize

if event.MOUSEBUTTONDOWN:

col = c
lin = l

c*Squaresize = ubicacion rectangulo

"""---------"""
posx = event.pos[0]
col = int(math.floor(posx/Squaresize)) # le va dar un número entero, que va a ir desde 0 hasta el largo de la matriz
#En mi caso debería restarle el punto desde donde empieza el tablero a posx, porque no empieza desde 0 en x
