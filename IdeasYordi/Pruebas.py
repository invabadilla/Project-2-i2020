import pygame

class Game:
    def __init__(self):
        self.width = 1000
        self.height = 700
        self.win = pygame.display.set_mode(self.width, self.height)
        self.enemys = []
        selftowers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load("bg.png")

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()

class Enemy:

    imgs = []
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.health = []
        self.path = []
        self.img = None


    def draw(self,win):


        self.animation_count += 1
        self.img = self.imgs[self.animation_count]
        if self.animation_count >=len(self.imgs):
            self.animation_count = 0
        win.blit(self.img, self(self.x, self.y))
        self.move()

    def collide(self, X, Y):



        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + height and Y >= self.y:
                return True



        return False
    def move(self):
        pass

        



enemy1 = Enemy(23,54,30,30)
enemy2 = Enemy(23,54,30,30)

enemigos = [enemy1, enemy2]


print(len(enemigos))
del enemy1
print(len(enemigos))
print(enemy1)














































            
