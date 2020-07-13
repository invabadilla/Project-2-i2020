import numpy as np

##matriz = np.zeros((9,5))
##
##matriz[5][3] = 1
##matriz[5][0] = 1
##matriz[7][3] = 1
##matriz[2][0] = 1
##
##np.save("matrJuego.npy",matriz)
##
##a = np.load("matrJuego.npy")
##
##print(a)

a = 3
b = 4
#Escudero
i = 4
d = 5
#Lenador
e = 3
f = 4
#Canibal
g = 4
h = 5

print(a)

archivo = open("Animal.txt","r")
archivo.seek(0)
a = archivo.read(1)
b = archivo.read(1)
i = archivo.read(1)
d = archivo.read(1)
e = archivo.read(1)
f = archivo.read(1)
g = archivo.read(1)
h = archivo.read(1)

archivo.close()
print(a)
