import pygame,sys,math
import numpy as np
import random
import time
from pygame import mixer
from random import randint

pygame.init()

#Variables globales
global continuar
jugador = ""
continuar = False
ancho = 900
alto = 700
fila = [145, 180, 220, 260, 300, 340, 375, 415, 435]
columna = [50, 95, 145, 190, 235]
lenadorwalk = False
lenadorattack = False
len_attack = 1
len_walk = 1
reloj = 0

#Colores
MORADO_CLARO = (184,112,204,80)
MORADO_OSCURO = (131,60,150,59)
GRIS = (214,202,252,99)
AMARILLO = (253,218,76,99)
CAFE = (201,184,141,79)

#Diferentes fuentes
fontTitulo = pygame.font.SysFont("Neuropol X Rg", 50)
font = pygame.font.SysFont("Neuropol X Rg", 35)
fontita = pygame.font.SysFont("Comic Sans MC", 30)

#Ventana de Inicio
(width, height) = (900, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.flip() #Mostrar ventana

#Titulo e ícono
pygame.display.set_caption("Avatars vs Rooks")
icon = pygame.image.load("icono.png")
pygame.display.set_icon(icon)

# Variables de tiempo
archivo = open("configuracion.txt","r")
archivo.seek(0)
#Arquero
a = int(archivo.read(1))
b = int(archivo.read(1))
#Escudero
i = int(archivo.read(1))
d = int(archivo.read(1))
#Lenador
e = int(archivo.read(1))
f = int(archivo.read(1))
#Canibal
g = int(archivo.read(1))
h = int(archivo.read(1))
level = int(archivo.read(1))

archivo.close()

#Clase botones
"""
Objeto: Button
Argumentos:
    color = tupla (RGB)
    x = int
    y = int
    width = int
    height = int
    img = variable imagen
    text = str
Metodos:
    draw:
    E: Ventana principal
    S: Despliega el rectangulo que representa el botón
    isOver:
    E: lista de cordenadas del cursor
"""
class Button():
    def __init__(self, color, x, y, width, height, img, tamano,text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.tamano = tamano
        self.text = text
        
        

        #Dibuja el botón en la pantalla
    def draw(self,screen,outline=None):
        #Crea outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        #Despliega imagen en caso de tenerla
        if self.img:
            screen.blit(self.img, (self.x + (self.width//2 - self.img.get_width()//2), self.y +(self.height//2 - self.img.get_height()//2)))
        

        if self.text != '':
            font = pygame.font.SysFont("Comic Sans MS", self.tamano)
            text = font.render(self.text, 1, MORADO_OSCURO)
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

        #Verifica si la posición del mouse está sobre el botón
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
"""
Objeto: Button
Argumentos:
    x = int
    y = int
    width = int
    height = int
    img = variable imagen
    text = str
Metodos:
    draw:
    S: Despliega el rectangulo que representa el botón
    isOver:
    S: Escribe las teclas pulsadas
"""
class Entry():
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self):
        font = pygame.font.SysFont("Neuropol X Rg", 35)
        text = font.render(self.text, 1 , MORADO_OSCURO)
        pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.width ,self.height),0)
        screen.blit(text , (self.x, self.y+2))

    def typing(self, event):
        if len(self.text) < 15:
            self. text += event.unicode
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[0:-2]
            
"""
Función que despliega la ventana principal
"""
def inicio():
    
    #Instancias de botones
    botonPlay = Button(MORADO_CLARO,190-50,100-90,100,70,None, 35,"Play")
    botonContinuar = Button(MORADO_CLARO,190-150,200-90,300,70,None, 35,"Continuar Partida")
    botonSalon = Button(MORADO_CLARO,190-140,300-90,280,70,None, 35,"Salon de la fama")
    botonConfig = Button(MORADO_CLARO,190-115,400-90,230,70,None, 35,"Configuracion")
    botonAyuda = Button(MORADO_CLARO,190-55,500-90,110,70,None, 35,"Ayuda")
    botonCreditos = Button(MORADO_CLARO,190-75,600-90,150,70,None, 35,"Creditos")
    botonExit = Button(MORADO_CLARO,190-40,700-90,80,70,None, 35,"Exit")
    listaBotonesInicio = [botonPlay,botonContinuar,botonSalon,botonConfig,botonAyuda,botonCreditos,botonExit]
    botonArquero = Button(MORADO_CLARO,440,200,80,70,None, 20, "Arquero")
    botonEscudero = Button(MORADO_CLARO,540,200,90,70,None, 20,"Escudero")
    botonLenador = Button(MORADO_CLARO,650,200,80,70,None, 20,"Leñador")
    botonCanibal = Button(MORADO_CLARO,750,200,80,70,None, 20,"Canibal")
    botonAumVel = Button(MORADO_CLARO,385,450,80,70,None, 20,"Menos")
    botonDismVel = Button(MORADO_CLARO,815,450,80,70,None, 20,"Más")
    botonAumVelAta = Button(MORADO_CLARO,385,550,80,70,None, 20,"Menos")
    botonDismVelAta = Button(MORADO_CLARO,815,550,80,70,None, 20,"Más")
    listaBotonesConfig = [botonArquero, botonEscudero, botonLenador, botonCanibal, botonAumVel, botonDismVel,botonAumVelAta,botonDismVelAta]
    #Instancias de Entries
    entryJugador = Entry(555,50,210,30,"",MORADO_OSCURO)
    #Variables para desplegar las diferentes secciones
    ayuda = False
    config = False
    salon = False
    creditos = False
    monstruo = ""
    velocidad = "¿?"
    velAtaque = "¿?"
    velocidades = [""]
    #Textos
    comoJugarText = fontTitulo.render("¿Como Jugar?", 1, MORADO_OSCURO)
    ayudaText0 = font.render("El juego es un tower defense", 1, MORADO_OSCURO)
    ayudaText1 = font.render("de estrategia en el que los", 1, MORADO_OSCURO)
    ayudaText2 = font.render("enemigos intentan llegar a ", 1, MORADO_OSCURO)
    ayudaText3 = font.render("la parte superior de la pantalla,", 1, MORADO_OSCURO)
    ayudaText4 = font.render ("para evitarlo debes colocar ", 1, MORADO_OSCURO)
    ayudaText5 = font.render("rooks que destrocen a los enemigos, ", 1, MORADO_OSCURO)
    ayudaText6 = font.render("pero no todo es tan sencillo, ", 1, MORADO_OSCURO)
    ayudaText7 = font.render ("debes conseguir monedas ", 1, MORADO_OSCURO)
    ayudaText8 = font.render("para constuir cada rook.", 1, MORADO_OSCURO)
    ayudaText9 = font.render("Ganas al derrotar a todos ", 1, MORADO_OSCURO)
    ayudaText10 = font.render("los enemigos de la zona.", 1, MORADO_OSCURO)
    jugadorText = font.render("Jugador: ", 1, MORADO_OSCURO)
    configVelocidadText = fontita.render("Vel. de movimiento:", 1, MORADO_OSCURO)
    configVelAtaqueText = fontita.render("Vel. de ataque:", 1, MORADO_OSCURO)
    configVelocidad = fontita.render(velocidad, 1, MORADO_OSCURO)
    configVelAtaque = fontita.render(velAtaque, 1, MORADO_OSCURO)
    desarrolladoresText = font.render ("Desarrolladores:", 1, MORADO_OSCURO)
    yordiText = font.render ("Yordi Brenes Roda ", 1, MORADO_OSCURO)
    ingridText = font.render ("Ingrid Vargas Badilla", 1, MORADO_OSCURO)
    paisText = font.render ("Juego desarrollado en Costa Rica ", 1, MORADO_OSCURO)
    institucionText = font.render ("Inst. Instituto Tecnológico de Costa Rica ", 1, MORADO_OSCURO)
    versionText = font.render ("Versión: 1.0 ", 1, MORADO_OSCURO)
    #Imagenes
    yordiImg = pygame.transform.scale(pygame.image.load('Yordi.jpg'), (200,200))
    ingridImg = pygame.transform.scale(pygame.image.load('Ingrid.jpg'), (200,200))
    """----------"""
    running = True

    while running:
        screen.fill((200,200,200))
        pygame.draw.rect(screen, (GRIS), (380, 0, 520, 700),0)
        screen.blit(jugadorText, (450, 52))

        for boton in listaBotonesInicio: # Mantiene los botones
            boton.draw(screen,(0,0,0))
        entryJugador.draw()

        if salon: #Si se clica el boton Salon
            def load_data():  # reads the player's name and the score obtained in the game in scores.txt
                file = open("scores.txt", "r", encoding='utf-8')
                contents: list = file.read().split("\n")
                result = []

                def sort_list(a, i, j, n):
                    if j == n:
                        i = i + 1
                        j = 0
                    if i == n:
                        return
                    if a[i][1] > a[j][1]:
                        temp = a[j]
                        a[j] = a[i]
                        a[i] = temp
                        sort_list(a, i, j + 1, n)
                    else:
                        sort_list(a, i, j + 1, n)
                    return a

                def do_split(temp: list):
                    if len(temp) != len(contents):
                        buff = contents[len(temp)].split(",")
                        buff[1] = int(buff[1])
                        temp.append(buff)
                        return do_split(temp)
                    temp = sort_list(temp, 0, 0, len(temp))
                    return temp

                if len(contents) > 1:
                    result = do_split([])
                file.close()
                return result


            def create_table(rows, columns, arr):
                if rows == 0 or columns == 0:
                    print("Unable to build the table.")
                    return 0
                else:
                    pos1 = font.render('1        ' + str(arr[0][0]), 1, MORADO_OSCURO)
                    pos6 = font.render(str(arr[0][1]), 1, MORADO_OSCURO)
                    screen.blit(pos1, (400, 160))
                    screen.blit(pos6, (700, 160))
                    pos2 = font.render('2        ' + str(arr[1][0]), 1, MORADO_OSCURO)
                    pos7 = font.render(str(arr[1][1]), 1, MORADO_OSCURO)
                    screen.blit(pos2, (400, 200))
                    screen.blit(pos7, (700, 200))
                    pos3 = font.render('3        ' + str(arr[2][0]), 1, MORADO_OSCURO)
                    pos8 = font.render(str(arr[2][1]), 1, MORADO_OSCURO)
                    screen.blit(pos3, (400, 240))
                    screen.blit(pos8, (700, 240))
                    pos4 = font.render('4        ' + str(arr[3][0]), 1, MORADO_OSCURO)
                    pos9 = font.render(str(arr[3][1]), 1, MORADO_OSCURO)
                    screen.blit(pos4, (400, 280))
                    screen.blit(pos9, (700, 280))
                    pos5 = font.render('5        ' + str(arr[4][0]), 1, MORADO_OSCURO)
                    pos10 = font.render(str(arr[4][1]), 1, MORADO_OSCURO)
                    screen.blit(pos5, (400, 320))
                    screen.blit(pos10, (700, 320))

            data = load_data()
            create_table(7, 3, data[::-1])


        elif ayuda: #Si es clica el boton Ayuda
            screen.blit(comoJugarText, (400, 100))
            screen.blit(ayudaText0, (400, 160))
            screen.blit(ayudaText1, (400, 190))
            screen.blit(ayudaText2, (400, 220))
            screen.blit(ayudaText3, (400, 250))
            screen.blit(ayudaText4, (400, 280))
            screen.blit(ayudaText5, (400, 310))
            screen.blit(ayudaText6, (400, 340))
            screen.blit(ayudaText7, (400, 370))
            screen.blit(ayudaText8, (400, 400))
            screen.blit(ayudaText9, (400, 430))
            screen.blit(ayudaText10, (400, 460))

        elif config: #Si se clica el boton Config
            for boton in listaBotonesConfig:
                boton.draw(screen,(0,0,0))
                configVelocidad = fontita.render(velocidad, 1, MORADO_OSCURO)
                configVelAtaque = fontita.render(velAtaque, 1, MORADO_OSCURO)
                screen.blit(configVelocidadText, (480, 475))
                screen.blit(configVelAtaqueText, (500, 575))
                screen.blit(configVelocidad, (685, 475))
                screen.blit(configVelAtaque, (650, 575))
                
        elif creditos:
            screen.blit(desarrolladoresText, (400, 180))
            screen.blit(yordiText, (430, 210))
            screen.blit(ingridText, (430, 240))
            screen.blit(yordiImg, (400, 300))
            screen.blit(ingridImg, (650, 300))
            screen.blit(paisText, (390, 550))
            screen.blit(institucionText, (390, 520))
            screen.blit(versionText, (390, 580))
            
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                entryJugador.typing(event)
            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotonesInicio:
                    if boton.isOver(pos):
                        boton.color = CAFE
                    else:
                        boton.color = AMARILLO
                for boton in listaBotonesConfig:
                    if boton.isOver(pos):
                        boton.color = CAFE
                    else:
                        boton.color = AMARILLO
            if event.type == pygame.MOUSEBUTTONDOWN:
                global a,b,i,d,e,f,g,h
                if botonPlay.isOver(pos):
                    global jugador
                    jugador = entryJugador.text
                    running = False
                    Juego()
                elif botonContinuar.isOver(pos):
                    global continuar
                    running = False
                    continuar = True
                    Juego()
                elif botonSalon.isOver(pos):
                    ayuda = False
                    config = False
                    salon = True
                    creditos = False
                elif botonConfig.isOver(pos):
                    ayuda = False
                    config = True
                    salon = False
                    creditos = False
                elif botonAyuda.isOver(pos):
                    ayuda = True
                    config = False
                    salon = False
                    creditos = False
                elif botonCreditos.isOver(pos):
                    ayuda = False
                    config = False
                    salon = False
                    creditos = True
                elif botonExit.isOver(pos):
                    running = False
                    archivo = open("Configuracion.txt", "w")
                    archivo.seek(0)
                    archivo.write(str(a)+str(b)+str(i)+str(d)+str(e)+str(f)+str(g)+str(h)+str(level))
                    archivo.close()
                    pygame.quit()
                    sys.exit()
                elif botonArquero.isOver(pos):
                    monstruo = "Arquero"
                    if a == 2:
                        velocidad = "Mamadísimo"
                    elif a == 4:
                        velocidad = "Rápido"
                    elif a == 6:
                        velocidad = "Normal"
                    elif a == 8:
                        velocidad = "Lento"
                    if b == 2:
                        velAtaque = "Mamadísimo"
                    elif b == 4:
                        velAtaque = "Rápido"
                    elif b == 6:
                        velAtaque = "Normal"
                    elif b == 8:
                        velAtaque = "Lento"
                elif botonEscudero.isOver(pos):
                    monstruo = "Escudero"
                    if i == 2:
                        velocidad = "Mamadísimo"
                    elif i == 4:
                        velocidad = "Rápido"
                    elif i == 6:
                        velocidad = "Normal"
                    elif i == 8:
                        velocidad = "Lento"
                    if d == 2:
                        velAtaque = "Mamadísimo"
                    elif d == 4:
                        velAtaque = "Rápido"
                    elif d == 6:
                        velAtaque = "Normal"
                    elif d == 8:
                        velAtaque = "Lento"
                elif botonLenador.isOver(pos):
                    monstruo = "Leñador"
                    if e == 2:
                        velocidad = "Mamadísimo"
                    elif e == 4:
                        velocidad = "Rápido"
                    elif e == 6:
                        velocidad = "Normal"
                    elif e == 8:
                        velocidad = "Lento"
                    if f == 2:
                        velAtaque = "Mamadísimo"
                    elif f == 4:
                        velAtaque = "Rápido"
                    elif f == 6:
                        velAtaque = "Normal"
                    elif f == 8:
                        velAtaque = "Lento"
                elif botonCanibal.isOver(pos):
                    monstruo = "Canibal"
                    if g == 2:
                        velocidad = "Mamadísimo"
                    elif g == 4:
                        velocidad = "Rápido"
                    elif g == 6:
                        velocidad = "Normal"
                    elif g == 8:
                        velocidad = "Lento"
                    if h == 2:
                        velAtaque = "Mamadísimo"
                    elif h == 4:
                        velAtaque = "Rápido"
                    elif h == 6:
                        velAtaque = "Normal"
                    elif h == 8:
                        velAtaque = "Lento"
                elif botonAumVel.isOver(pos):
                    if monstruo == "Arquero":
                        if a < 8 and a >= 2:
                            a += 2
                            if a == 2:
                                velocidad = "Mamadísimo"
                            elif a == 4:
                                velocidad = "Rápido"
                            elif a == 6:
                                velocidad = "Normal"
                            elif a == 8:
                                velocidad = "Lento"
                    elif monstruo == "Escudero":
                        if i < 8 and i >= 2:                        
                            i += 2
                            if i == 2:
                                velocidad = "Mamadísimo"
                            elif i == 4:
                                velocidad = "Rápido"
                            elif i == 6:
                                velocidad = "Normal"
                            elif i == 8:
                                velocidad = "Lento"
                    elif monstruo == "Leñador":
                        if e < 8 and e >= 2:                        
                            e += 2
                            if e == 2:
                                velocidad = "Mamadísimo"
                            elif e == 4:
                                velocidad = "Rápido"
                            elif e == 6:
                                velocidad = "Normal"
                            elif e == 8:
                                velocidad = "Lento"                          
                    elif monstruo == "Canibal":
                        if g < 8 and g >= 2:                        
                            g += 2
                            if g == 2:
                                velocidad = "Mamadísimo"
                            elif g == 4:
                                velocidad = "Rápido"
                            elif g == 6:
                                velocidad = "Normal"
                            elif g == 8:
                                velocidad = "Lento"
                elif botonDismVel.isOver(pos):                 
                    if monstruo == "Arquero":
                        if a <= 8 and a > 2:   
                            a -= 2
                            if a == 2:
                                velocidad = "Mamadísimo"
                            elif a == 4:
                                velocidad = "Rápido"
                            elif a == 6:
                                velocidad = "Normal"
                            elif a == 8:
                                velocidad = "Lento"
                    elif monstruo == "Escudero":
                        if i <= 8 and i > 2:                        
                            i -= 2
                            if i == 2:
                                velocidad = "Mamadísimo"
                            elif i == 4:
                                velocidad = "Rápido"
                            elif i == 6:
                                velocidad = "Normal"
                            elif i == 8:
                                velocidad = "Lento"
                    elif monstruo == "Leñador":
                        if e <= 8 and e > 2:                        
                            e -= 2
                            if e == 2:
                                velocidad = "Mamadísimo"
                            elif e == 4:
                                velocidad = "Rápido"
                            elif e == 6:
                                velocidad = "Normal"
                            elif e == 8:
                                velocidad = "Lento"
                    elif monstruo == "Canibal":
                        if g <= 8 and g > 2:                    
                            g -= 2
                            if g == 2:
                                velocidad = "Mamadísimo"
                            elif g == 4:
                                velocidad = "Rápido"
                            elif g == 6:
                                velocidad = "Normal"
                            elif g == 8:
                                velocidad = "Lento"
                elif botonDismVelAta.isOver(pos):                  
                    if monstruo == "Arquero":
                        if b <= 8 and b > 2:                        
                            b -= 2
                            if b == 2:
                                velAtaque = "Mamadísimo"
                            elif b == 4:
                                velAtaque = "Rápido"
                            elif b == 6:
                                velAtaque = "Normal"
                            elif b == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Escudero":
                        if d <= 8 and d > 2:                        
                            d -= 2
                            if d == 2:
                                velAtaque = "Mamadísimo"
                            elif d == 4:
                                velAtaque = "Rápido"
                            elif d == 6:
                                velAtaque = "Normal"
                            elif d == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Leñador":
                        if f <= 8 and f > 2:                        
                            f -= 2
                            if f == 2:
                                velAtaque = "Mamadísimo"
                            elif f == 4:
                                velAtaque = "Rápido"
                            elif f == 6:
                                velAtaque = "Normal"
                            elif f == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Canibal":
                        if h <= 8 and h > 2:                        
                            h -= 2
                            if h == 2:
                                velAtaque = "Mamadísimo"
                            elif h == 4:
                                velAtaque = "Rápido"
                            elif h == 6:
                                velAtaque = "Normal"
                            elif h == 8:
                                velAtaque = "Lento"
                elif botonAumVelAta.isOver(pos):      
                    if monstruo == "Arquero":
                        if b < 8 and b >= 2:                          
                            b += 2
                            if b == 2:
                                velAtaque = "Mamadísimo"
                            elif b == 4:
                                velAtaque = "Rápido"
                            elif b == 6:
                                velAtaque = "Normal"
                            elif b == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Escudero":
                        if d < 8 and d >= 2:                        
                            d += 2
                            if d == 2:
                                velAtaque = "Mamadísimo"
                            elif d == 4:
                                velAtaque = "Rápido"
                            elif d == 6:
                                velAtaque = "Normal"
                            elif d == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Leñador":
                        if f < 8 and f >= 2:                        
                            f += 2
                            if f == 2:
                                velAtaque = "Mamadísimo"
                            elif f == 4:
                                velAtaque = "Rápido"
                            elif f == 6:
                                velAtaque = "Normal"
                            elif f == 8:
                                velAtaque = "Lento"
                    elif monstruo == "Canibal":
                        if h < 8 and h >= 2:                        
                            h += 2
                            if h == 2:
                                velAtaque = "Mamadísimo"
                            elif h == 4:
                                velAtaque = "Rápido"
                            elif h == 6:
                                velAtaque = "Normal"
                            elif h == 8:
                                velAtaque = "Lento"
        pygame.display.update()


position_columna = [438, 515, 592, 669, 746]
position_fila = [38, 115, 192, 269, 346, 423, 500, 577, 654] 
listaHacha = []


"""------------------JUEGO----------------"""
"""
Dezpliega la interfaz del juego
"""
def Juego():
    global reloj
    global contEnemigos
    global monedas
    global matriz
    global rooks
    now = pygame.time.get_ticks()//1000
    reloj = pygame.time.get_ticks()//1000
    running = True
    TAM_CASILLA = 77 #Tamaño de cada casilla
    tipo = 0 #Variable que determina que rook colocar
    contEnemigos = 5 #Variable que determina cuando se supera el nivel
    monedas = 100

    #Texto de interfaz
    jugadorText = font.render("Jugador: "+str(jugador), 1, MORADO_OSCURO)
    #Imágenes
    coinImgs = [pygame.image.load('Coin0.png'),pygame.image.load('Coin1.png'),pygame.image.load('Coin2.png')]
    rookImgs = [pygame.image.load("Sand.png"),pygame.image.load("Rock.png"), pygame.image.load("Fire.png"), pygame.image.load("Water.png")]
    bulletImgs = [pygame.image.load("Dust.png"), pygame.image.load("BulletRock.png"), pygame.image.load("Fireball.png"), pygame.image.load("Waterdrop.png")]
    muteImg = pygame.image.load('Mute.png')
    tableros = [pygame.image.load('lawn2.jpg'), pygame.image.load('lawn1.jpg'), pygame.image.load('lawn3.jpg')]
    #Efectos de sonido
    global estadoMusica
    estadoMusica = True
    musica = mixer.music.load("Graze the Roof.mp3")
    pygame.mixer.music.play(-1)
    disparoAgua = mixer.Sound("WaterSplash.wav")
    disparoFuego = mixer.Sound("Fireball.wav")
    disparoArena = mixer.Sound("Sand.wav")
    disparoRoca = mixer.Sound("DisparoRock.wav")
    disparoFlecha = mixer.Sound("DisparoFlecha.wav")
    golpeRoca = mixer.Sound("Rock.wav")
    placeRook = mixer.Sound("PlaceRook.wav")
    victory = mixer.Sound("Victory.wav")
    gameOver = mixer.Sound("GameOver.wav")
    getMoneda = mixer.Sound("GetCoin.wav")
    hits = [mixer.Sound("Hit1.wav"), mixer.Sound("Hit3.wav")]
    dead = mixer.Sound("Dead.wav")
    gameOver = mixer.Sound("GameOver.wav")
    # Listas
    rooks = []
    coins = []
    enemigos = []
    enemigosDisponibles = ["Arquero","Escudero","Lenador","Canibal"]
    #Instancias de botones
    botonSand = Button(AMARILLO,55,200,100,70,rookImgs[0],None)
    botonRock = Button(AMARILLO,200,200,100,70,rookImgs[1],None)
    botonFire = Button(AMARILLO,55,300,100,70,rookImgs[2],None)
    botonWater = Button(AMARILLO,200,300,100,70,rookImgs[3],None)
    botonQuit = Button(AMARILLO,100,600,150,70,None,35,"Quit")
    botonMute = Button(AMARILLO,60,500,50,50,muteImg,None)
    listaBotones = [botonSand, botonRock, botonFire, botonWater, botonQuit, botonMute]
    #Eventos con tiempo
    coinCooldown = 3000
    coinCooldowns = [3000, 5000, 7000, 10000]
    tiempo = pygame.time.get_ticks()
    sandCooldown = 3000
    rockCooldown = 5000
    fireCooldown = 6000
    waterCooldown = 6000
    clock = pygame.time.Clock()
    enemigoCoolDown = 5000
    global enemigoCoolDowns
    enemigoCoolDowns = [3000, 4000, 5000]
    tiempoEnemigo = pygame.time.get_ticks()  
    global continuar

    """
    Objeto: Coin
    Atributos:
    r: int
    c: int
    Metodos:
    draw:
    S: Dezpliega la imagen en pantalla
    """
    class Coin():
        def __init__(self, r, c):
            self.r = r
            self.c = c
            self.img = random.choice(coinImgs)
            if self.img == coinImgs[0]:
                self.valor = 25
            elif self.img == coinImgs[1]:
                self.valor = 50
            elif self.img == coinImgs[2]:
                self.valor = 100
        def draw(self):
            screen.blit(self.img, (position_columna[self.c]-30,position_fila[self.r]-30))

    """
    Objetos: Rook
    Atributos:
    tipo: str
    r: int
    c: int
    listaDisparos: list
    last_fire: int
    cooldown: int
    vida: int
    coste: int
    ptsAtaque: int
    img: variable de la imagen
    Métodos:
    draw:
    S: Dezpliega la imagen del rook
    disparar:
    S: True si hay un enemigo en la columna del rook
    """
    class Rook():
        def __init__(self, tipo, r, c):
            global monedas
            self.tipo = tipo
            self.r = r
            self.c = c
            self.listaDisparos = []
            self.last_fire = 0
            if tipo == "Sand":   # Aquí van las respectivas variables de velocidad de ataque
                self.cooldown = sandCooldown
                self.vida = 7
                self.coste = 50
                self.ptsAtaque = 2
                self.img = rookImgs[0]
            elif tipo == "Rock":
                self.cooldown = rockCooldown
                self.vida = 14
                self.coste = 100
                self.ptsAtaque = 4
                self.img = rookImgs[1]
            elif tipo == "Fire":
                self.cooldown = fireCooldown
                self.vida = 16
                self.coste = 150
                self.ptsAtaque = 8
                self.img = rookImgs[2]
            elif tipo == "Water":
                self.cooldown = waterCooldown
                self.vida = 16
                self.coste = 150
                self.ptsAtaque = 8
                self.img = rookImgs[3]
            monedas -= self.coste
            
        def draw(self):
            screen.blit(self.img, (position_columna[self.r]-30,position_fila[self.c]-30))

        def disparar(self):
            ataque = False
            matrizTrans = np.transpose(matriz) # Transposición de la matriz para que sea más facil verificar la columna
            for elem in matrizTrans[self.r]:
                if elem ==  5 or elem == 6 or elem == 7 or elem ==8 : #if elem es igual a monsturo*
                    ataque = True
                    break
            if ataque == True:
                if self.tipo == "Rock":
                    disparoRoca.play()
                elif self.tipo == "Fire":
                    disparoFuego.play()
                elif self.tipo == "Water":
                    disparoAgua.play()                    
                self.listaDisparos.append(Bullet(self.tipo, self.c, self.r, self.ptsAtaque))
                #Crea la bala
            else:
                pass

    """
    Objeto: Lenador
    Atributos:
    kind: int
    x: int
    y: int
    image: Imagen
    walk: Lista
    ataque: int
    vida: int
    posImagen: int
    tiempoCambio: int
    imagenLenador: imagen
    list_attack: lista
    r: int
    c: int
    cont: int
    cont2: int
    cambioY: int
    
    Métodos:
    Move()        :Verifica si es posible el desplazamiento y el ataque
    draw()        :Coloca la imagen en la pantalla
    trayectoria() :Cambia la posicion del objeto
    Attack()      :Realiza el ataque
    """
    class Lenador(pygame.sprite.Sprite):  # Clase para los lenadores
        global position_fila, position_columna, a, b, i, d, e, f, g, h
        clock = pygame.time.Clock()
        def __init__(self, x, y, kind):
            pygame.sprite.Sprite.__init__(self)
            position_fila.append(731)
            position_fila.append(808)
            self.vali = i
            self.kind = kind
            if self.kind == "Arquero":
                self.image = pygame.image.load('Images/a_a1.png')
                self.walk = [pygame.image.load('Images/a_c1.png'), pygame.image.load('Images/a_c2.png'),
                             pygame.image.load('Images/a_c3.png'), pygame.image.load('Images/a_c4.png'),
                             pygame.image.load('Images/a_c1.png'), pygame.image.load('Images/a_c2.png'),
                             pygame.image.load('Images/a_c3.png'), pygame.image.load('Images/a_c4.png')]
                self.ataque = 2
                self.vida = 5

            elif self.kind == "Escudero":
                self.image = pygame.image.load('Images/e_a1.png')
                self.walk = [pygame.image.load('Images/e_c1.png'), pygame.image.load('Images/e_c2.png'),
                             pygame.image.load('Images/e_c3.png'),
                             pygame.image.load('Images/e_c4.png'), pygame.image.load('Images/e_c5.png'),
                             pygame.image.load('Images/e_c6.png'),
                             pygame.image.load('Images/e_c7.png'), pygame.image.load('Images/e_c8.png'),
                             pygame.image.load('Images/e_c9.png'),
                             pygame.image.load('Images/e_c10.png')]
                self.ataque = 3
                self.vida = 10

            elif self.kind == "Lenador":
                self.image = pygame.image.load('Images/l_a1.png')
                self.attack = [pygame.image.load('Images/l_a1.png'), pygame.image.load('Images/l_a1.png'), pygame.image.load('Images/l_a1.png'),
                               pygame.image.load('Images/l_a2.png'), pygame.image.load('Images/l_a2.png'), pygame.image.load('Images/l_a2.png'),
                               pygame.image.load('Images/l_a3.png'), pygame.image.load('Images/l_a3.png'), pygame.image.load('Images/l_a3.png'),
                               pygame.image.load('Images/l_a4.png'), pygame.image.load('Images/l_a4.png'), pygame.image.load('Images/l_a4.png'),
                               pygame.image.load('Images/l_a5.png'), pygame.image.load('Images/l_a5.png'), pygame.image.load('Images/l_a5.png'),
                               pygame.image.load('Images/l_a6.png'), pygame.image.load('Images/l_a6.png'), pygame.image.load('Images/l_a6.png'),
                               pygame.image.load('Images/l_a7.png'), pygame.image.load('Images/l_a7.png'), pygame.image.load('Images/l_a7.png'),
                               pygame.image.load('Images/l_a8.png'), pygame.image.load('Images/l_a8.png'), pygame.image.load('Images/l_a8.png'),
                               pygame.image.load('Images/l_a9.png'), pygame.image.load('Images/l_a9.png'), pygame.image.load('Images/l_a9.png')]
                self.walk = [pygame.image.load('Images/le_c1.png'), pygame.image.load('Images/le_c2.png'),
                             pygame.image.load('Images/le_c3.png'),
                             pygame.image.load('Images/le_c4.png'), pygame.image.load('Images/le_c5.png'),
                             pygame.image.load('Images/le_c6.png'),
                             pygame.image.load('Images/le_c7.png'), pygame.image.load('Images/le_c8.png'),
                             pygame.image.load('Images/le_c9.png'),
                             pygame.image.load('Images/le_c10.png'), pygame.image.load('Images/le_c11.png'),
                             pygame.image.load('Images/le_c12.png'),
                             pygame.image.load('Images/le_c13.png'), pygame.image.load('Images/le_c14.png')]
                self.ataque = 9
                self.vida = 20

            elif self.kind == "Canibal":
                self.image = pygame.image.load('Images/c_a1.png')
                self.attack = [pygame.image.load('Images/c_a1.png'), pygame.image.load('Images/c_a1.png'),pygame.image.load('Images/c_a1.png'),
                               pygame.image.load('Images/c_a1.png'), pygame.image.load('Images/c_a1.png'), pygame.image.load('Images/c_a1.png'),
                               pygame.image.load('Images/c_a3.png'), pygame.image.load('Images/c_a3.png'), pygame.image.load('Images/c_a3.png'),
                               pygame.image.load('Images/c_a4.png'), pygame.image.load('Images/c_a4.png'), pygame.image.load('Images/c_a4.png'),
                               pygame.image.load('Images/c_a5.png'), pygame.image.load('Images/c_a5.png'), pygame.image.load('Images/c_a5.png'),
                               pygame.image.load('Images/c_a6.png'), pygame.image.load('Images/c_a6.png'), pygame.image.load('Images/c_a6.png'),
                               pygame.image.load('Images/c_a7.png'), pygame.image.load('Images/c_a7.png'), pygame.image.load('Images/c_a7.png'),
                               pygame.image.load('Images/c_a8.png'), pygame.image.load('Images/c_a8.png'), pygame.image.load('Images/c_a8.png')]
                self.walk = [pygame.image.load('Images/c_c1.png'), pygame.image.load('Images/c_c2.png'),
                             pygame.image.load('Images/c_c3.png'),
                             pygame.image.load('Images/c_c4.png'), pygame.image.load('Images/c_c5.png'),
                             pygame.image.load('Images/c_c6.png'),
                             pygame.image.load('Images/c_c7.png'), pygame.image.load('Images/c_c8.png'),
                             pygame.image.load('Images/c_c9.png'),
                             pygame.image.load('Images/c_c10.png'), pygame.image.load('Images/c_c11.png'),
                             pygame.image.load('Images/c_c12.png')]
                self.ataque = 12
                self.vida = 25

            self.posImagen = 0
            self.tiempoCambio = 1
            self.imagenLenador = self.walk[self.posImagen]
            self.list_attack = []

            self.r = x
            self.c = y
            self.cont = 0
            self.cont2 = 0
            self.x = position_columna[self.r] - 20
            self.y = position_fila[self.c] + 20
            self.cambioY = 3
            self.cambioimg = 0

        def Move(self):
            if self.c > 8:
                if reloj % 2 == 0:
                    if self.cont == 0:
                        self.c -= 1
                        self.cont = 1
                else:
                    self.cont = 0
                    self.imagenLenador = self.image

            else:
                n = matriz[self.c - 2][self.r]
                if self.kind == "Arquero":
                    matriz[self.c - 1][self.r] = 5
                    if n != 1 and n != 2 and n != 3 and n != 4:
                        if reloj % a == 0:  # Avance del arquero
                            if self.cont == 0:
                                matriz[self.c-1][self.r] = 0
                                self.c -= 1
                                self.cont = 1
                                matriz[self.c-1][self.r] = 5
                        else:
                            self.cont = 0
                            self.imagenLenador = self.image

                    if reloj % b == 0:  # Ataque del arquero
                        if self.cont2 == 0:
                            self.Attack()
                            self.cont2 = 1
                    else:
                        self.cont2 = 0
                elif self.kind == "Escudero":
                    matriz[self.c - 1][self.r] = 6
                    if n != 1 and n != 2 and n != 3 and n != 4:
                        if reloj % i == 0:  # Avance del escudero
                            if self.cont == 0:
                                matriz[self.c-1][self.r] = 0
                                self.c -= 1
                                self.cont = 1
                                matriz[self.c-1][self.r] = 6
                        else:
                            self.cont = 0
                            self.imagenLenador = self.image
                    if reloj % d == 0:  # Ataque del escudero
                        if self.cont2 == 0:
                            self.Attack()
                            self.cont2 = 1
                    else:
                        self.cont2 = 0
                elif self.kind == "Lenador":
                    matriz[self.c - 1][self.r] = 7
                    if n != 1 and n != 2 and n != 3 and n != 4:
                        if reloj % e == 0:                    # Avance del lenador
                            if self.cont == 0:
                                matriz[self.c-1][self.r] = 0
                                self.c -= 1
                                self.cont = 1
                                matriz[self.c-1][self.r] = 7
                        else:
                            self.cont = 0
                            self.imagenLenador = self.image
                    if n == 1 or n == 2 or n == 3 or n == 4:
                        if reloj % f == 0:                   # Ataque del lenador
                            self.Attack()
                            if self.cont2 == 0:
                                self.y -= 20
                                self.cont2 = 1
                        else:
                            self.cont2 = 0

                elif self.kind == "Canibal":
                    matriz[self.c - 1][self.r] = 8
                    if n != 1.0 and n != 2.0 and n != 3.0 and n != 4.0:
                        if reloj % g == 0:  # Avance del canibal
                            if self.cont == 0:
                                matriz[self.c-1][self.r] = 0
                                self.c -= 1
                                self.cont = 1
                                matriz[self.c-1][self.r] = 8
                        else:
                            self.imagenLenador = self.image
                            self.cont = 0
                    if n == 1 or n == 2 or n == 3 or n == 4:
                        if reloj % h == 0:  # Ataque del canibal
                            self.Attack()
                            if self.cont2 == 0:
                                self.y -= 20
                                self.cont2 = 1
                        else:
                            self.cont2 = 0

        def draw(self):
            screen.blit(self.imagenLenador, (int(self.x), int(self.y)))


        def trayectoria(self):
            if self.vida == 0:
                matriz[self.c - 1][self.r] = 0
            if self.y > position_fila[self.c-1]-20:
                self.posImagen += 1
                self.tiempoCambio += 1
                if self.posImagen > len(self.walk)-1:
                    self.posImagen = 0
                self.imagenLenador = self.walk[self.posImagen]
                x = int(math.floor(self.y / TAM_CASILLA))
                self.y -= self.cambioY

        def Attack(self):
            validacion = False
            matrizTrans = np.transpose(matriz)
            for elem in matrizTrans[self.r]:
                if elem == 1 or elem == 2 or elem == 3 or elem == 4:
                    validacion = True

            if validacion:
                if self.kind == "Arquero" or self.kind == "Escudero":
                    self.list_attack.append(Bullet(self.kind, self.c, self.r, self.ataque))
                else:
                    self.cambioimg = 1
                    self.corto()

        def corto(self):
            if self.kind == "Lenador" or self.kind == "Canibal":
                if self.cambioimg > 0 and self.cambioimg < len(self.attack):
                    self.cambioimg +=1
                    self.posImagen += 1
                    self.tiempoCambio += 1
                    if self.posImagen > len(self.attack)-1:
                        self.posImagen = 0
                    self.imagenLenador = self.attack[self.posImagen]
                    x = int(math.floor(self.y / TAM_CASILLA))
                    #self.y -= 0
                elif self.cambioimg == len(self.attack):
                    self.list_attack.append(Bullet(self.kind, self.c, self.r, self.ataque))
                    self.cambioimg = 0

            else:
                return

    """
    Objeto:Bullet
    Atributos:
    tipo: string
    r: int
    c: int
    x: int
    y: int
    dano: int
    cambioY: int
    Métodos:
    draw:
    Mantiene la bala en patalla
    trayectoria:
    Cambia la posición en y de la instancia bullet
    """
    class Bullet():
        def __init__(self, tipo, r, c, dano):
            self.tipo = tipo
            self.r = r
            self.c = c
            self.x = position_columna[self.c] -15
            self.y = position_fila[self.r]
            self.dano = dano
            
            if tipo == "Sand":
                self.img = bulletImgs[0]
                self.cambioY = 3
            elif tipo == "Rock":
                self.img = bulletImgs[1]
                self.cambioY = 3
            elif tipo == "Fire":
                self.img = bulletImgs[2]
                self.cambioY = 3
            elif tipo == "Water":
                self.img = bulletImgs[3]
                self.cambioY = 3
            elif tipo == "Arquero":
                self.img = pygame.image.load('Images/f1.png')
                self.cambioY = -3
            elif tipo == "Escudero":
                self.img = pygame.image.load('Images/e1.png')
                self.cambioY = -3
            elif tipo == "Lenador":
                self.img = pygame.image.load('Images/transp.png')
                self.cambioY = -3
                self.y = position_fila[self.r-1]

            elif tipo == "Canibal":
                self.img = pygame.image.load('Images/transp.png')
                self.cambioY = -3
                self.y = position_fila[self.r-1]
            self.posimagen = 0
                
        def draw(self):
            if self.tipo != "Canibal" and self.tipo != "Lenador":
                screen.blit(self.img,(int(self.x), int(self.y) ) )
            else:
                screen.blit(self.img, (int(self.x), int(self.y)-80))

        def trayectoria(self):
            c = int(math.floor(self.y/TAM_CASILLA))
            r = int(math.floor((self.x-400)/TAM_CASILLA))
            self.c = c
            self.r = r
            self.y += self.cambioY
    """
    Funcion que cambia las variables relacionadas al nivel
    """
    def nextLevel():
        global level, enemigoCoolDowns, contEnemigos, matriz, rooks
        level += 1
        contEnemigos = 5
        rooks = []
        matriz = np.zeros((9,5))
        enemigoCoolDowns = [enemigoCoolDowns[0]*0.3, enemigoCoolDowns[1]*0.3, enemigoCoolDowns[2]*0]
        if level == 3:
            continuar = False
            matriz = np.zeros((9,5))
            inicio()
            #Ganaste
            
    global level
    if continuar:
        level -= 1
        nextLevel()
        matriz = np.load("matrizJuego.npy")
    else:
        matriz = np.zeros((9,5))
        level = 0
    for n in range(0,9):
        for m in range(0,5):
            if matriz[n][m] == 1:
                rooks.append(Rook("Sand",m,n))
            elif matriz[n][m] == 2:
                rooks.append(Rook("Rock",m,n))
            elif matriz[n][m] == 3:
                rooks.append(Rook("Fire",m,n))
            elif matriz[n][m] == 4:
                rooks.append(Rook("Water",m,n))
            elif matriz[n][m] == 5:
                enemigos.append(Lenador(m,n,"Arquero",))
            elif matriz[n][m] == 6:
                enemigos.append(Lenador(m,n,"Escudero"))
            elif matriz[n][m] == 7:
                enemigos.append(Lenador(m,n,"Lenador"))
            elif matriz[n][m] == 8:
                enemigos.append(Lenador(m,n,"Canibal"))

    monedasText = font.render("Monedas: "+str(monedas), 1, MORADO_OSCURO)
    
    """
    Objeto:Fuegos
    Atributos:
    x: int
    y: int
    images: lista
    pos: int
    image = imagen de la lista
    Métodos:
    mover():
    Crea la animacion
    draw():
    Dibuja los objetos en pantalla 
    """
    class Fuegos():
        def __init__(self, x, y):
            self.x = x
            self.y = y
            if victoria == 0:
                self.images = [pygame.image.load('Images/c_11.png'), pygame.image.load('Images/c_22.png'),
                               pygame.image.load('Images/c_33.png'), pygame.image.load('Images/c_44.png'),
                               pygame.image.load('Images/c_33.png'), pygame.image.load('Images/c_22.png'),
                               pygame.image.load('Images/c_11.png'), pygame.image.load('Images/c_55.png'),
                               pygame.image.load('Images/c_66.png'), pygame.image.load('Images/c_77.png'),
                               pygame.image.load('Images/c_66.png'), pygame.image.load('Images/c_55.png')]
            elif victoria == 1:
                self.images = [pygame.image.load('Images/fu_01.png'), pygame.image.load('Images/fu_02.png'),
                               pygame.image.load('Images/fu_03.png'), pygame.image.load('Images/fu_04.png'),
                               pygame.image.load('Images/fu_05.png'), pygame.image.load('Images/fu_06.png'),
                               pygame.image.load('Images/fu_07.png'), pygame.image.load('Images/fu_08.png'),
                               pygame.image.load('Images/fu_09.png'), pygame.image.load('Images/fu_01.png')]
            self.pos = 0
            self.image = self.images[self.pos]

        def mover(self):
            self.pos += 1
            if self.pos > len(self.images) - 1:
                self.pos = 0
            self.image = self.images[self.pos]

        def draw(self):
            screen.blit(self.image, (self.x, self.y))


    cont = 0
    gano = pygame.image.load('Images/gano1.png')
    perdio = pygame.image.load('Images/perdio.png')
    nextLVL = pygame.image.load('Images/next.gif')
    victoria = 0
    clock = pygame.time.Clock()
    fuegos = []

    while running:
        global lenadorwalk, len_walk, listaHacha, lenadorattack, len_attack
        reloj = pygame.time.get_ticks()//1000 - now

        relojEnemigo = pygame.time.get_ticks()
        
        if relojEnemigo - tiempoEnemigo > enemigoCoolDown and contEnemigos != 0:
            # Random choice: 0=arquero, 1=escudero, 2=lenador, 3=canibal
            avatarchoice = random.choice(enemigosDisponibles)
            x = randint(0,4)
            tiempoEnemigo = relojEnemigo
            # enemigoCoolDown = random.choice(enemigoCoolDowns)
            enemigos.append(Lenador(x, 10, avatarchoice))
            contEnemigos -= 1


        for event in pygame.event.get():
            #Mantiene la ventana abierta

            pos = pygame.mouse.get_pos()



            #Asignar valor a la matriz se le hace click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 400 and pos[0] < 785 and pos[1] < 700 and pos[1] >0:
                    #Valores en la matriz, colum y raw
                    c = int(math.floor((pos[0] - 400)/TAM_CASILLA))
                    r = int(math.floor(pos[1]/TAM_CASILLA))
                    if matriz[r][c] == 1 or matriz[r][c] == 2 or matriz[r][c] == 3 or matriz[r][c] == 4: #Quitar rooks
                        for rook in rooks:
                            if rook.r == c and rook.c == r:
                                rooks.remove(rook)
                                matriz[r][c] = 0
                    elif matriz[r][c] == 0: #Colocar rooks
                        placeRook.play()
                        if tipo == "Sand" and monedas >= 50:
                            matriz[r][c] = 1
                            rooks.append(Rook("Sand", c, r))
                        elif tipo == "Rock" and monedas >= 100:
                            matriz[r][c] = 2
                            rooks.append(Rook("Rock", c, r))
                        elif tipo == "Fire" and monedas >= 150:
                            matriz[r][c] = 3
                            rooks.append(Rook("Fire", c, r))
                        elif tipo == "Water" and monedas >= 150:
                            matriz[r][c] = 4
                            rooks.append(Rook("Water", c, r))
                    for coin in coins: #Obtener coin
                        if coin.r == r and coin.c == c:
                            getMoneda.play()
                            monedas += coin.valor
                            matriz[r][c] = 0
                            coins.remove(coin)
                elif botonMute.isOver(pos):
                    if estadoMusica:
                        pygame.mixer.music.pause()
                        estadoMusica = False
                    else:
                        estadoMusica = True 
                        pygame.mixer.music.unpause()                            
                # Escoger que rook colocar
                elif botonSand.isOver(pos):
                    tipo = "Sand"
                elif botonRock.isOver(pos):
                    tipo = "Rock"
                elif botonFire.isOver(pos):
                    tipo = "Fire"
                elif botonWater.isOver(pos):
                    tipo = "Water"
                elif botonQuit.isOver(pos):
                    running = False
                    np.save("matrizJuego.npy",matriz)
                    continuar = False
                    matriz = np.zeros((9,5))
                    pygame.mixer.music.pause()
                    estadoMusica = False
                    archivo = open("Configuracion.txt", "w")
                    archivo.seek(0)
                    archivo.write(str(a)+str(b)+str(i)+str(d)+str(e)+str(f)+str(g)+str(h)+str(level))
                    archivo.close()
                    inicio()
                else:
                    pass

            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotones:
                    if boton.isOver(pos):
                        boton.color = MORADO_CLARO
                    else:
                        boton.color = AMARILLO
                        
        cronometro = font.render('Tiempo: ' + str(reloj), 1, MORADO_OSCURO)
        #Mantener las instancias en pantalla
        screen.fill((200, 200, 200))
        screen.blit(tableros[level], (370, -19))
        monedasText = font.render("Monedas: " + str(monedas), 1, MORADO_OSCURO, (200,200,200))
        screen.blit(monedasText, (5, 10))
        screen.blit(jugadorText, (5, 40))
        screen.blit(cronometro, (5, 70))
        for boton in listaBotones:
            boton.draw(screen, (0, 0, 0))

        for rook in rooks: #Mantener los rooks en pantalla
            nowRook = pygame.time.get_ticks()
            rook.draw()
            if nowRook - rook.last_fire >= rook.cooldown: #Comprueba si está listo para disparar
                rook.last_fire = nowRook
                rook.disparar()
            if len(rook.listaDisparos) != 0: #Comprueba si hay proyectiles en pantalla
                for proyectil in rook.listaDisparos:
                    proyectil.draw()
                    proyectil.trayectoria()
                    if proyectil.y > 699:  # Comprueba si la posición de la bala sobrepasa el tablero, si lo hace, la elimina
                        rook.listaDisparos.remove(proyectil)
                for proyectil in rook.listaDisparos:
                    for enemigo in enemigos:             
                        if math.sqrt((enemigo.x-proyectil.x)**2 +(enemigo.y - proyectil.y)**2) <= 10:
                            if rook.tipo == "Sand":
                                disparoArena.play()
                            elif rook.tipo == "Rock":
                                golpeRoca.play()
                            random.choice(hits).play()
                            rook.listaDisparos.remove(proyectil)
                            enemigo.vida -= proyectil.dano
                            if enemigo.vida <= 0:
                                dead.play()
                                monedas += 100
                                matriz[enemigo.c-1][enemigo.r] = 0
                                enemigos.remove(enemigo)

        nowCoin = pygame.time.get_ticks()
        if nowCoin - tiempo >= coinCooldown: #Comprueba si se debe generar una moneda
            # Establece una posición aleatoria en la matriz
            rCoin = random.randint(0,8)
            cCoin = random.randint(0,4)
            tiempo = nowCoin
            coinCooldown = random.choice(coinCooldowns)
            if matriz[rCoin][cCoin] == 0: #Si la posición está vacia, la genera
                coins.append(Coin( rCoin, cCoin))
                matriz[rCoin][cCoin] = 9

        for coin in coins: #Mantiene el dibujo de la moneda en pantalla
            coin.draw()


        for enemigo in enemigos:
            enemigo.Move()
            enemigo.trayectoria()
            enemigo.draw()
            enemigo.corto()
            for proyectil in enemigo.list_attack:
                proyectil.trayectoria()
                proyectil.draw()
                if proyectil.y < 1:
                        enemigo.list_attack.remove(proyectil)
                for rook in rooks:
                    if (proyectil.c,proyectil.r) == (rook.c,rook.r):
                        rook.vida -= proyectil.dano
                        enemigo.list_attack.remove(proyectil)
                        if rook.vida <= 0:
                            matriz[rook.c][rook.r] = 0
                            rooks.remove(rook)
                            
        for m in range(0,5):
            if matriz[0][m] == 5 or matriz[0][m] == 6 or matriz[0][m] == 7 or matriz[0][m] == 8:
                gameOver.play()
                level = 0
                victoria = 0
                n = 0

                x = 100
                y = 100
                fuegos.append(Fuegos(x, y))
                x = 100
                y = 500
                fuegos.append(Fuegos(x, y))
                x = 600
                y = 500
                fuegos.append(Fuegos(x, y))
                x = 600
                y = 100
                fuegos.append(Fuegos(x, y))
                while n < 100:
                    screen.fill((200, 200, 200))
                    for elem in fuegos:
                        m = 0
                        elem.draw()
                        if m % 300 == 0:
                            elem.mover()
                        m + 1
                        n += 1
                    screen.blit(perdio, (150, 90))
                    clock.tick(8)
                    pygame.display.update()

                running = False
                continuar = False
                matriz = np.zeros((9,5))
                pygame.mixer.music.pause()
                estadoMusica = False
                reloj = 0
                inicio()
                
        if contEnemigos == 0 and len(enemigos) == 0:
            if level != 2:
                n = 0
                while n < 1000:
                    screen.fill((200,200,200))
                    screen.blit(nextLVL, (150, 90))
                    n += 1
                    pygame.display.update()
            else:
                ganador = str(jugador) + ',' + str(reloj)
                file = open("scores.txt", "a")
                file.write('\n' + str(ganador))
                file.close()
                running = False
                continuar = False
                matriz = np.zeros((9,5))
                pygame.mixer.music.pause()
                estadoMusica = False
                victoria = 1
                n = 0
                x = 30
                y = 30
                fuegos.append(Fuegos(x, y))
                x = 150
                y = 500
                fuegos.append(Fuegos(x, y))
                x = 550
                y = 500
                fuegos.append(Fuegos(x, y))
                x = 700
                y = 30
                fuegos.append(Fuegos(x, y))
                victory.play()
                while n < 200:
                    screen.fill((200,200,200))
                    for elem in fuegos:
                        m = 0
                        elem.draw()
                        if m % 300 == 0:
                            elem.mover()
                        m +1
                        n += 1
                    screen.blit(gano, (100,90))
                    clock.tick(8)
                    pygame.display.update()
            nextLevel()

        pygame.display.update()

        

inicio()  
    

