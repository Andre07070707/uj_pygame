import pygame
import math
from time import sleep
from pygame.locals import *
from pygame import mixer

pygame.init()
#configuracao da tela e das cores 
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basketball Game")

white = pygame.Color('white')
black = pygame.Color('black')
red = pygame.Color('red')
blue = pygame.Color('blue')
green = pygame.Color('green')
orange = pygame.Color('orange')

#configuracao do player e da bola
player_width, player_height = 150, 210  
ball_radius = 15
player_pos = pygame.Vector2(width // 2, height - player_height)
ball_pos = pygame.Vector2(player_pos.x + player_width // 2, player_pos.y - ball_radius * 2)
ball_speed = pygame.Vector2(0, 0)
ball_in_motion = False

#inserir as imagens
campo = pygame.image.load("campo2.jpg").convert_alpha()
player_image = pygame.image.load('craque2.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

#connfiguracoes do cesto 
basket_width, basket_height = 112, 30
basket_pos = pygame.Rect(width // 2 - basket_width // 2, 50, basket_width, basket_height)
basket_speed = 5
basket_direction = 1  

#carregar a imagem do menu e configuracoes do lancamento da bolae mais
menuimage = pygame.image.load('campo3.jpg').convert_alpha()
clock = pygame.time.Clock()
running = True
launch_angle = 45
launch_speed = 0
max_launch_speed = 40
power_increase_rate = 0.5
launching = False
score = 0
lives = 5
game_state = "menu"

font = pygame.font.SysFont(None, 36)

#musica ed fundo
mixer.init()
mixer.music.load('basket.mp3')
mixer.music.play()

#funcao para desenhar os elementos da tela
def draw():
    screen.fill(white)
    screen.blit(campo , (0 , 0))
    pygame.draw.circle(screen, orange , (int(ball_pos.x), int(ball_pos.y)), ball_radius)
    pygame.draw.rect(screen, red, basket_pos)
    screen.blit(player_image, player_pos)
    draw_trajectory()
    draw_power_bar()
    draw_score()
    draw_lives()
    pygame.display.flip()

#funcao para desenhar o menu
def draw_menu():
    cnt = True
    while cnt:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(menuimage , (0 , 0))
        title_text = font.render("Basketball Game", True, white)
        play_text = font.render("Play", True, white)
        screen.blit(title_text, (285 , 130))
        screen.blit(play_text, (360 , 185 ))
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            cnt = False
        clock.tick(60)
#funcao para desenhar as vidas erstantes ao player
def draw_lives():
    score_text = font.render(f"Lives: {lives}", True, white)
    screen.blit(score_text, (width - 150, 135))

#funcao para desenhar a trajetoria
def draw_trajectory():
    if not ball_in_motion:
        angle_radians = math.radians(launch_angle)
        length = 200
        for i in range(0, length, 10):
            dx = i * math.cos(angle_radians)
            dy = i * math.sin(angle_radians)
            pygame.draw.circle(screen, white, (int(ball_pos.x + dx), int(ball_pos.y - dy)), 2)

def draw_power_bar():
    bar_height = 200
    bar_width = 20
    bar_x = 50
    bar_y = height - bar_height - 50
    power_height = int((launch_speed / max_launch_speed) * bar_height) #calcular a altura da bara de forca consoante a velocidade da bola
    pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, green, (bar_x, bar_y + bar_height - power_height, bar_width, power_height))

def draw_score():
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width - 150, 100))

def handle_input():
    global ball_in_motion, ball_speed, launch_angle, launch_speed, launching
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 5
        ball_pos.x -= 5
    if keys[pygame.K_d]:
        player_pos.x += 5
        ball_pos.x += 5
    if pygame.mouse.get_pressed()[0]:  
        launching = True
        launch_speed += power_increase_rate
        if launch_speed > max_launch_speed:
            launch_speed = max_launch_speed
    else:
        if launching:
            angle_radians = math.radians(launch_angle)
            ball_speed = pygame.Vector2(launch_speed * math.cos(angle_radians), -launch_speed * math.sin(angle_radians))
            ball_in_motion = True
            launch_speed = 0
            launching = False
    mouse_x, mouse_y = pygame.mouse.get_pos()
    launch_angle = math.degrees(math.atan2(ball_pos.y - mouse_y, mouse_x - ball_pos.x))

def update_ball():
    global ball_in_motion, score, basket_speed, lives
    if ball_in_motion:
        ball_speed.y += 0.5  #meio q a simular a acelaracao gravitica para ir diminuindo a velocidade da bola e basicamente criar um movimento parabolico
        ball_pos.x += ball_speed.x
        ball_pos.y += ball_speed.y
        if ball_pos.y > height:
            ball_in_motion = False
            reset_ball()
            lives -= 1
        if basket_pos.collidepoint(ball_pos.x, ball_pos.y):
            score += 1
            ball_in_motion = False
            reset_ball()
            if score %5 == 0:
                basket_speed +=3
    
                #acima e basicamente o aumento da velocidade do cesto consoante o score
def update_basket():
    global basket_pos, basket_direction, basket_speed, width
    basket_pos.x += basket_direction * basket_speed
    if basket_pos.x < 0 or basket_pos.x + basket_width > width:
        basket_direction *= -1  

def reset_ball():
    global ball_pos, ball_speed
    ball_pos.update(player_pos.x + player_width // 2, player_pos.y - ball_radius * 2)
    ball_speed.update(0, 0)

def main():
    global running, lives
    draw_menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        if lives == 0:
            break
        handle_input()
        update_ball()
        update_basket()  
        draw()
        clock.tick(60)

if __name__ == "__main__":
    main()