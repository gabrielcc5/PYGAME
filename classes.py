import pygame

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
        self.image = original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
