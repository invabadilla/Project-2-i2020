# -*- coding: utf-8 -*-

import pygame
import random
import player1
from threading import Thread
import time

pygame.init()
lista_avatar = []

# Definimos algunas variables que usaremos en nuestro código

ancho_ventana = 500
alto_ventana = 500
screen = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Nivel 1")

clock = pygame.time.Clock()

position_fila = [30, 75, 120, 165, 210]
position_columna = [125, 160, 200, 240, 280, 320, 360, 395, 435]


player = player1.Lenador((random.choice(position_fila), 435))
game_over = False

while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

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

pygame.quit ()
