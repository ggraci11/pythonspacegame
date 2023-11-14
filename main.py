import pygame
pygame.font.init()



#VARIABLES
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters!")
DIVIDER_COLOR = (0,0,0)
FPS = 60
WIDTH_SHIP, HEIGHT_SHIP = (55,40)
DIVIDER = pygame.Rect(WIDTH//2 - 5 ,0 ,10 , HEIGHT)
BULLET_SPEED = 8
BULLET_COUNT = 20
HP_FONT = pygame.font.SysFont('comicsans', 40)
TEXT_COLOR = (255,255,255)
SPACE = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))



#RED SHIP
RED_SHIP_IMAGE = pygame.image.load("spaceship_red.png")
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE, (WIDTH_SHIP, HEIGHT_SHIP)), 90)
RED_HIT = pygame.USEREVENT + 1
RED_SHELL = (255,0,0)
#YELLOW SHIP
YELLOW_SHIP_IMAGE = pygame.image.load("spaceship_yellow.png")
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMAGE, (WIDTH_SHIP, HEIGHT_SHIP)), 270)
YELLOW_HIT = pygame.USEREVENT + 2
YELLOW_SHELL = (255,255,0)



def red_controls(red, keys_pressed):
#RED CONTOLS
    #LEFT
    if keys_pressed[pygame.K_a] and red.x - 5 > 0:
        red.x -= 5
    #RIGHT
    if keys_pressed[pygame.K_d] and red.x + 5 + red.width < DIVIDER.x:
        red.x += 5
    #UP
    if keys_pressed[pygame.K_w] and red.y - 5 > 0:
        red.y -= 5
    #DOWN
    if keys_pressed[pygame.K_s] and red.y + 5 + red.height < HEIGHT - 10:
        red.y += 5



def yellow_controls(yellow, keys_pressed):
#YELLOW CONTROLS
    #LEFT
    if keys_pressed[pygame.K_LEFT] and yellow.x - yellow.width > DIVIDER.x - 25:
        yellow.x -= 5
    #RIGHT
    if keys_pressed[pygame.K_RIGHT] and yellow.x - 5 < 850:
        yellow.x += 5
    #UP
    if keys_pressed[pygame.K_UP] and yellow.y - yellow.height + 35 > 0:
        yellow.y -= 5
    #DOWN
    if keys_pressed[pygame.K_DOWN] and yellow.y + yellow.height < HEIGHT - 18:
        yellow.y += 5



def draw_window(red, yellow, red_bullets, yellow_bullets, RED_HP, YELLOW_HP):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, DIVIDER_COLOR, DIVIDER)

    red_hp_text = HP_FONT.render("Health:" + str(RED_HP), 1, TEXT_COLOR)
    yellow_hp_text = HP_FONT.render("Health:" + str(YELLOW_HP), 1, TEXT_COLOR)
    WIN.blit(yellow_hp_text,(WIDTH - yellow_hp_text.get_width() - 10, 10))
    WIN.blit(red_hp_text, (10,10))

    WIN.blit(RED_SHIP, (red.x, red.y))
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))

    for bullets in red_bullets:
        pygame.draw.rect(WIN, RED_SHELL, bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_SHELL, bullets)

    pygame.display.update()



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red.remove(bullet)

def main():
    red = pygame.Rect(100, 320, WIDTH_SHIP, HEIGHT_SHIP)
    yellow = pygame.Rect(762, 320, WIDTH_SHIP, HEIGHT_SHIP)

    red_bullets = []
    yellow_bullets = []
    RED_HP = 10
    YELLOW_HP = 10
    clock = pygame.time.Clock()
    game_run = True

    while game_run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < BULLET_COUNT:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < BULLET_COUNT:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                RED_HP -= 1
               
            if event.type == YELLOW_HIT:
                YELLOW_HP -= 1
        winner_text = ""
        if RED_HP <= 0:
            winner_text = "Yellow Wins!"
        if YELLOW_HP <=0:
            winner_text = "Red Wins!"


        keys_pressed = pygame.key.get_pressed()
        red_controls(red, keys_pressed)
        yellow_controls(yellow, keys_pressed)
        draw_window(red, yellow, red_bullets, yellow_bullets, RED_HP, YELLOW_HP)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    pygame.quit()



if __name__ == "__main__":
    main()