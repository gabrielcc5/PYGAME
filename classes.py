import pygame
# Tela de início
class StartScreen:
    def __init__(self, screen, clock, width, height, fps, image_path):
        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height
        self.fps = fps
        
        self.image = pygame.image.load("C:\Users\anacl\OneDrive\Documents\PyGame\PYGAME\Assets\Imagens\Tela de início.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.img_rect = self.image.get_rect(center=(width // 2, height // 2))