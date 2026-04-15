import pygame
import sys
import math

# start pygame systems
pygame.init()

# start sound system
pygame.mixer.init()

# WINDOW
# create game window
screen = pygame.display.set_mode((800, 600))

# set title on top bar
pygame.display.set_caption("footballRetro")

# clock controls FPS
clock = pygame.time.Clock()

# SOUND
# load kick sound
kick_sound = pygame.mixer.Sound("dist/assets/kick.wav")
kick_sound.set_volume(0.6)
kick_channel = pygame.mixer.Channel(0)

# load cheer sound
cheer_sound = pygame.mixer.Sound("dist/assets/cheer.mp3")
cheer_sound.set_volume(0.8)
cheer_channel = pygame.mixer.Channel(1)

# FONTS
title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 60)
score_font = pygame.font.SysFont(None, 50)
timer_font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 70)

# MENU TEXT
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
game_duration = 30
game_start_time = None
winner_text = ""

# GOAL FLASH
goal_flash_time = 0

# MAIN GAME LOOP
running = True
while running:
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

    # GAME LOGIC DRAW
    elif game_state == "game":
        # calculate time passed
        seconds_passed = (pygame.time.get_ticks() - game_start_time) // 1000

        # calculate time left
        time_left = max(0, game_duration - seconds_passed)

        # convert to MM:SS
        minutes = time_left // 60
        seconds = time_left % 60
        timer_text = f"{minutes:02}:{seconds:02}"

        # when timer reaches zero, decide winner
        if time_left == 0:
            if left_score > right_score:
                winner_text = "Blue Wins!"
            elif right_score > left_score:
                winner_text = "Red Wins!"
            else:
                winner_text = "Draw!"
            game_state = "game_over"

        # BLUE MOVEMENT
        if blue_running:
            move_x = math.cos(math.radians(blue_angle)) * blue_speed
            move_y = math.sin(math.radians(blue_angle)) * blue_speed
            blue_x += move_x
            blue_y += move_y
        else:
            blue_angle += blue_rotation_speed
            if blue_angle >= 360:
                blue_angle -= 360

        # RED MOVEMENT
        if red_running:
            move_x = math.cos(math.radians(red_angle)) * red_speed
            move_y = math.sin(math.radians(red_angle)) * red_speed
            red_x += move_x
            red_y += move_y
        else:
            red_angle += red_rotation_speed
            if red_angle >= 360:
                red_angle -= 360

        # keep players inside the screen
        blue_x = max(0, min(blue_x, 800 - blue_width))
        blue_y = max(0, min(blue_y, 600 - blue_height))

        red_x = max(0, min(red_x, 800 - red_width))
        red_y = max(0, min(red_y, 600 - red_height))

        # BALL MOVEMENT
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # friction slows ball every frame
        ball_speed_x *= friction
        ball_speed_y *= friction

        # stop tiny ball movement
        if abs(ball_speed_x) < 0.1:
            ball_speed_x = 0
        if abs(ball_speed_y) < 0.1:
            ball_speed_y = 0

        # bounce off top
        if ball_y - ball_radius <= 0:
            ball_y = ball_radius
            ball_speed_y *= -1

        # bounce off bottom
        if ball_y + ball_radius >= 600:
            ball_y = 600 - ball_radius
            ball_speed_y *= -1

        # check if ball is in goal openings
        in_left_goal_opening = left_goal_y <= ball_y <= left_goal_y + goal_height
        in_right_goal_opening = right_goal_y <= ball_y <= right_goal_y + goal_height

        # bounce left wall if not in goal opening
        if ball_x - ball_radius <= 0 and not in_left_goal_opening:
            ball_x = ball_radius
            ball_speed_x *= -1

        # bounce right wall if not in goal opening
        if ball_x + ball_radius >= 800 and not in_right_goal_opening:
            ball_x = 800 - ball_radius
            ball_speed_x *= -1

        # current time used for kick sound cooldown
        current_time = pygame.time.get_ticks()

        # BLUE COLLISION
        blue_center_x = blue_x + blue_width / 2
        blue_center_y = blue_y + blue_height / 2

        dx1 = ball_x - blue_center_x
        dy1 = ball_y - blue_center_y
        distance1 = math.sqrt(dx1 * dx1 + dy1 * dy1)

        min_distance1 = ball_radius + max(blue_width, blue_height) / 2

        if distance1 < min_distance1 and distance1 != 0:
            # only play kick sound after cooldown
            if current_time - last_kick_time > kick_cooldown:
                kick_channel.stop()
                kick_channel.play(kick_sound)
                last_kick_time = current_time

            overlap = min_distance1 - distance1
            nx = dx1 / distance1
            ny = dy1 / distance1

            # push ball away from player
            ball_x += nx * overlap
            ball_y += ny * overlap

            # if blue is moving, kick ball in facing direction
            if blue_running:
                ball_speed_x = math.cos(math.radians(blue_angle)) * 9
                ball_speed_y = math.sin(math.radians(blue_angle)) * 9

        # RED COLLISION
        red_center_x = red_x + red_width / 2
        red_center_y = red_y + red_height / 2

        dx2 = ball_x - red_center_x
        dy2 = ball_y - red_center_y
        distance2 = math.sqrt(dx2 * dx2 + dy2 * dy2)

        min_distance2 = ball_radius + max(red_width, red_height) / 2

        if distance2 < min_distance2 and distance2 != 0:
            if current_time - last_kick_time > kick_cooldown:
                kick_channel.stop()
                kick_channel.play(kick_sound)
                last_kick_time = current_time

            overlap = min_distance2 - distance2
            nx = dx2 / distance2
            ny = dy2 / distance2

            ball_x += nx * overlap
            ball_y += ny * overlap

            if red_running:
                ball_speed_x = math.cos(math.radians(red_angle)) *  9
                ball_speed_y = math.sin(math.radians(red_angle)) * 9

        # GOAL DETECTION
        if ball_x - ball_radius <= 0 and in_left_goal_opening:
            right_score += 1
            cheer_channel.stop()
            cheer_channel.play(cheer_sound)
            goal_flash_time = pygame.time.get_ticks()

            # reset all positions after goal
            ball_x = 400
            ball_y = 300
            ball_speed_x = 0
            ball_speed_y = 0

            blue_x = 100
            blue_y = 100
            blue_angle = 0
            blue_running = False

            red_x = 650
            red_y = 250
            red_angle = 180
            red_running = False

        if ball_x + ball_radius >= 800 and in_right_goal_opening:
            left_score += 1
            cheer_channel.stop()
            cheer_channel.play(cheer_sound)
            goal_flash_time = pygame.time.get_ticks()

            ball_x = 400
            ball_y = 300
            ball_speed_x = 0
            ball_speed_y = 0

            blue_x = 100
            blue_y = 100
            blue_angle = 0
            blue_running = False

            red_x = 650
            red_y = 250
            red_angle = 180
            red_running = False

        # DRAW BACKGROUND AND FIELD
        # gray street-style background
        screen.fill((60, 60, 60))

        # dark top and bottom border strips
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, 800, 10))
        pygame.draw.rect(screen, (40, 40, 40), (0, 590, 800, 10))

        # vertical texture lines
        for i in range(0, 800, 40):
            pygame.draw.line(screen, (70, 70, 70), (i, 0), (i, 600), 1)

        # horizontal texture lines
        for i in range(0, 600, 40):
            pygame.draw.line(screen, (70, 70, 70), (0, i), (800, i), 1)

        # center markings
        pygame.draw.line(screen, (200, 200, 200), (400, 0), (400, 600), 2)
        pygame.draw.circle(screen, (180, 180, 180), (400, 300), 70, 2)

        # goals
        pygame.draw.rect(screen, (255, 255, 255), (left_goal_x, left_goal_y, goal_width, goal_height))
        pygame.draw.rect(screen, (255, 255, 255), (right_goal_x, right_goal_y, goal_width, goal_height))

        # left goal net
        for y in range(left_goal_y, left_goal_y + goal_height, 10):
            pygame.draw.line(screen, (200, 200, 200), (left_goal_x, y), (left_goal_x + goal_width, y), 1)
        for x in range(left_goal_x, left_goal_x + goal_width, 5):
            pygame.draw.line(screen, (200, 200, 200), (x, left_goal_y), (x, left_goal_y + goal_height), 1)

        # right goal net
        for y in range(right_goal_y, right_goal_y + goal_height, 10):
            pygame.draw.line(screen, (200, 200, 200), (right_goal_x, y), (right_goal_x + goal_width, y), 1)
        for x in range(right_goal_x, right_goal_x + goal_width, 5):
            pygame.draw.line(screen, (200, 200, 200), (x, right_goal_y), (x, right_goal_y + goal_height), 1)

        # draw ball
        pygame.draw.circle(screen, (0, 0, 0), (int(ball_x), int(ball_y)), ball_radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius, 2)

        # draw blue pointed player
        blue_surface = pygame.Surface((blue_width, blue_height), pygame.SRCALPHA)
        blue_points = [
            (0, 0),
            (0, blue_height),
            (blue_width * 0.7, blue_height),
            (blue_width, blue_height / 2),
            (blue_width * 0.7, 0),
        ]
        pygame.draw.polygon(blue_surface, (0, 100, 255), blue_points)
        rotated_blue = pygame.transform.rotate(blue_surface, -blue_angle)
        rotated_blue_rect = rotated_blue.get_rect(
            center=(blue_x + blue_width / 2, blue_y + blue_height / 2)
        )
        screen.blit(rotated_blue, rotated_blue_rect.topleft)

        # draw red pointed player
        red_surface = pygame.Surface((red_width, red_height), pygame.SRCALPHA)
        red_points = [
            (0, 0),
            (0, red_height),
            (red_width * 0.7, red_height),
            (red_width, red_height / 2),
            (red_width * 0.7, 0),
        ]
        pygame.draw.polygon(red_surface, (255, 0, 0), red_points)
        rotated_red = pygame.transform.rotate(red_surface, -red_angle)
        rotated_red_rect = rotated_red.get_rect(
            center=(red_x + red_width / 2, red_y + red_height / 2)
        )
        screen.blit(rotated_red, rotated_red_rect.topleft)

        # draw score
        score_text = score_font.render(f"{left_score}  -  {right_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(400, 40))
        screen.blit(score_text, score_rect)

        # draw timer
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=(400, 80))
        screen.blit(timer_surface, timer_rect)

        # draw white flash just after a goal
        if pygame.time.get_ticks() - goal_flash_time < 300:
            flash = pygame.Surface((800, 600))
            flash.set_alpha(120)
            flash.fill((255, 255, 255))
            screen.blit(flash, (0, 0))

    # GAME OVER SCREEN
    elif game_state == "game_over":
        screen.fill((20, 20, 20))

        game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 0))
        result_text = button_font.render(winner_text, True, (255, 255, 255))
        final_score_text = score_font.render(f"Final Score: {left_score} - {right_score}", True, (255, 255, 255))
        restart_text = score_font.render("Press Enter", True, (200, 200, 200))

        game_over_rect = game_over_text.get_rect(center=(400, 180))
        result_rect = result_text.get_rect(center=(400, 280))
        final_score_rect = final_score_text.get_rect(center=(400, 350))
        restart_rect = restart_text.get_rect(center=(400, 430))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(result_text, result_rect)
        screen.blit(final_score_text, final_score_rect)
        screen.blit(restart_text, restart_rect)

    # show updated frame
    pygame.display.update()

    # keep 60 FPS
    clock.tick(60)

# close game
pygame.quit()
sys.exit()