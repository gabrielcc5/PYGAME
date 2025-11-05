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