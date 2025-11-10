import random
import pygame
from classes import *
from math import * 
from config import *

pygame.init()


# Configuração da tela 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Spike Storm")
clock = pygame.time.Clock()

# Imagem de início
start_image = pygame.image.load("Assets/Imagens/start_image.jpeg")
start_image = pygame.transform.scale(start_image, (WIDTH, HEIGHT))
background_image = pygame.image.load("Assets/Imagens/background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.image.load("Assets/Imagens/Player.png")
# Estado do jogo e botão Play
state = "menu"
font = pygame.font.SysFont(None, 64)
play_text = font.render("PLAY", True, (255, 255, 255))
play_button_width, play_button_height = 240, 90
play_button_rect = pygame.Rect(0, 0, play_button_width, play_button_height)
play_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 150)
jogador = Player(WIDTH - 800, HEIGHT -100, scale=(40, 40))
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu" and play_button_rect.collidepoint(event.pos):
                state = "game"

        elif event.type == pygame.KEYDOWN:
            # Espaço para pular no jogo
            if state == "game" and event.key == pygame.K_SPACE:
                # chama o método jump da classe Player
                try:
                    jogador.jump()
                except Exception:
                    if hasattr(jogador, 'gravidade'):
                        jogador.gravidade = -6
            if state == "menu" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                state = "game"

    screen.fill((30, 30, 30))

    if state == "menu":
        try:
            screen.blit(start_image, (0, 0))
        except Exception:
            screen.fill((30, 30, 30))

        # botão play
        pygame.draw.rect(screen, (0, 0, 0), play_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), play_button_rect, width=3, border_radius=12)
        text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, text_rect)

    else:
        screen.blit(background_image, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()