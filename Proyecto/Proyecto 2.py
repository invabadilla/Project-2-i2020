import pygame,sys,math
import numpy as np
import random
from random import randint
import player1
from threading import Thread
import time

pygame.init()

lista_avatar = []
position_fila = [30, 75, 120, 165, 210]
position_columna = [125, 160, 200, 240, 280, 320, 360, 395, 435]

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
listaBotones = [botonPlay, botonSalon, botonConfig, botonAyuda, botonCreditos, botonExit]

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

def Juego():
    '''
    matriz = np.zeros((9,5))
    print(matriz)

    def unoMatriz(r,c):
        matriz[r][c] = 1
        print(matriz)
    '''
    def loopVentana():
        screen.fill((200,200,200))

    #screen = py.display.set_mode((284,500))

    class Lenador():
        def __init__(self, x, y, id, pantalla):
            self.fila = [30, 75, 120, 165, 210]
            self.columna = [125, 160, 200, 240, 280, 320, 360, 395, 435]
            self.x = x
            self.y = y
            self.id = id
            self.screen = screen
            self.sheet = pygame.image.load('lenadortest1.png')
            self.sheet.set_clip(pygame.Rect(430, 32, 463, 32))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect = self.image.get_rect()
            print(x,y,self.id)
            self.position = (self.fila[x], self.columna[y])
            #self.rect.topleft = position
            self.frame = 0

            self.left_states = {0: (430, 32, 463, 32), 1: (430, 32, 463, 32)}
            self.screen.blit(self.image, self.position)
            avatar1_thread = Thread(target=lambda: self.update(self.image, self.position))
            avatar1_thread.daemon = True
            avatar1_thread.start()

        def get_frame(self, frame_set):
            self.frame += 1
            if self.frame > (len(frame_set) - 1):
                self.frame = 0
            return frame_set[self.frame]

        def clip(self, clipped_rect):
            if type(clipped_rect) is dict:
                self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
            else:
                self.sheet.set_clip(pygame.Rect(clipped_rect))
            return clipped_rect

        def update(self, image, position):
            global position_fila
            print('pos ',self.position[1],position_fila[self.x+1])
            if self.position[1] > position_fila[self.x+1] :
                self.clip(self.left_states)
                self.rect.y -= 5
            elif self.position == position_fila[self.x+1]:
                self.clip(self.left_states[0])
                self.x =+1

            self.image = self.sheet.subsurface(self.sheet.get_clip())

    clock = pygame.time.Clock()
    game_over = False

    while game_over == False:
        loopVentana()
        pygame.display.update()
        #Mantiene la ventana abierta
        for event in pygame.event.get():
            tamCasilla = 77 #Tamaño de cada casilla
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                game_over = True

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

        def create_avatar(id):
            global lista_avatar
            x = randint(0, 4)
            y = 8
            avatar = Lenador(x, y, id, screen)
            lista_avatar.append(id)

            time.sleep(10)
            create_avatar(id + 1)
                               
        avatar_thread = Thread(target=create_avatar, args=[0])
        avatar_thread.start()
                               
        fondo = pygame.image.load('egipto.jpg')
        
        screen.blit(fondo,(0,0))


        pygame.display.flip()
        clock.tick(0.5)
    pygame.quit()

mainMenu()  
    

