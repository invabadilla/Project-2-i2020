import pygame,sys,math
import numpy as np
import random
import player1
from threading import Thread
import time

pygame.init()

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
        screen.fill((255,0,0))
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

def Juego():
    running = True
    matriz = np.zeros((9,5))
    print(matriz)

    def unoMatriz(r,c):
        matriz[r][c] = 1
        print(matriz)
    
    def loopVentana():
        screen.fill((255,0,0))
        

    while running:
        loopVentana()
        pygame.display.update()
        #Mantiene la ventana abierta
        for event in pygame.event.get():
            tamCasilla = 77 #Tamaño de cada casilla
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
                    c = int(math.floor((pos[0] - 400)/tamCasilla))
                    r = int(math.floor(pos[1]/tamCasilla))
                    unoMatriz(r,c)
                else:
                    pass

        position_fila = [30, 75, 120, 165, 210]
        position_columna = [125, 160, 200, 240, 280, 320, 360, 395, 435]


        player = player1.Lenador((random.choice(position_fila), 435))
        def create_avatar():
           player = player1.Lenador((random.choice(position_fila), 435))
           lista_avatar.append(player)

           time.sleep(10)
           create_avatar()
                               
        avatar_thread = Thread(target=create_avatar)#, args=[0])
        avatar_thread.start()
                               
        fondo = pygame.image.load('egipto.jpg')

        def create_avatar():
           player = player1.Lenador((random.choice(position_fila), 435))
           lista_avatar.append(player)
                               
        
        screen.blit(fondo,(0,0))
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(5)
        

mainMenu()  
    

