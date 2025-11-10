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


class Obstacle(pygame.sprite.Sprite):
    """Obstáculo que se move para a esquerda e morre fora da tela.
    Usa `Assets/Imagens/obstacle.png` se existir; caso contrário desenha um retângulo vermelho.
    """
    def __init__(self, x, speed=4, image_path="Assets/Imagens/obstacle.png", scale=(60, 60)):
        super().__init__()
        try:
            img = pygame.image.load(image_path).convert_alpha()
            if scale is not None:
                img = pygame.transform.scale(img, scale)
            self.image = img
        except Exception:
            w, h = scale if scale is not None else (60, 60)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((200, 30, 30))
            self.image = surf

        self.rect = self.image.get_rect()
        self.rect.left = x
        # Alinha o obstáculo ao chão do jogo (mesma referência usada pelo Player)
        ground_y = HEIGHT - 90
        self.rect.bottom = ground_y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
