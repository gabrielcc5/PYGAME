import pygame
from config import *

# Tela de início
class StartScreen: 
    def __init__(self, width, height, image_path="Assets/Imagens/Tela de início.png"):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (width, height))

class Background:
    def __init__(self, width, height, image_path="Assets/Imagens/background.png"):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="Assets/Imagens/Player.png", scale=(20, 20)):
        super().__init__()
        original_image = pygame.image.load(image_path).convert_alpha()
        original_image = pygame.transform.scale(original_image, (80,80))
        self.gravidade = 1
        self.image = original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

        self.vel_y = 0
        self.gravity = 0.6 
        self.jump_strength = -15
        self.grounded = False

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += int(self.vel_y)

        ground_y = HEIGHT - 70
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.grounded = True
        else:
            self.grounded = False

    def jump(self):
        if self.grounded:
            self.vel_y = self.jump_strength
            self.grounded = False
