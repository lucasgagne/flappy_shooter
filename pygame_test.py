#WE NEED TO TRACK WHEN BULLETS HIT WALLS, WE NEED TO TRACK WHEN BIRD HITS WALLS. 
import pygame
import os
pygame.font.init()
import random


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoota Game")

WHITE = (100, 100, 100)
FPS = 60
VEL = 25
BULLET_VEL = 20
ENEMY_HEIGHT = 70
ENEMY_WIDTH = 50
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
BIRD_WIDTH = 70
BIRD_HEIGHT = 50
SCROLL_VEL = 5
LIGHT_WIDTH = 50


LIGHT_IMAGE = pygame.image.load(os.path.join("images", "light.png")).convert()
BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.jpeg")).convert()
BACKGROUND_WIDTH = BACKGROUND_IMAGE.get_width()
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH - 100, HEIGHT))
BULLET_IMAGE = pygame.image.load(os.path.join("images", "bullet.png"))
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "thug.png"))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
BIRD_IMAGE = pygame.image.load(os.path.join("images", "bird.png"))
#Rotate bird below and rescale it
BIRD = pygame.transform.rotate(pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT)), 10)
MAX_BULLETS = 2
ENEMY_HIT = pygame.USEREVENT + 1
PLAYER_DIE = pygame.USEREVENT + 2


class enemy:
    health = 0
    rand_height = random.randint(80, 350)
    rect = pygame.Rect(WIDTH + 200, rand_height , ENEMY_WIDTH, ENEMY_HEIGHT)

    def __init__(self, health, enemy_list):
        self.health = health
        enemy_list.append(self)
        self.enemy_list = enemy_list
    

    
def create_lights(light_list):
    #Place light barriers every 100 pixels
    new_list = []
    image_list = []
    for i in range(4):
        rand_height1 = random.randint(HEIGHT // 5, HEIGHT // 3)
        LIGHT1 = pygame.transform.rotate(pygame.transform.scale(LIGHT_IMAGE, (LIGHT_WIDTH, rand_height1)), 180)
        rand_height2 = random.randint(HEIGHT // 5, HEIGHT // 3)
        LIGHT2 = pygame.transform.scale(LIGHT_IMAGE, (LIGHT_WIDTH, rand_height2))

        new_list.append(pygame.Rect(WIDTH+ (600*i), 0, LIGHT_WIDTH, rand_height1))
        new_list.append(pygame.Rect(WIDTH+ (600*i), HEIGHT - rand_height2, LIGHT_WIDTH, rand_height2))
        
        image_list.append(LIGHT1)
        image_list.append(LIGHT2)
    light_list = new_list
    return light_list, image_list

        


def drawWindow(rect, bird_bullets, kill_count, scroll, enemy_list, light_list, images):
    #IF WE WANT TO MAKE A DRAWING TEMPLATE, WE CAN SIMPLY NOT DRAW A BACKGROUND...
    for i in range(3):
        WIN.blit(BACKGROUND, (i*(WIDTH-100) + scroll, 0) )
    WIN.blit(BIRD, (rect.x, rect.y))
    #Draw lights
    for i in range(len(light_list)):
        light_list[i].x -= SCROLL_VEL
        WIN.blit(images[i], (light_list[i].x, light_list[i].y))
    for enemy in enemy_list:
        enemy.rect.x -= SCROLL_VEL
        WIN.blit(ENEMY, (enemy.rect.x, enemy.rect.y))
        if enemy.rect.x  <  -5:
            enemy.rect.x = WIDTH + 200
            enemy.rect.y = random.randint(80, 400)
        if enemy.health == 0:

            enemy_list.remove(enemy)
            enemy.rect.x = -500
            enemy.rect.y = -500
            kill_count += 1
        #CHECK IF ENEMY CONTACTS BIRD
        if enemy.rect.colliderect(rect):
                pygame.event.post(pygame.event.Event(PLAYER_DIE))
    #CHECK IF BIRD CONTACTS WALL
    for wall in light_list:
        if wall.colliderect(rect):
            pygame.event.post(pygame.event.Event(PLAYER_DIE))
    #Check if bird flew too low
    if rect.y > (HEIGHT ):
        pygame.event.post(pygame.event.Event(PLAYER_DIE))

    for bullet in bird_bullets:
        WIN.blit(BULLET_IMAGE, (bullet.x, bullet.y))
    if kill_count > 0:
        font = pygame.font.SysFont('Calibri', 25, True, False) 
        text = font.render("KILL COUNT: " + str(kill_count), True, (255, 87, 51)) # in line 48
        WIN.blit(text, (0, 0))
   
    pygame.display.update()
    

def physics(rect):
    rect.y += 15


def handle_bullets(bird_bullets, enemy_list, wall_list):
    for bullet in bird_bullets:
        bullet.x += BULLET_VEL
        for en in enemy_list:
            if en.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                bird_bullets.remove(bullet)
        for wall in wall_list:
            if wall.colliderect(bullet):
                bird_bullets.remove(bullet)
        if bullet.x > WIDTH:
            bird_bullets.remove(bullet)
            

def handle_movement(keys_pressed, rect):
    if keys_pressed[pygame.K_w] and rect.y > -50: # up
        rect.y -= VEL
def display_game_over():
    run = True
    while run:
        font = pygame.font.SysFont('Times New Roman', 50, True, False) 
        text = font.render("GAME OVER", True, (255, 87, 51)) # in line 48
        WIN.blit(text, (WIDTH/2 - 180, HEIGHT/2))    
        font = pygame.font.SysFont('Times New Roman', 25, True, False) 
        text = font.render("Press p to play again", True, (255, 87, 51)) # in line 48
        WIN.blit(text, (WIDTH/2 - 180, 2*HEIGHT/3))   
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    enemy
                    gameLoop()

def start_screen():
    run = True
    while run:
        font = pygame.font.SysFont('Times New Roman', 50, True, False) 
        text = font.render("Welcome, press P to start", True, (255, 87, 51)) # in line 48
        WIN.blit(text, (WIDTH/2 - 250, HEIGHT/2))    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gameLoop()


    
   


def gameLoop():
    rect = pygame.Rect(WIDTH / 3, HEIGHT / 3, BIRD_WIDTH, BIRD_HEIGHT)
    clock = pygame.time.Clock()
    bird_bullets = []
    enemy_list = []
    TESTENEMY = enemy(1, enemy_list)
    kill_count = 0
    scroll = 0
    light_list = []
     #GENERATE LIGHTS, WE UPDATE LIGHT_LISTS, and RETURN IMAGES FOR NEW LIGHTS.
    #Create a counter to track when to build more lights
    count = 0


    run = True
    while run:
        clock.tick(FPS)
        #GENERATE LIGHTS EVERY 3300 pixels
        if count % 3300 == 0:
            print("FUCK")
            light_list, images = create_lights(light_list)
        count -= SCROLL_VEL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(bird_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(rect.x + 10, rect.y + 20, BULLET_WIDTH, BULLET_HEIGHT)
                    bird_bullets.append(bullet)

            if event.type == ENEMY_HIT:
                for en in enemy_list:
                    en.health -= 1
                    if en.health == 0:
                        kill_count += 1
                    en.health = 1
                    en.rect.x = WIDTH + 200
                    en.rect.y = random.randint(80, 400)
            if event.type == PLAYER_DIE:
                run = False
                break
       

               
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, rect)
        
        handle_bullets(bird_bullets, enemy_list, light_list)
        drawWindow(rect, bird_bullets, kill_count, scroll, enemy_list, light_list, images)

        scroll -= SCROLL_VEL
        #RESET SCROLL WHEN WE SCROLLED TOO MUCH
        if abs(scroll) > (WIDTH - 100):
            scroll = 0
        physics(rect)
    display_game_over()
    pygame.quit()


if __name__ == "__main__":
    start_screen()