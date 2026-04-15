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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()