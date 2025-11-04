import random
import pygame
from classes import *
from math import * 

pygame.init()

WIDTH, HEIGHT = 1424, 900
FPS = 100

# Configuração da tela 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Spike Storm")
clock = pygame.time.Clock()

# Imagem de início
start_image = pygame.image.load("Assets/Imagens/Tela de início.png").convert()



running = True
while running:
    screen.blit(start_image, (0, 0))

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip() 

pygame.quit()