import pygame,sys,math
import numpy as np
import random
import player1
from threading import Thread
import time

pygame.init()

#Variables globales
ancho = 900
alto = 700
fila = [145, 180, 220, 260, 300, 340, 375, 415, 435]
columna = [50, 95, 145, 190, 235]

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
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        #Dibuja el botón en la pantalla
    def draw(self,screen,outline=None):
        #Crea outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 45)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

        #Verifica si la posición del mouse está sobre el botón
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

#Instancias de botones
botonPlay = Button((0,255,0),155,100,100,70,"Play")
botonSalon = Button((0,255,0),80,200,260,70,"Salón de la fama")
botonConfig = Button((0,255,0),100,300,220,70,"Configuración")
botonAyuda = Button((0,255,0),160,400,110,70,"Ayuda")
botonCreditos = Button((0,255,0),130,500,150,70,"Créditos")
botonExit = Button((0,255,0),170,600,80,70,"Exit")
listaBotones = [botonPlay,botonSalon,botonConfig,botonAyuda,botonCreditos,botonExit]

def mainMenu():

    # Loop del juego
    def loopVentana():
        screen.fill((200,200,200))
        for elem in listaBotones:
            elem.draw(screen,(0,0,0))

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
                    Juego()

            if event.type == pygame.MOUSEMOTION:
                for elem in listaBotones:
                    if elem.isOver(pos):
                        elem.color = (0,0,255)
                    else:
                        elem.color = (0,255,0)

def Ayuda():
    running = True
    while running:
        pygame.display.update()

        #Mantiene la ventana abierta
        for event in pygame.event.get():
            pass


"""------------------JUEGO----------------"""

class Lenador(pygame.sprite.Sprite):   #Clase para los lenadores

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/le_c1.png')
        self.walk = [pygame.image.load('Images/le_c1.png'), pygame.image.load('Images/le_c2.png'), pygame.image.load('Images/le_c3.png'),
                     pygame.image.load('Images/le_c4.png'), pygame.image.load('Images/le_c5.png'), pygame.image.load('Images/le_c6.png'),
                     pygame.image.load('Images/le_c7.png'), pygame.image.load('Images/le_c8.png'), pygame.image.load('Images/le_c9.png'),
                     pygame.image.load('Images/le_c10.png'), pygame.image.load('Images/le_c11.png'), pygame.image.load('Images/le_c12.png'),
                     pygame.image.load('Images/le_c13.png'), pygame.image.load('Images/le_c14.png')]

        self.rect = self.image.get_rect()
        self.rect.centerx = 600
        self.rect.centery = 577

        self.list_attack = []
        self.life = True

        self.speed = 5

    def Move(self):
        if self.life:
            if self.rect.left <= 400:
                self.rect.left = 400
            elif self.rect.right > 700:
                self.rect.right = 700

    def Attack(self):
        pass

    def Draw(self, superficie):
        #if self.walkCount
        superficie.blit(self.image, self.rect)

def Juego():
    running = True
    matriz = np.zeros((9,5))
    matriz[3][3] = 3
    print(matriz)
    TAM_CASILLA = 77 #Tamaño de cada casilla
    global cont
    cont = 0
    #Imágenes
    fondo = pygame.image.load('lawn1.png')
    coinImg = [pygame.image.load('Coin0.png'),pygame.image.load('Coin1.png'),pygame.image.load('Coin2.png')]
    rookImgs = [pygame.image.load("Sand.png")] # Imagenes de rooks
    bulletImgs = [pygame.image.load("Dust.png")]
    #Posiciones en el tablero
    position_columna = [438, 515, 592, 669, 746]
    position_fila = [38, 115, 192, 269, 346, 423, 500, 577, 654]
    # Lista de Rooks
    rooks = []
    bullets = []

    class Rook():
        def __init__(self, tipo, r, c, vida, ptsAtaque, alcance, velMov, velAta, img):
            self.tipo = "Sand"
            self.r = r
            self.c = c
            self.vida = vida
            self.ptsAtaque = ptsAtaque
            self.alcance = alcance
            self.velMov = velMov
            self.velAta = velAta
            self.img = img


        def draw(self):
            screen.blit(self.img, (position_columna[self.r]-30,position_fila[self.c]-30))

        def atacar(self):
            global cont 
            ataque = False
            matrizTrans = np.transpose(matriz)
            for elem in matrizTrans[self.r]:
                if elem ==  3: #if elem es igual a monsturo*
                    ataque = True
                    break
            if ataque == True and cont == 0: #TEmporal, hace que solo se dispare una bala
                cont += 1
                bullets.append(Bullet(self.tipo, self.r, self.c, self.ptsAtaque))
            else:
                pass

######    class Coins():
######        def __init__(self, x, y, width, height, valor):
######            self.valor = valor
######            self.x = x
######            self.y = y
######            self.height = height
######            self.width = width
######            self.hitbox = (x,y,width,height)
######
######        def draw(self,screen):
######            screen.blit(self.img, (self.x,self.y))
######            pygame.draw.rect(screen, (0,0,0), self.hitbox, 2)

    class Bullet():
        def __init__(self,tipo,r,c,ataque):
            if tipo == "Sand":
                self.img = bulletImgs[0]
            self.r = r
            self.c = c
            self.x = position_columna[self.r] -15
            self.y = position_fila[self.c]
            self.ataque = ataque
            self.cambioY = 0.1
            self.estado = 1

        def redraw(self):
            screen.blit(self.img, (self.x,int(self.y)))
            self.y += self.cambioY
            self.c = int(math.floor((self.x - 400)/TAM_CASILLA))
            self.r = int(math.floor(self.y/TAM_CASILLA))
            if matriz[self.r][self.c] == 1: #Verificar si hay un monstruo, el 1 es temporal
                pass
                #eliminar bala

    #Asigna un 1 a la posicion de la raiz de entrada
    def unoMatriz(r,c):
        matriz[r][c] = 1
        print(matriz)

    screen.fill((200, 200, 200))
    avatar = Lenador()  # llamar al lenador
    inGame = True  # si aun el jugador sigue con vida





    while running:

        keys = pygame.key.get_pressed() #si una tecla es presionada
        avatar.Move()

        #Mantiene la ventana abierta
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

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
                    if matriz[r][c] == 0:
                        rooks.append(Rook("Sand", c, r, 8, 8, 3, 3, 3, rookImgs[0]))
                        unoMatriz(r,c)
                else:
                    pass

        screen.blit(tablero, (400, 15))
        avatar.Draw(screen)
        for elem in rooks:
            elem.draw()
            elem.atacar()
        for elem in bullets:
            elem.redraw()
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
##        clock.tick(5)
        

mainMenu()  
    

