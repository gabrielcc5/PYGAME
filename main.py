import random
import pygame
from classes import *
from math import * 
from config import *
import json
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("PYGAME/Assets/Som/videoplayback.mp3")
jump_sound = pygame.mixer.Sound("PYGAME/Assets/Som/Jump.wav")
jump_sound.set_volume(3.20)

# Sistema de recorde
HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    """Carrega o melhor tempo do arquivo"""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)
        except Exception:
            return 0
    return 0

def save_highscore(score):
    """Salva o novo recorde no arquivo"""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": score}, f)
    except Exception:
        pass

# Carrega recorde ao iniciar
highscore = load_highscore()
# highscore toalmente criado pelo Copilot

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
# Imagem de vitória (final)
victory_image = pygame.image.load("Assets/Imagens/victory.png").convert_alpha()
victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))  

# Estado do jogo e botão Play
state = "menu"
font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 36)
play_text = font.render("PLAY", True, (255, 255, 255))
win_text = font.render("VITÓRIA!", True, (0, 255, 0))
play_button_width, play_button_height = 240, 90
play_button_rect = pygame.Rect(0, 0, play_button_width, play_button_height)
play_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 150)
jogador = Player(WIDTH - 800, HEIGHT -100, scale=(40, 40))
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)

# Grupo de obstáculos
obstacle_group = pygame.sprite.Group()

# Spawn timer (ms)
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(500,1500) 

# Variáveis de dificuldade progressiva
game_start_time = None  # Será setado quando o jogo começar
GAME_DURATION = 45000  # 45 segundos em ms
obstacle_speed = 4
last_difficulty_increase = 0

# Variáveis para tela de vitória
win_time = None  # Marca quando a vitória aconteceu
WIN_DELAY = 5000  # 5 segundos em ms
win_score = None 

bg_x = 0
bg_speed = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu" and play_button_rect.collidepoint(event.pos):
                state = "game"
                # Inicializa o tempo de início do jogo
                game_start_time = pygame.time.get_ticks()
                last_spawn = game_start_time
                obstacle_speed = 4
                last_difficulty_increase = game_start_time
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            elif state == "win":
                # Volta ao menu
                state = "menu"
                pygame.mixer.music.stop()

        elif event.type == pygame.KEYDOWN:
            # Espaço para pular no jogo
            if state == "game" and event.key == pygame.K_SPACE:
                # chama o método jump da classe Player
                try:
                    jogador.jump()
                except Exception:
                    if hasattr(jogador, 'gravidade'):
                        jogador.gravidade = -6
                try:
                    jump_sound.play()
                except Exception:
                    pass
            if state == "menu" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                state = "game"
                # Inicializa o tempo de início do jogo
                game_start_time = pygame.time.get_ticks()
                last_spawn = game_start_time
                obstacle_speed = 4
                last_difficulty_increase = game_start_time
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            elif state == "win" and event.key == pygame.K_SPACE:
                # Volta ao menu
                state = "menu"
                pygame.mixer.music.stop()

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

        # Mostra o highscore no menu
        if highscore > 0:
            highscore_text = small_font.render(f"Highscore: {highscore}%", True, (200, 200, 200))
            highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(highscore_text, highscore_rect)

    # Desenha e atualiza o jogo somente quando no estado 'game'
    if state == "game":
        now = pygame.time.get_ticks()
        elapsed_time = now - game_start_time
        
        # Verifica se o jogador venceu (45 segundos)
        if elapsed_time >= GAME_DURATION:
            # Salva a porcentagem final (será 100 aqui)
            win_score = int(min(elapsed_time / GAME_DURATION * 100, 100))
            state = "win"
            # Marca o tempo da vitória (primeira vez que chega aqui)
            if win_time is None:
                win_time = now
            # Limpa obstáculos
            for o in obstacle_group:
                o.kill()
            obstacle_group.empty()

        
        # Aumenta dificuldade a cada 15 segundos
        elapsed_seconds = (now - game_start_time) // 1000  # tempo em segundos
        if elapsed_seconds > 0 and elapsed_seconds % 15 == 0 and (now - last_difficulty_increase) > 500:
            # Aumenta velocidade dos obstáculos
            obstacle_speed += 1
            last_difficulty_increase = now
        
        bg_x -= bg_speed
        if bg_x <= -WIDTH:
            bg_x = 0

        # Desenha duas cópias do background para scrolling contínuo
        screen.blit(background_image, (bg_x, 0))
        screen.blit(background_image, (bg_x + WIDTH, 0))

        # Atualiza sprites do jogo
        # Spawn de obstáculos
        if now - last_spawn > spawn_interval:
            last_spawn = now
            # Gera um novo intervalo aleatório para o próximo obstáculo
            spawn_interval = random.randint(500, 2000)  # varia entre 0.5 e 2 segundos
            # spawn em x logo fora da tela com a velocidade atual
            ob = Obstacle(WIDTH + 20, speed=obstacle_speed)
            obstacle_group.add(ob)
            all_sprites.add(ob)

        all_sprites.update()
        all_sprites.draw(screen)

        # Desenha barra de progresso
        progress_bar_width = 600
        progress_bar_height = 30
        progress_bar_x = (WIDTH - progress_bar_width) // 2
        progress_bar_y = 20
        
        # Calcula progresso (0.0 a 1.0)
        progress = min(elapsed_time / GAME_DURATION, 1.0)
        # Converte para porcentagem (0-100)
        percentage = int(progress * 100)
        
        # Desenha fundo da barra
        pygame.draw.rect(screen, (100, 100, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        
        # Desenha barra preenchida
        filled_width = int(progress_bar_width * progress)
        pygame.draw.rect(screen, (0, 255, 0), (progress_bar_x, progress_bar_y, filled_width, progress_bar_height))
        
        # Desenha borda da barra
        pygame.draw.rect(screen, (255, 255, 255), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
        
        # Desenha porcentagem dentro da barra
        percentage_text = small_font.render(f"{percentage}%", True, (255, 255, 255))
        text_rect = percentage_text.get_rect(center=(WIDTH // 2, progress_bar_y + progress_bar_height // 2))
        screen.blit(percentage_text, text_rect)

        # Colisão usando os rects de colisão reduzidos (menos sensível)
        for obstacle in obstacle_group:
            if jogador.collision_rect.colliderect(obstacle.collision_rect):
                # Calcula o tempo alcançado nesta tentativa
                current_score = percentage
                # Atualiza recorde se necessário
                if current_score > highscore:
                    highscore = current_score
                    save_highscore(highscore)
                
                state = "menu"
                pygame.mixer.music.stop()
                # limpa obstáculos e reseta sprites (mantém o jogador)
                for o in obstacle_group:
                    o.kill()
                obstacle_group.empty()
                all_sprites.empty()
                # reseta jogador posição e adiciona de novo
                jogador.rect.center = (WIDTH - 800, HEIGHT -100)
                jogador.vel_y = 0
                jogador.collision_rect.center = jogador.rect.center
                all_sprites.add(jogador)
                # reseta velocidade para o próximo jogo
                obstacle_speed = 4
                break

    # Tela de vitória
    elif state == "win":
        try:
            screen.blit(start_image, (0, 0))
        except Exception:
            screen.fill((30, 30, 30))

        # se quisermos mostrar a imagem apenas quando o jogador completou 100%
        if win_score == 100:
            img_rect = victory_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
            screen.blit(victory_image, img_rect)

        
        
        # Mostra o highscore
        if highscore == 100:
            record_text = small_font.render(f"Novo Highscore! 100%", True, (0, 255, 0))
        else:
            record_text = small_font.render(f"Highscore: {highscore}%", True, (200, 200, 200))
        record_rect = record_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(record_text, record_rect)
        
        # Calcula tempo restante para voltar ao menu
        now = pygame.time.get_ticks()
        time_remaining = max(0, (WIN_DELAY - (now - win_time)) // 1000)
        
        # Texto com countdown
        if time_remaining > 0:
            countdown_text = small_font.render(f"Voltando em {time_remaining}s...", True, (200, 200, 200))
            countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
            screen.blit(countdown_text, countdown_rect)
        else:
            # Após 5 segundos, volta automaticamente ao menu
            state = "menu"
            win_time = None
            pygame.mixer.music.stop()
        
        # Texto para voltar ao menu
        restart_text = small_font.render("Clique para voltar ao menu", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(FPS)



pygame.quit()