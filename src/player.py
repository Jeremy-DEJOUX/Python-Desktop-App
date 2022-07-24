import pygame
import os
import platform

from animation import AnimateSprite


class Player(AnimateSprite):

    def __init__(self, name, x, y):
        cwd = os.getcwd()
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12) #Pied du joueur
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()


    def move_right(self): self.position[0] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_up(self): self.position[1] -= self.speed

    def move_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self): #Përmet de se replacer avant la collision
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

