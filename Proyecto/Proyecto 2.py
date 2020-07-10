import pygame,sys,math
import numpy as np
import random

import time

pygame.init()

#Variables globales
ancho = 900
alto = 700
fila = [145, 180, 220, 260, 300, 340, 375, 415, 435]
columna = [50, 95, 145, 190, 235]
lenadorwalk = False
len_walk = 1

#Colores
MORADO_CLARO = (184,112,204,80)
MORADO_OSCURO = (131,60,150,59)
GRIS = (214,202,252,99)
AMARILLO = (253,218,76,99)
CAFE = (201,184,141,79)
tablero = pygame.image.load('lawn2.png')
lista_avatar = []

#Ventana de Inicio
(width, height) = (900, 700)
screen = pygame.display.set_mode((width, height))
pygame.display.flip() #Mostrar ventana

# Titulo e ícono
pygame.display.set_caption("Avatars vs Rooks")
icon = pygame.image.load("icono.png")
pygame.display.set_icon(icon)

#Clase botones
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



def mainMenu():

    #Instancias de botones
    botonPlay = Button(MORADO_CLARO,155,100,100,70,None,"Play")
    botonSalon = Button(MORADO_CLARO,80,200,260,70,None,"Salon de la fama")
    botonConfig = Button(MORADO_CLARO,100,300,220,70,None,"Configuracion")
    botonAyuda = Button(MORADO_CLARO,160,400,110,70,None,"Ayuda")
    botonCreditos = Button(MORADO_CLARO,130,500,150,70,None,"Creditos")
    botonExit = Button(MORADO_CLARO,170,600,80,70,None,"Exit")
    listaBotones = [botonPlay,botonSalon,botonConfig,botonAyuda,botonCreditos,botonExit]

    # Loop del juego
    def loopVentana():
        screen.fill(GRIS)
        for boton in listaBotones:
            boton.draw(screen,(0,0,0))

    running = True
    while running:
        #Mantiene el color y los objetos en la ventana
        loopVentana()
        pygame.display.update()

        #Mantiene la ventana abierta
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()      #Cerrar pygame sin ventana de error

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonPlay.isOver(pos):
                    running = False
                    Juego()

            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotones:
                    if boton.isOver(pos):
                        boton.color = CAFE
                    else:
                        boton.color = AMARILLO

def Ayuda():
    running = True
    while running:
        pygame.display.update()

        #Mantiene la ventana abierta
        for event in pygame.event.get():
            pass


"""------------------JUEGO----------------"""

class Lenador(pygame.sprite.Sprite):   #Clase para los lenadores
    global position_fila, position_columna
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load('Images/le_c1.png')
        self.walk = [pygame.image.load('Images/le_c1.png'), pygame.image.load('Images/le_c2.png'), pygame.image.load('Images/le_c3.png'),
                     pygame.image.load('Images/le_c4.png'), pygame.image.load('Images/le_c5.png'), pygame.image.load('Images/le_c6.png'),
                     pygame.image.load('Images/le_c7.png'), pygame.image.load('Images/le_c8.png'), pygame.image.load('Images/le_c9.png'),
                     pygame.image.load('Images/le_c10.png'), pygame.image.load('Images/le_c11.png'), pygame.image.load('Images/le_c12.png'),
                     pygame.image.load('Images/le_c13.png'), pygame.image.load('Images/le_c14.png')]
        self.posImagen = 0
        self.imagenLenador = self.walk[self.posImagen]

        self.rect = self.image.get_rect()
        self.rect.centerx = position_columna[self.x]
        self.rect.centery = position_fila[self.y]

        self.list_attack = []
        self.life = True

        self.speed = 1

    def Move(self):
        pass
        '''
        if self.life:
            if self.rect.left <= 400:
                self.rect.left = 400
            elif self.rect.right > 700:
                self.rect.right = 700'''
    def avance(self, y, screen):
        n = 0
        while self.rect.centery > position_fila[y]:
            self.rect.centery -= self.speed
            print('n ',n)
            print('len ', len(self.walk)-1)
            if n < (len(self.walk)-1):
                n += 1
            else:
                print('entre')
                n = 0
            screen.blit(self.walk[n], self.rect)
        self.y  -= 1

    def Attack(self):
        pass

    def Draw(self, superficie):
        #if self.walkCount
        superficie.blit(self.image, self.rect)

position_columna = [438, 515, 592, 669, 746]
position_fila = [38, 115, 192, 269, 346, 423, 500, 577, 654]

def Juego():
##    tiempoInicio = pygame.time.get_ticks()
##    global auxTiempo
##    auxTiempo = 1
    running = True
    matriz = np.zeros((9,5))
    matriz[3][3] = 2 # número de prueba
    print(matriz) # pa probar
    TAM_CASILLA = 77 #Tamaño de cada casilla
    global monedas
    monedas = 500 #Monedas del jugador
    jugador = "Engret y LLordi" #Provicional
    tipo = 0 #Variable que determina que rook colocar
    global cooldownTracker
    cooldownTracker = 0
    

    #Texto de interfaz
    font = pygame.font.SysFont("Neuropol X Rg", 30)
    monedasText = font.render("Monedas: "+str(monedas), 1, MORADO_OSCURO)
    jugadorText = font.render("Jugador: "+str(jugador), 1, MORADO_OSCURO)
    #Imágenes
    fondo = pygame.image.load('lawn1.png')
    coinImg = [pygame.image.load('Coin0.png'),pygame.image.load('Coin1.png'),pygame.image.load('Coin2.png')]
    rookImgs = [pygame.image.load("Sand.png"),pygame.image.load("Rock.png"), pygame.image.load("Fire.png"), pygame.image.load("Water.png")] 
    bulletImgs = [pygame.image.load("Dust.png"), pygame.image.load("BulletRock.png"), pygame.image.load("Fireball.png"), pygame.image.load("Waterdrop.png")]
    muteImg = pygame.image.load('Mute.png')
    #Posiciones en el tablero

    # Lista de Rooks
    rooks = []
    #Instancias de botones
    botonSand = Button((0,255,0),55,200,100,70,rookImgs[0],None)
    botonRock = Button((0,255,0),200,200,100,70,rookImgs[1],None)
    botonFire = Button((0,255,0),55,300,100,70,rookImgs[2],None)
    botonWater = Button((0,255,0),200,300,100,70,rookImgs[3],None)
    botonQuit = Button((0,255,0),100,600,150,70,None,"Quit")
    botonMute = Button((0,255,0),60,500,100,70,muteImg,None)
    listaBotones = [botonSand, botonRock, botonFire, botonWater, botonQuit, botonMute]
    #Eventos con tiempo
    eventoDisparo = pygame.USEREVENT + 1
    pygame.time.set_timer(eventoDisparo, 4000)

    """
    Métodos:
    draw: despliega la imagen del rook
    atacar: determina si hay un enemigo en la columna
    """
    class Rook():
        def __init__(self, tipo, r, c, vida, coste, ptsAtaque, velAta, img):
            global monedas
            self.tipo = tipo
            self.r = r
            self.c = c
            self.vida = vida
            self.coste = coste
            self.ptsAtaque = ptsAtaque
            self.velAta = velAta
            self.img = img
            self.listaDisparos = []
            self.last_fire = 0
            if tipo == "Sand":   # Aquí van las respectivas variables de velocidad de ataque
                self.cooldown = 5000
            elif tipo == "Rock":
                self.cooldown = 5000
            elif tipo == "Fire":
                self.cooldown = 5000
            elif tipo == "Water":
                self.cooldown = 5000
            self.cooldown = 5000
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

####    class Coins():
####        def __init__(self, x, y, width, height, valor):
####            self.valor = valor
####            self.x = x
####            self.y = y
####            self.height = height
####            self.width = width
####            self.hitbox = (x,y,width,height)

        def draw(self,screen):
            screen.blit(self.img, (self.x,self.y))
            pygame.draw.rect(screen, (0,0,0), self.hitbox, 2)

    """
    Métodos:
    redraw: animación y movimiento de la bala
    """
    class Bullet():
        def __init__(self,tipo,r,c,ataque):
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
            self.ataque = ataque
            self.cambioY = 3
            self.estado = 1

        def draw(self):
            screen.blit(self.img,(int(self.x), int(self.y) ) )

        def trayectoria(self):
            self.y += self.cambioY

##        def redraw(self):
##            pos = [self.x,self.y]
##            screen.blit(self.img, (self.x,int(self.y)))
##            self.y += self.cambioY
####            self.c = int(math.floor((self.x - 400)/TAM_CASILLA))
####            self.r = int(math.floor(self.y/TAM_CASILLA))
##            c = int(math.floor((pos[0] - 400)/TAM_CASILLA))
##            r = int(math.floor(pos[1]/TAM_CASILLA))
##            if matriz[self.r][self.c] == 1: #Verificar si hay un monstruo, el 1 es temporal


    #Asigna un 1 a la posicion de la raiz de entrada
    def unoMatriz(r,c):
        matriz[r][c] = 1
        print(matriz)

    #Mantiene los botones y objetos en pantalla
    def loopVentana():
        global lenadorwalk, len_walk
        screen.blit(tablero, (370, 0))

        screen.fill(GRIS)
        screen.blit(tablero, (373, -17))
        avatar.Draw(screen)
        monedasText = font.render("Monedas: "+str(monedas), 1, MORADO_OSCURO,GRIS)
        screen.blit(monedasText,(5,10))
        screen.blit(jugadorText,(5,40))
        for boton in listaBotones:
            boton.draw(screen, (0,0,0))
        for rook in rooks:
            now = pygame.time.get_ticks()
            rook.draw()
            rook.atacar()
        for bullet in bullets:
            bullet.redraw()
        reloj = pygame.time.get_ticks()//1000
        print(reloj)
        if reloj % 4 == 0:
            lenadorwalk = True
        else:
            lenadorwalk = False
            len_walk = 1


    screen.fill((200, 200, 200))
    avatar = Lenador(1,8)  # llamar al lenador
            if now - rook.last_fire >= rook.cooldown:
                rook.last_fire = now
                rook.disparar()
            if len(rook.listaDisparos) != 0:
                for proyectil in rook.listaDisparos:
                    proyectil.draw()
                    proyectil.trayectoria()
                    if proyectil.y > 700:  # if posición del proyectil llega a una casilla con monstru:
                        rook.listaDisparos.remove(proyectil)




    avatar = Lenador()  # llamar al lenador
    inGame = True  # si aun el jugador sigue con vida

    clock = pygame.time.Clock()
    clock = pygame.time.Clock()


    while running:
        global lenadorwalk, len_walk, reloj
        clock.tick(30)
        keys = pygame.key.get_pressed() #si una tecla es presionada
        avatar.Move()
        loopVentana()

        #Mantiene la ventana abierta
        if inGame:
            if lenadorwalk and len_walk != 0:
                aux_y = avatar.y - 1
                avatar.avance(aux_y, screen)


                len_walk = 0
            if 8 % 5 == 0:
                # screen.blit(tablero, (0, 0))
                avatar.rect.top -= avatar.speed
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

##            if event.type == eventoDisparo:
##                for rook in rooks:
##                    rook.disparar()
            if inGame:
                if keys[pygame.K_DOWN]:
                    #screen.blit(tablero, (0, 0))
                    avatar.rect.bottom += avatar.speed
                if keys[pygame.K_UP]:
                    #screen.blit(tablero, (0, 0))
                    avatar.rect.top -= avatar.speed




            #Asignar valor a la matriz se le hace click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 400 and pos[0] < 785:
                    print(pos)
                    #Valores en la matriz, colum y raw
                    c = int(math.floor((pos[0] - 400)/TAM_CASILLA))
                    r = int(math.floor(pos[1]/TAM_CASILLA))
                    if matriz[r][c] == 1:
                        for rook in rooks:
                            if rook.r == c and rook.c == r:
                                rooks.remove(rook)
                                matriz[r][c] = 0
                    elif matriz[r][c] == 0:
                        if tipo == "Sand" and monedas >= 50:
                            rooks.append(Rook("Sand", c, r, 7, 50, 2, None, rookImgs[0]))
                            unoMatriz(r,c)
                        elif tipo == "Rock" and monedas >= 100:
                            rooks.append(Rook("Rock", c, r, 14, 100, 4, None, rookImgs[1]))
                            unoMatriz(r,c)
                        elif tipo == "Fire" and monedas >= 150:
                            rooks.append(Rook("Fire", c, r, 16, 150, 8, None, rookImgs[2]))
                            unoMatriz(r,c)
                        elif tipo == "Water" and monedas >= 150:
                            rooks.append(Rook("Water", c, r, 16, 150, 8, None, rookImgs[3]))
                            unoMatriz(r,c)

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
                    mainMenu()
                else:
                    pass
            if event.type == pygame.MOUSEMOTION:
                for boton in listaBotones:
                    if boton.isOver(pos):
                        boton.color = (0,0,255)
                    else:
                        boton.color = (0,255,0)
        clock.tick(90)




        pygame.display.update()

####        coinX = random.choice(position_fila)
####        coinY = random.choice(position_columna)
####
####        coin = (coinX,coinY)


##        player = player1.Lenador((random.choice(position_fila), 654))
##        def create_avatar(id):
##           player = player1.Lenador((random.choice(position_fila), 654))
##           lista_avatar.append(id)
##
##           time.sleep(10)
##           create_avatar(id + 1)

##        avatar_thread = Thread(target=create_avatar, args=[0])
##        avatar_thread.start()


##
##        def create_avatar():
##           player = player1.Lenador((random.choice(position_fila), 654))
##           lista_avatar.append(player)
##
##
##        screen.blit(fondo,(0,0))
##        screen.blit(player.image, player.rect)
Juego()
        #pygame.display.flip()

        

mainMenu()  
    

