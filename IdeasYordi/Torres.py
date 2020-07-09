import pygame
pygame.init()
position_col = [438, 515, 592, 669, 746]
position_raw = [38, 115, 192, 269, 346, 423, 500, 577, 654]
sandImg = pygame.image.load("Sand.png")

(width, height) = (900, 700)
GRIS = (155,155,155)
screen = pygame.display.set_mode((width, height))
pygame.display.flip() #Mostrar ventana

class Rook():
    def __init__(self, r, c, vida, ataque, alcance, velMov, velAta, sandImg):
        self.x = position_raw[c]
        self.y = position_col[r] 
        self.vida = vida
        self.ataque = ataque
        self.alcance = alcance
        self.velMov = velMov
        self.velAta = velAta
        self.img = sandImg

        
    def draw(self):
        screen.blit(self.img, (self.x,self.y))
        
##        pygame.draw.rect(screen, (255,0,0), (self.x,self.y,self.x+50,self.y+50),0)
    
running = True
rooks = [Rook(2,3,8,8,3,3,3,sandImg)]
while running:
    #Mantiene el color y los objetos en la ventana
    pygame.display.update()
    for elem in rooks:
        elem.draw()
        
    #Mantiene la ventana abierta
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()     
            sys.exit()      #Cerrar pygame sin ventana de error


