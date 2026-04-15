import pygame
import sys
import math

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FootballRetro")
clock = pygame.time.Clock()
running = True

# Sounds
kick_sound = pygame.mixer.Sound("src/assets/kick.wav") #load sound file
kick_sound.set_volume(0.5) #volume
kick_channel = pygame.mixer.Channel(0) #create a channel for the sound
cheer_sound = pygame.mixer.Sound("src/assets/cheer.mp3")
cheer_sound.set_volume(0.8)
cheer_channel = pygame.mixer.Channel(1) #no interference with kick sound


# Font
title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 60)
score_font = pygame.font.SysFont(None, 50)
timer_font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 70)

# Menu title and buttons
title_text = title_font.render("footballRetro", True, (255, 255, 0))
title_rect = title_text.get_rect(center=(400, 120))

start_text = button_font.render("START", True, (255, 255, 255))
exit_text = button_font.render("EXIT", True, (255, 255, 255))

start_rect = start_text.get_rect(center=(400, 280))
exit_rect = exit_text.get_rect(center=(400, 380))

# GAME STATE 
# menu = start menu
# game = active match
# game_over = final result screen
game_state = "menu"

# BLUE PLAYER 
blue_x = 100
blue_y = 100
blue_width = 50
blue_height = 30
blue_speed = 5
blue_angle = 0
blue_rotation_speed = 3
blue_running = False

# RED PLAYER
red_x = 650
red_y = 250
red_width = 50
red_height = 30
red_speed = 5
red_angle = 180
red_rotation_speed = 3
red_running = False

# BALL
ball_x = 400
ball_y = 300
ball_radius = 10
ball_speed_x = 0
ball_speed_y = 0
friction = 0.995

# GOALS
goal_width = 20
goal_height = 120

left_goal_x = 0
left_goal_y = 240

right_goal_x = 780
right_goal_y = 240

# SCORE
left_score = 0
right_score = 0

# SOUND COOLDOWN
# prevents kick sound from playing too many times in a row
last_kick_time = 0
kick_cooldown = 300

# TIMER
game_duration = 120
game_start_time = None
winner_text = ""

# GOAL FLASH 
goal_flash_time = 0



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # get current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # mouse clicks only matter in the menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                # if START clicked
                if start_rect.collidepoint(mouse_pos):
                    game_state = "game"

                    # start timer
                    game_start_time = pygame.time.get_ticks()

                    # reset score
                    left_score = 0
                    right_score = 0
                    winner_text = ""

                    # reset ball
                    ball_x = 400
                    ball_y = 300
                    ball_speed_x = 0
                    ball_speed_y = 0

                    # reset blue
                    blue_x = 100
                    blue_y = 100
                    blue_angle = 0
                    blue_running = False

                    # reset red
                    red_x = 650
                    red_y = 250
                    red_angle = 180
                    red_running = False

                # if EXIT clicked
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # when key is pressed
        if event.type == pygame.KEYDOWN:
            if game_state == "game":
                # blue uses SPACE
                if event.key == pygame.K_SPACE:
                    blue_running = True

                # red uses ENTER
                if event.key == pygame.K_RETURN:
                    red_running = True

            elif game_state == "game_over":
                # after match, ENTER returns to menu
                if event.key == pygame.K_RETURN:
                    game_state = "menu"

        # when key is released
        if event.type == pygame.KEYUP:
            if game_state == "game":
                if event.key == pygame.K_SPACE:
                    blue_running = False
                if event.key == pygame.K_RETURN:
                    red_running = False

    # MENU DRAW
    if game_state == "menu":
        screen.fill((20, 20, 20))
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(exit_text, exit_rect)
    
    



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()