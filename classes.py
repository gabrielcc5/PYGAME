import pygame

# Tela de início
class StartScreen: 
    def __init__(self, width, height, image_path="Assets/Imagens/Tela de início.png"):
        self.image = pygame.image.load(image_path).convert()