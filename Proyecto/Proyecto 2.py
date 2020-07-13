import pygame,sys,math
import numpy as np
import random
from random import randint

import time

pygame.init()

#Variables globales
ancho = 900
alto = 700
fila = [145, 180, 220, 260, 300, 340, 375, 415, 435]
columna = [50, 95, 145, 190, 235]
lenadorwalk = False
lenadorattack = False
len_attack = 1
len_walk = 1
reloj = 0
lista_enemigos = []

#Velocidad de avance y ataque de los avatars 
#Arquero
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

#Colores
MORADO_CLARO = (184,112,204,80)
MORADO_OSCURO = (131,60,150,59)
GRIS = (214,202,252,99)
AMARILLO = (253,218,76,99)
CAFE = (201,184,141,79)
tablero = pygame.image.load('lawn2.png') #Que hace esto aquí? XD

#Diferentes fuentes
fontTitulo = pygame.font.SysFont("Neuropol X Rg", 50)
font = pygame.font.SysFont("Neuropol X Rg", 35)

#Ventana de Inicio
(width, height) = (900, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.flip() #Mostrar ventana

#Titulo e ícono
pygame.display.set_caption("Avatars vs Rooks")
icon = pygame.image.load("icono.png")
pygame.display.set_icon(icon)

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
    def __init__(self, color, x,y,width,height, img ,text=''):
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
            font = pygame.font.SysFont("SeriesOrbit", 35)
            text = font.render(self.text, 1, MORADO_OSCURO)
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

        #Verifica si la posición del mouse está sobre el botón
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True



def inicio():
    
    #Instancias de botones
    botonPlay = Button(MORADO_CLARO,155,100,100,70,None,"Play")
    botonSalon = Button(MORADO_CLARO,80,200,260,70,None,"Salon de la fama")
    botonConfig = Button(MORADO_CLARO,100,300,220,70,None,"Configuracion")
    botonAyuda = Button(MORADO_CLARO,160,400,110,70,None,"Ayuda")
    botonCreditos = Button(MORADO_CLARO,130,500,150,70,None,"Creditos")
    botonExit = Button(MORADO_CLARO,170,600,80,70,None,"Exit")
    listaBotones = [botonPlay,botonSalon,botonConfig,botonAyuda,botonCreditos,botonExit]
    #Variables para desplegar las diferentes secciones
    ayuda = False
    config = False
    salon = False
    creditos = False
    ventanas = [ayuda, config, salon, creditos]
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
    """----------"""
    running = True

    while running:
        screen.fill(GRIS)

        for boton in listaBotones: # Mantiene los botones
            boton.draw(screen,(0,0,0))

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
            pass
        elif creditos:
            pass
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()      #Cerrar pygame sin ventana de error

            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotones:
                    if boton.isOver(pos):
                        boton.color = CAFE
                    else:
                        boton.color = AMARILLO
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonPlay.isOver(pos):
                    running = False
                    Juego()
                elif botonSalon.isOver(pos):
                    for ventana in ventanas:
                        ventana = False
                    salon = True
                elif botonConfig.isOver(pos):
                    for ventana in ventanas:
                        ventana = False
                    config = True
                elif botonAyuda.isOver(pos):
                    for ventana in ventanas:
                        ventana = False
                    ayuda = True
                elif botonCreditos.isOver(pos):
                    for ventana in ventanas:
                        ventana = False
                    creditos = True
                elif botonExit.isOver(pos):
                    running = False
                    pygame.quit()
                    sys.exit()  
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
    matriz = np.zeros((9,5))
    matriz[3][3] = 2 # número de prueba
    TAM_CASILLA = 77 #Tamaño de cada casilla
    global monedas
    monedas = 500 #Monedas del jugador
    jugador = "Engret y LLordi" #Nombre del jugador
    tipo = 0 #Variable que determina que rook colocar


    #Texto de interfaz
    monedasText = font.render("Monedas: "+str(monedas), 1, MORADO_OSCURO)
    jugadorText = font.render("Jugador: "+str(jugador), 1, MORADO_OSCURO)
    #Imágenes
    fondo = pygame.image.load('lawn1.png')
    coinImgs = [pygame.image.load('Coin0.png'),pygame.image.load('Coin1.png'),pygame.image.load('Coin2.png')]
    rookImgs = [pygame.image.load("Sand.png"),pygame.image.load("Rock.png"), pygame.image.load("Fire.png"), pygame.image.load("Water.png")]
    bulletImgs = [pygame.image.load("Dust.png"), pygame.image.load("BulletRock.png"), pygame.image.load("Fireball.png"), pygame.image.load("Waterdrop.png")]
    muteImg = pygame.image.load('Mute.png')
    #Posiciones en el tablero

    # Listas
    rooks = []
    coins = []
    enemigosDisponibles = ['arquero', 'escudero', 'lenador', 'canibal']
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
            screen.blit(self.img, (position_columna[self.c]-30,position_fila[self.r]-15))

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
                if elem ==  2: #if elem es igual a monsturo*
                    ataque = True
                    break
            if ataque == True:
                self.listaDisparos.append(Bullet(self.tipo, self.r, self.c, self.ptsAtaque))
                #Crea la bala
            else:
                pass

    class Lenador(pygame.sprite.Sprite):  # Clase para los lenadores
        global position_fila, position_columna, a, b, i, d, e, f, g, h
        clock = pygame.time.Clock()
        def __init__(self, x, y, kind):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y
            self.kind = kind
            if self.kind == 0:
                self.image = pygame.image.load('Images/a_c1.png')
            elif self.kind == 1:
                self.image = pygame.image.load('Images/e_c1.png')
            elif self.kind == 2:
                self.image = pygame.image.load('Images/le_c1.png')
            elif self.kind == 3:
                self.image = pygame.image.load('Images/c_c1.png')
            self.walk = []  # [pygame.image.load('Images/le_c1.png'), pygame.image.load('Images/le_c2.png'), pygame.image.load('Images/le_c3.png'),
            # pygame.image.load('Images/le_c4.png'), pygame.image.load('Images/le_c5.png'), pygame.image.load('Images/le_c6.png'),
            # pygame.image.load('Images/le_c7.png'), pygame.image.load('Images/le_c8.png'), pygame.image.load('Images/le_c9.png'),
            # pygame.image.load('Images/le_c10.png'), pygame.image.load('Images/le_c11.png'), pygame.image.load('Images/le_c12.png'),
            # pygame.image.load('Images/le_c13.png'), pygame.image.load('Images/le_c14.png')]
            self.posImagen = 0
            self.tiempoCambio = 1
            self.imagenLenador = self.image
            self.rect = self.imagenLenador.get_rect()
            self.rect.centerx = position_columna[self.x]
            self.rect.centery = position_fila[self.y]
            self.list_attack = []
            self.speed = 1

            self.lenadorwalk = False
            self.len_walk = 1

        def Move(self):
            if self.kind == 0:
                if reloj % a == 0:  # Avance del arquero
                    self.lenadorwalk = True
                    self.entre()
                    self.len_walk = 0
                else:
                    self.lenadorwalk = False
                    self.len_walk = 1
                if reloj % b == 0:  # Ataque del arquero
                    self.lenadorattack = True

                else:
                    self.lenadorattack = False
                    self.len_attack = 1
            elif self.kind == 1:
                if reloj % i == 0:  # Avance del escudero
                    self.lenadorwalk = True
                    self.entre()
                    self.len_walk = 0
                else:
                    self.lenadorwalk = False
                    self.len_walk = 1
                if reloj % d == 0:  # Ataque del escudero
                    self.lenadorattack = True
                else:
                    self.lenadorattack = False
                    self.len_attack = 1
            elif self.kind == 2:
                if reloj % e == 0:  # Avance del lenador
                    self.lenadorwalk = True
                    self.entre()
                    self.len_walk = 0
                else:
                    self.lenadorwalk = False
                    self.len_walk = 1
                if reloj % f == 0:  # Ataque del lenador
                    self.lenadorattack = True
                else:
                    self.lenadorattack = False
                    self.len_attack = 1
            elif self.kind == 3:
                if reloj % g == 0:  # Avance del canibal
                    self.lenadorwalk = True
                    self.entre()
                    self.len_walk = 0
                else:
                    self.lenadorwalk = False
                    self.len_walk = 1
                if reloj % h == 0:  # Ataque del canibal
                    self.lenadorattack = True
                else:
                    self.lenadorattack = False
                    self.len_attack = 1

        def entre (self):
            if self.lenadorwalk and self.len_walk != 0:
                aux_y = self.y - 1
                self.avance(aux_y, screen)
                    
        def avance(self, y, screen):
            while self.rect.centery > position_fila[y]:
                self.posImagen += 1
                self.tiempoCambio += 1
                if self.posImagen > len(self.walk)-1:
                    self.posImagen = 0

                self.rect.centery -= self.speed
                self.Draw(screen)
                clock.tick(50)
            self.y  -= 1

        def Attack(self, x, y):
            myAtaque = Hacha(x,y,'Images/h1.png')
            self.list_attack.append(myAtaque)
            #print(len(self.list_attack))

        def Draw(self, superficie):
            #if self.walkCount
            self.imagenLenador = self.image
            superficie.blit(self.imagenLenador, self.rect)

    class Hacha(pygame.sprite.Sprite):
        def __init__(self, posx, posy, ruta):
            pygame.sprite.Sprite.__init__(self)   #Permite que la clase utilice los sprites
            self.imagenHacha = pygame.image.load(ruta)
            self.rect = self.imagenHacha.get_rect()
            self.speed = 5
            self.rect.top = posy
            self.rect.left = posx
            #self.disparoPersonaje = personaje

        def trayectoria(self):
            #if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.speed

        def Draw(self, screen):
            screen.blit(self.imagenHacha, self.rect)

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
            if tipo == "Sand":
                self.img = bulletImgs[0]
            elif tipo == "Rock":
                self.img = bulletImgs[1]
            elif tipo == "Fire":
                self.img = bulletImgs[2]
            elif tipo == "Water":
                self.img = bulletImgs[3]
            self.r = r
            self.c = c
            self.x = position_columna[self.r] -15
            self.y = position_fila[self.c]
            self.dano = dano
            self.cambioY = 3

        def draw(self):
            screen.blit(self.img,(int(self.x), int(self.y) ) )

        def trayectoria(self):
            r = int(math.floor(self.y/TAM_CASILLA))
            self.r = r
            self.c = c
            self.y += self.cambioY

    #Asigna un 1 a la posicion de la raiz de entrada
    def unoMatriz(r,c):
        matriz[r][c] = 1


    inGame = True  # si aun el jugador sigue con vida

    clock = pygame.time.Clock()

    enemigoCoolDown = 5000
    enemigoCoolDowns = [3000, 4000, 5000]
    tiempoEnemigo = pygame.time.get_ticks()


    while running:
        global lenadorwalk, len_walk, listaHacha, lenadorattack, len_attack, lista_enemigos
        reloj = pygame.time.get_ticks()//1000

        for elem in lista_enemigos:
            elem.Move()
            elem.Draw(screen)
            for x in elem.list_attack:
                x.trayectoria()
                x.Draw(screen)
                if x.rect.top < 1:
                    elem.list_attack.remove(x)

        global lenadorwalk, len_walk
        clock.tick(30)
        keys = pygame.key.get_pressed() #si una tecla es presionada


        for event in pygame.event.get():
            #Mantiene la ventana abierta
            if inGame:
                #Generar enemigos aleatoreamente


                relojEnemigo = pygame.time.get_ticks()

                if relojEnemigo - tiempoEnemigo > enemigoCoolDown:
                    # Random choice: 0=arquero, 1=escudero, 2=lenador, 3=canibal
                    avatarchoice = randint(0, 3)
                    x = randint(0, 4)
                    tiempoEnemigo = relojEnemigo
                    #enemigoCoolDown = random.choice(enemigoCoolDowns)
                    if matriz[8][x] == 0:
                        lista_enemigos.append(Lenador(x, 8, avatarchoice))
                        matriz[8][x] = 2



            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #Asignar valor a la matriz se le hace click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 400 and pos[0] < 785:
                    print(pos)
                    #Valores en la matriz, colum y raw
                    c = int(math.floor((pos[0] - 400)/TAM_CASILLA))
                    r = int(math.floor(pos[1]/TAM_CASILLA))
                    if matriz[r][c] == 1: #Quitar rooks
                        for rook in rooks:
                            if rook.r == c and rook.c == r:
                                rooks.remove(rook)
                                matriz[r][c] = 0
                    elif matriz[r][c] == 0: #Colocar rooks
                        if tipo == "Sand" and monedas >= 50:
                            rooks.append(Rook("Sand", c, r))
                            unoMatriz(r,c)
                        elif tipo == "Rock" and monedas >= 100:
                            rooks.append(Rook("Rock", c, r))
                            unoMatriz(r,c)
                        elif tipo == "Fire" and monedas >= 150:
                            rooks.append(Rook("Fire", c, r))
                            unoMatriz(r,c)
                        elif tipo == "Water" and monedas >= 150:
                            rooks.append(Rook("Water", c, r))
                            unoMatriz(r,c)
                    for coin in coins: #Obtener coin
                        if coin.r == r and coin.c == c:
                            monedas += coin.valor
                            coins.remove(coin)
                            matriz[r][c] = 0


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
        screen.blit(tablero, (370, 0))
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
                    posMatriz = matriz[proyectil.r][proyectil.c]
                    if proyectil.y > 680:  # Comprueba si la posición de la bala sobrepasa el tablero, si lo hace, la elimina
                        rook.listaDisparos.remove(proyectil)
                    elif posMatriz == 2:   # Comprueba si la posición de la bala alcanza un enemigo, si lo hace, la elimina
                        rook.listaDisparos.remove(proyectil)
                        """
                        for enemigo in lista_enemigos:
                            if matriz[enemigo.r][enemigo.c] == posMatriz:
                            enemigo.health -= proyectil.dano
                            if enemigo.health <= 0:
                                lista_enemigos.remove(enemigo)
                        """

        nowCoin = pygame.time.get_ticks()
        if nowCoin - tiempo >= coinCooldown: #Comprueba si se debe generar una moneda
            # Establece una posición aleatoria en la matriz
            rCoin = random.randint(0,8)
            cCoin = random.randint(0,4)
            tiempo = nowCoin
            coinCooldown = random.choice(coinCooldowns)
            if matriz[rCoin][cCoin] == 0: #Si la posición está vacia, la genera
                coins.append(Coin( rCoin, cCoin))
                matriz[rCoin][cCoin] = 3

        for coin in coins: #Mantiene el dibujo de la moneda en pantalla
            coin.draw()


        for elem in lista_enemigos:
            elem.Draw(screen)
            for x in elem.list_attack:
                x.Draw(screen)
                x.trayectoria()
                if x.rect.top < 1:
                    elem.list_attack.remove(x)


        pygame.display.update()



##        player = player1.Lenador((random.choice(position_fila), 654))
##        def create_avatar(id):
##           player = player1.Lenador((random.choice(position_fila), 654))
##           lista_avatar.append(id)
##
##           time.sleep(10)
##           create_avatar(id + 1)

##
##        def create_avatar():
##           player = player1.Lenador((random.choice(position_fila), 654))
##           lista_avatar.append(player)
##
##
##        screen.blit(fondo,(0,0))
##        screen.blit(player.image, player.rect)
##Juego()


        

inicio()  
    

