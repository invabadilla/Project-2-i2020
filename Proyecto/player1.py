import pygame
position_fila = [30, 75, 120, 165, 210]
position_columna = [125, 160, 200, 240, 280, 320, 360, 395, 435]

class Lenador(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('lenadortest1.png')
        self.sheet.set_clip(pygame.Rect(430, 32, 463, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        #self.x
        self.left_states = { 0: (430, 32, 463, 32), 1:(430, 32, 463, 32) }

        #avatar_thread = Thread(target=lambda: self.update(self.rect
    

    
    def update(self, direction ):
        if direction == 'left':
            self.clip(self.left_states)
            self.rect.y -= 5

        if direction == 'stand_left':
            self.clip(self.left_states[0])
        self.image = self.sheet.subsurface(self.sheet.get_clip())


    '''    
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

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')
    '''
