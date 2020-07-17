import pygame,sys,math
import numpy as np
import random
from random import randint
import time
from pygame import mixer

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
fontita = pygame.font.SysFont("Neuropol X Rg", 25)

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
"""
class Button():
    def __init__(self, color, x, y, width, height, img ,text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.text = text
        
        

        #Dibuja el botón en la pantalla
    def draw(self,screen,outline=None):
        #Crea outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        #Despliega imagen en caso de tenerla
        if self.img:
            screen.blit(self.img, (self.x +18,self.y +5))
        
        

        if self.text != '':
            font = pygame.font.SysFont("Comic Sans MS", 35)
            text = font.render(self.text, 1, MORADO_OSCURO)
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

        #Verifica si la posición del mouse está sobre el botón
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

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
            
            
def inicio():
    
    #Instancias de botones
    botonPlay = Button(MORADO_CLARO,155,20,100,70,None,"Play")
    botonContinuar = Button(MORADO_CLARO,90,100,240,70,None,"Continuar Partida")
    botonSalon = Button(MORADO_CLARO,80,200,260,70,None,"Salon de la fama")
    botonConfig = Button(MORADO_CLARO,100,300,220,70,None,"Configuracion")
    botonAyuda = Button(MORADO_CLARO,160,400,110,70,None,"Ayuda")
    botonCreditos = Button(MORADO_CLARO,130,500,150,70,None,"Creditos")
    botonExit = Button(MORADO_CLARO,170,600,80,70,None,"Exit")
    listaBotonesInicio = [botonPlay,botonContinuar,botonSalon,botonConfig,botonAyuda,botonCreditos,botonExit]
    botonArquero = Button(MORADO_CLARO,450,200,80,70,None,"Arquero")
    botonEscudero = Button(MORADO_CLARO,550,200,80,70,None,"Escudero")
    botonLenador = Button(MORADO_CLARO,650,200,80,70,None,"Leñador")
    botonCanibal = Button(MORADO_CLARO,750,200,80,70,None,"Canibal")
    botonAumVel = Button(MORADO_CLARO,400,450,80,70,None,"Más")
    botonDismVel = Button(MORADO_CLARO,750,450,80,70,None,"Menos")
    botonAumVelAta = Button(MORADO_CLARO,400,550,80,70,None,"Más")
    botonDismVelAta = Button(MORADO_CLARO,750,550,80,70,None,"Menos")
    listaBotonesConfig = [botonArquero, botonEscudero, botonLenador, botonCanibal, botonAumVel, botonDismVel,botonAumVelAta,botonDismVelAta]
    #Instancias de Entries
    entryJugador = Entry(500,50,210,30,"",MORADO_OSCURO)
    #Variables para desplegar las diferentes secciones
    ayuda = False
    config = False
    salon = False
    creditos = False
    monstruo = ""
    velocidad = "Unga"
    velAtaque = "AH"
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
    """----------"""
    running = True

    while running:
        screen.fill(GRIS)
        screen.blit(jugadorText, (390, 52))

        for boton in listaBotonesInicio: # Mantiene los botones
            boton.draw(screen,(0,0,0))
        entryJugador.draw()

        if salon: #Si se clica el boton Salon
            pass

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
                screen.blit(configVelocidadText, (500, 475))
                screen.blit(configVelAtaqueText, (500, 575))
                screen.blit(configVelocidad, (675, 475))
                screen.blit(configVelAtaque, (630, 575))
        elif creditos:
            print("ahhhh")
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
                    salon = True
                    creditos = True
                elif botonExit.isOver(pos):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif botonArquero.isOver(pos):
                    monstruo = "Arquero"
                    velocidad = str(a)
                    velAtaque = str(b)
                elif botonEscudero.isOver(pos):
                    monstruo = "Escudero"
                    velocidad = str(i)
                    velAtaque = str(d)
                elif botonLenador.isOver(pos):
                    monstruo = "Lenador"
                    velocidad = str(e)
                    velAtaque = str(f)
                elif botonCanibal.isOver(pos):
                    monstruo = "Canibal"
                    velocidad = str(g)
                    velAtaque = str(h)
                elif botonAumVel.isOver(pos):
                    if monstruo == "Arquero":
                        a += 1
                        velocidad = str(a)
                    elif monstruo == "Escudero":
                        i += 1
                        velocidad = str(i)
                    elif monstruo == "Lenador":
                        e += 1
                        velocidad = str(e)
                    elif monstruo == "Canibal":
                        g += 1
                        velocidad = str(g)
                elif botonDismVel.isOver(pos):
                    if monstruo == "Arquero":
                        a -= 1
                        velocidad = str(a)
                    elif monstruo == "Escudero":
                        i -= 1
                        velocidad = str(i)
                    elif monstruo == "Lenador":
                        e -= 1
                        velocidad = str(e)
                    elif monstruo == "Canibal":
                        g -= 1
                        velocidad = str(g)
                elif botonDismVelAta.isOver(pos):
                    if monstruo == "Arquero":
                        b -= 1
                        velAtaque = str(b)
                    elif monstruo == "Escudero":
                        d -= 1
                        velAtaque = str(d)
                    elif monstruo == "Lenador":
                        f -= 1
                        velAtaque = str(f)
                    elif monstruo == "Canibal":
                        h -= 1
                        velAtaque = str(h)
                elif botonAumVelAta.isOver(pos):
                    if monstruo == "Arquero":
                        b += 1
                        velAtaque = str(b)
                    elif monstruo == "Escudero":
                        d += 1
                        velAtaque = str(d)
                    elif monstruo == "Lenador":
                        f += 1
                        velAtaque = str(f)
                    elif monstruo == "Canibal":
                        h += 1
                        velAtaque = str(h) 
        pygame.display.update()


position_columna = [438, 515, 592, 669, 746]
position_fila = [38, 115, 192, 269, 346, 423, 500, 577, 654] 
listaHacha = []


"""------------------JUEGO----------------"""
def Juego():
##    tiempoInicio = pygame.time.get_ticks()
##    global auxTiempo
##    auxTiempo = 1
    global reloj
    reloj = pygame.time.get_ticks()//1000
    running = True
    TAM_CASILLA = 77 #Tamaño de cada casilla
    global monedas
    global matriz
    global rooks
    monedas = 5000 #Monedas del jugador
    tipo = 0 #Variable que determina que rook colocar
    global contEnemigos
    contEnemigos = 5 #Variable que determina cuando se supera el nivel
    global level
    level = 0

    #Texto de interfaz
    monedasText = font.render("Monedas: "+str(monedas), 1, MORADO_OSCURO)
    jugadorText = font.render("Jugador: "+str(jugador), 1, MORADO_OSCURO)
    #Imágenes
    fondo = pygame.image.load('lawn1.png')
    coinImgs = [pygame.image.load('Coin0.png'),pygame.image.load('Coin1.png'),pygame.image.load('Coin2.png')]
    rookImgs = [pygame.image.load("Sand.png"),pygame.image.load("Rock.png"), pygame.image.load("Fire.png"), pygame.image.load("Water.png")]
    bulletImgs = [pygame.image.load("Dust.png"), pygame.image.load("BulletRock.png"), pygame.image.load("Fireball.png"), pygame.image.load("Waterdrop.png")]
    muteImg = pygame.image.load('Mute.png')
    tableros = [pygame.image.load('lawn2.png'), pygame.image.load('lawn1.png'), pygame.image.load('lawn3.jpg')]
    #Efectos de sonido


    # Listas
    rooks = []
    coins = []
    enemigos = []
    enemigosDisponibles = ["Arquero","Escudero","Lenador","Canibal"]
    musica = mixer.music.load("Graze the Roof.mp3")
    pygame.mixer.music.play(-1)
    global estadoMusica
    estadoMusica = True
    #Instancias de botones
    botonSand = Button((0,255,0),55,200,100,70,rookImgs[0],None)
    botonRock = Button((0,255,0),200,200,100,70,rookImgs[1],None)
    botonFire = Button((0,255,0),55,300,100,70,rookImgs[2],None)
    botonWater = Button((0,255,0),200,300,100,70,rookImgs[3],None)
    botonQuit = Button((0,255,0),100,600,150,70,None,"Quit")
    botonMute = Button((0,255,0),60,500,100,70,muteImg,None)
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

    archivo = open("Configuracion.txt", "w")
    archivo.seek(0)
    archivo.write(str(a)+str(b)+str(i)+str(d)+str(e)+str(f)+str(g)+str(h))
    archivo.close()
    
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
            self.hitbox = (self.x + 20, self.y, 28, 60)

        def Move(self):
            n = matriz[self.c - 2][self.r]

            if self.kind == "Arquero":
                if n != 1 and n != 2 and n != 3 and n != 4:
                    if reloj % a == 0:  # Avance del arquero
                        if self.cont == 0:
                            matriz[self.c][self.r] = 0
                            self.c -= 1
                            self.cont = 1
                            matriz[self.c][self.r] = 5
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
                if n != 1 and n != 2 and n != 3 and n != 4:
                    if reloj % i == 0:  # Avance del escudero
                        if self.cont == 0:
                            matriz[self.c][self.r] = 0
                            self.c -= 1
                            self.cont = 1
                            matriz[self.c][self.r] = 6
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
                if n != 1 and n != 2 and n != 3 and n != 4:
                    if reloj % e == 0:                    # Avance del lenador
                        if self.cont == 0:
                            matriz[self.c][self.r] = 0
                            self.c -= 1
                            self.cont = 1
                            matriz[self.c][self.r] = 7
                    else:
                        self.cont = 0
                        self.imagenLenador = self.image
                if n == 1 or n == 2 or n == 3 or n == 4:
                    if reloj % f == 0:                   # Ataque del lenador
                        if self.cont2 == 0:
                            self.Attack()
                            self.cont2 = 1
                    else:
                        self.cont2 = 0
            elif self.kind == "Canibal":
                if n != 1.0 and n != 2.0 and n != 3.0 and n != 4.0:
                    if reloj % g == 0:  # Avance del canibal
                        if self.cont == 0:
                            matriz[self.c][self.r] = 0
                            self.c -= 1
                            self.cont = 1
                            matriz[self.c][self.r] = 8
                    else:
                        self.imagenLenador = self.image
                        self.cont = 0
                if n == 1 or n == 2 or n == 3 or n == 4:
                    if reloj % h == 0:  # Ataque del canibal
                        if self.cont2 == 0:
                            self.Attack()
                            self.cont2 = 1
                    else:
                        self.cont2 = 0

        def draw(self):
            self.hitbox = (self.x + 10, self.y, 28, 60)
            screen.blit(self.imagenLenador, (int(self.x), int(self.y)))
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

        def trayectoria(self):
            if self.y > position_fila[self.c-1]:
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
                self.list_attack.append(Bullet(self.kind, self.c, self.r, self.ataque))

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
                self.img = pygame.image.load('Images/h1.png')
                self.cambioY = -3
            elif tipo == "Canibal":
                self.img = pygame.image.load('Images/p1.png')
                self.cambioY = -3
                
        def draw(self):
            screen.blit(self.img,(int(self.x), int(self.y) ) )

        def trayectoria(self):
            c = int(math.floor(self.y/TAM_CASILLA))
            r = int(math.floor((self.x-400)/TAM_CASILLA))
            self.c = c
            self.r = r
            self.y += self.cambioY

##    clock = pygame.time.Clock()
##
##    enemigoCoolDown = 5000
##    enemigoCoolDowns = [3000, 4000, 5000]
##    tiempoEnemigo = pygame.time.get_ticks()

    
    if continuar:
        matriz = np.load("matrizJuego.npy")
    else:
        matriz = np.zeros((9,5))
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

##    def musica():
##        if level == 0:
##            if music
##    
    def nextLevel():
        global level, enemigoCoolDowns, contEnemigos, matriz, rooks
        level +=1
        contEnemigos = 5
        rooks = []
        matriz = np.zeros((9,5))
        enemigoCoolDowns = [enemigoCoolDowns[0]*0.3, enemigoCoolDowns[1]*0.3, enemigoCoolDowns[2]*0]

        if level == 3:
            continuar = False
            matriz = np.zeros((9,5))
            inicio()
            #Ganaste

            
    while running:
        global lenadorwalk, len_walk, listaHacha, lenadorattack, len_attack
        reloj = pygame.time.get_ticks()//1000

        #clock.tick(30)
        # Generar enemigos aleatoreamente
        relojEnemigo = pygame.time.get_ticks()
        if contEnemigos == 0 and len(enemigos) == 0:
            n = 0
            while n < 1000:
                #ANIMACIÓN DE VICTORIA
                n += 1
            nextLevel()

        if relojEnemigo - tiempoEnemigo > enemigoCoolDown and contEnemigos != 0:

            # Random choice: 0=arquero, 1=escudero, 2=lenador, 3=canibal
            avatarchoice = random.choice(enemigosDisponibles)
            x = randint(0,4)
            tiempoEnemigo = relojEnemigo
            # enemigoCoolDown = random.choice(enemigoCoolDowns)
            enemigos.append(Lenador(x, 8, avatarchoice))
            contEnemigos -= 1
            if matriz[8][x] == 0:
                if avatarchoice == 0:
                    matriz[8][x] = 5
                elif avatarchoice == 1:
                    matriz[8][x] = 6
                elif avatarchoice == 2:
                    matriz[8][x] = 7
                elif avatarchoice == 3:
                    matriz[8][x] = 8


        for event in pygame.event.get():
            #Mantiene la ventana abierta

            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                continuar = False
                running = False
                pygame.quit()
                sys.exit()

            #Asignar valor a la matriz se le hace click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 400 and pos[0] < 785:
                    #Valores en la matriz, colum y raw
                    c = int(math.floor((pos[0] - 400)/TAM_CASILLA))
                    r = int(math.floor(pos[1]/TAM_CASILLA))
                    if matriz[r][c] == 1 or matriz[r][c] == 2 or matriz[r][c] == 3 or matriz[r][c] == 4: #Quitar rooks
                        for rook in rooks:
                            if rook.r == c and rook.c == r:
                                rooks.remove(rook)
                                matriz[r][c] = 0
                    elif matriz[r][c] == 0: #Colocar rooks
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
                    inicio()
                else:
                    pass

            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotones:
                    if boton.isOver(pos):
                        boton.color = (0,0,255)
                    else:
                        boton.color = (0,255,0)

        #Mantener las instancias en pantalla
        screen.fill((200, 200, 200))
        screen.blit(tableros[level], (370, -19))
        monedasText = font.render("Monedas: " + str(monedas), 1, MORADO_OSCURO, (200,200,200))
        screen.blit(monedasText, (5, 10))
        screen.blit(jugadorText, (5, 40))
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
                    posMatriz = matriz[proyectil.c][proyectil.r]
                    if proyectil.y > 650:  # Comprueba si la posición de la bala sobrepasa el tablero, si lo hace, la elimina
                        rook.listaDisparos.remove(proyectil)
                    for enemigo in enemigos:
                        if proyectil.x > enemigo.x and proyectil.x < enemigo.x + enemigo.hitbox[2]:
                            if proyectil.y > enemigo.y and proyectil.y < enemigo.y + enemigo.hitbox[3]:
                                rook.listaDisparos.remove(proyectil)
                                enemigo.vida -= proyectil.dano
                                if enemigo.vida <= 0:
                                    monedas += 100
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

        pygame.display.update()

##Juego()


        

inicio()  
    

