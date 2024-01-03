
import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
GROUND_HEIGHT = 20
GROUND_COLOR = (0, 255, 0)
FPS = 60

# width, height = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
pygame.display.set_caption("Bouncy Ball")
clock = pygame.time.Clock()

b1 = pygame.image.load("b1.png")
b2 = pygame.image.load("b2.png")
b3 = pygame.image.load("b3.png")
arch = pygame.image.load("arch.png")
rat = pygame.image.load("rat.png")
pigeon = pygame.image.load("pigeon.png")
star = pygame.image.load("star.png")

b1_width, b1_height = 150, 200
b1 = pygame.transform.scale(b1, (b1_width, b1_height))

b2_width, b2_height = 180, 330
b2 = pygame.transform.scale(b2, (b2_width, b2_height))

arch_width, arch_height = 150, 220
arch = pygame.transform.scale(arch, (arch_width, arch_height))

b3_width, b3_height = 120, 500
b3 = pygame.transform.scale(b3, (b3_width, b3_height))

rat_width, rat_height = 30, 30
rat = pygame.transform.scale(rat, (rat_width, rat_height))

pigeon_width, pigeon_height = 30, 30
pigeon = pygame.transform.scale(pigeon, (pigeon_width, pigeon_height))

star_width, star_height = 30, 30
star = pygame.transform.scale(star, (star_width, star_height))

pigeon_x, pigeon_y = -pigeon_width, random.randint(0, HEIGHT // 2)
pigeon_speed = 5

b1_x, b1_y = -100, 400
b2_x, b2_y = 370, 300
b3_x, b3_y = 630, 200
arch_x, arch_y = 120, 400
rat_x, rat_y = 370, 270
star_x, star_y = 440, 80

initial_ball_pos = [10, 150]
initial_ball_speed = [5, 0]  # Initial Speed
jump_speed = -15
gravity = 1
on_ground = True
jump_timer = 0
rat_speed = 2
moving_right = True

ball_pos = initial_ball_pos.copy()
ball_speed = initial_ball_speed.copy()

ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
arch_rect = pygame.Rect(arch_x, arch_y, arch_width, arch_height)
star_rect = pygame.Rect(star_x, star_y, star_width, star_height)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_pos[0] - BALL_RADIUS > 0:
        ball_speed[0] = -5
    elif keys[pygame.K_RIGHT] and ball_pos[0] + BALL_RADIUS < WIDTH:
        ball_speed[0] = 5
    else:
        ball_speed[0] = 0

    ball_pos[0] += ball_speed[0]

    # Collision detection with b1
    if b1_x < ball_pos[0] < b1_x + b1_width and ball_pos[1] + BALL_RADIUS > b1_y:
        ball_pos[1] = b1_y - BALL_RADIUS
        ball_speed[1] = 0
        on_ground = True
    elif b2_x < ball_pos[0] < b2_x + b2_width and ball_pos[1] + BALL_RADIUS > b2_y:
        ball_pos[1] = b2_y - BALL_RADIUS
        ball_speed[1] = 0
        on_ground = True
    elif b3_x < ball_pos[0] < b3_x + b3_width and ball_pos[1] + BALL_RADIUS > b3_y:
        ball_pos[1] = b3_y - BALL_RADIUS
        ball_speed[1] = 0
        on_ground = True
    elif arch_rect.colliderect(
            pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
        ball_pos[1] = arch_rect.top - BALL_RADIUS
        ball_speed[1] = jump_speed
        on_ground = True

    # Collision detection with star
    if star_rect.colliderect(
            pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
        print("Congratulations! You reached the star!")
        running = False  # You can add more logic for winning the game

    # Apply gravity if not on b1, b2, or arch
    if not on_ground:
        ball_speed[1] += gravity
        ball_pos[1] += ball_speed[1]

    # Ball bouncing off the ground
    if ball_pos[1] + BALL_RADIUS > HEIGHT - GROUND_HEIGHT:
        ball_pos[1] = HEIGHT - GROUND_HEIGHT - BALL_RADIUS
        ball_speed[1] = 0
        on_ground = True

    # Automatic jump (every 0.2 seconds)
    if on_ground:
        jump_timer += 1
        if jump_timer >= FPS * 0.2:
            ball_speed[1] = jump_speed
            on_ground = False
            jump_timer = 0

    # Bounce off the walls
    if ball_pos[0] - BALL_RADIUS < 0 or ball_pos[0] + BALL_RADIUS > WIDTH:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] + BALL_RADIUS >= HEIGHT - GROUND_HEIGHT:
        ball_pos = initial_ball_pos.copy()
        ball_speed = initial_ball_speed.copy()

    screen.fill("cyan2")

    if moving_right:
        rat_x += rat_speed
        if rat_x + rat_width > 570:  # Reverse direction when reaching right edge
            moving_right = False
    else:
        rat_x -= rat_speed
        if rat_x < 370:  # Reverse direction when reaching left edge
            moving_right = True
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

    pigeon_x += pigeon_speed

    if pigeon_x > WIDTH:
        pigeon_x = 0
        pigeon_y = random.randint(0, HEIGHT // 2)

    ball_rect = pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS,
                            BALL_RADIUS * 2, BALL_RADIUS * 2)
    rat_rect = pygame.Rect(rat_x, rat_y, rat_width, rat_height)
    pigeon_rect = pygame.Rect(pigeon_x, pigeon_y, pigeon_width, pigeon_height)

    if ball_rect.colliderect(rat_rect):
        ball_pos = initial_ball_pos.copy()
        ball_speed = initial_ball_speed.copy()

    # Check collision with the pigeon
    elif ball_rect.colliderect(pigeon_rect):
        ball_pos = initial_ball_pos.copy()
        ball_speed = initial_ball_speed.copy()

      # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])),
                     BALL_RADIUS)
    screen.blit(b1, (b1_x, b1_y))
    screen.blit(arch, (arch_x, arch_y))
    screen.blit(b2, (b2_x, b2_y))
    screen.blit(b3, (b3_x, b3_y))
    screen.blit(rat, (rat_x, rat_y))
    screen.blit(pigeon, (pigeon_x, pigeon_y))
    screen.blit(star, (star_x, star_y))

    pygame.display.flip()
    clock.tick(FPS)
        

pygame.quit()
sys.exit()

