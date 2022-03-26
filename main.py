


import pygame
import sys, os, random
from SpaceShip import *
from constants import *

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()


gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

fileLocation = os.path.dirname(os.path.abspath(__file__)) # now inside directory 'Space_Invaders'
# print(fileLocation) # for debugging
# print(os.path.join(fileLocation, ".debugging.txt"))
# print(os.path.join(fileLocation, ".HighScore.txt"))
# print(os.path.join(fileLocation, "Assets", "images", "spaceship1.png"))
        


# Image Rendering
HOMESHIP_IMG = pygame.image.load(os.path.join(fileLocation, "Assets", "images", "spaceship1.png"))
HOMESHIP_IMG = pygame.transform.scale(HOMESHIP_IMG, (HOMESHIP_WIDTH, HOMESHIP_HEIGHT))
ENEMYSHIP_IMG = pygame.image.load(os.path.join(fileLocation, "Assets", "images", "spaceship2.png"))
ENEMYSHIP_IMG = pygame.transform.rotate(pygame.transform.scale(ENEMYSHIP_IMG, (ENEMYSHIP_WIDTH, ENEMYSHIP_HEIGHT)), 180)
BACKGROUND_IMG = pygame.image.load(os.path.join(fileLocation, "Assets", "images", "spaceBackground.jpg")).convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Sounds

channel1 = pygame.mixer.Channel(0) # Background music channel
channel2 = pygame.mixer.Channel(1) # buller sound
channel3 = pygame.mixer.Channel(2)

BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "background_music.ogg"))
BACKGROUND_MUSIC.set_volume(0.7)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "bullet_fire_sound.ogg"))
BULLET_FIRE_SOUND.set_volume(1)
BULLET_HIT_IMPACT = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "bullet_hit_impact.ogg"))
BULLET_HIT_IMPACT.set_volume(1)
ENEMYSHIP_HIT_SOUND = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "enemyship_hit.ogg"))
ENEMYSHIP_HIT_SOUND.set_volume(1)
CRASH_SOUND = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "crash.wav"))
CRASH_SOUND.set_volume(1)
GAME_OVER_MUSIC = pygame.mixer.Sound(os.path.join(fileLocation, "Assets", "sounds", "cheering.wav"))
GAME_OVER_MUSIC.set_volume(0.7)


# Custom Events
GAME_OVER = pygame.USEREVENT + 1 # GAME OVER

FONT = pygame.font.SysFont("consolas", 30)
WINNER_FONT = pygame.font.SysFont("consolas", 15)
WELCOME_FONT = pygame.font.SysFont('Consolas', 28)


def draw_display(homeship, enemyShips, homeShipBullets, enemyShipBullets):
    gameDisplay.blit(BACKGROUND_IMG, (0, 0))
    health_text = FONT.render("HOMESHIP HEALTH: {}".format(homeship.health), 1, WHITE)
    score_text = FONT.render("YOUR SCORE: {}".format(str(SCORE)), 1, WHITE)
    gameDisplay.blit(HOMESHIP_IMG, (homeship.x, homeship.y))
    gameDisplay.blit(health_text,(WIDTH/2 -health_text.get_width()/2,HEIGHT/2))
    gameDisplay.blit(score_text, ((WIDTH/2 -score_text.get_width()/2,(HEIGHT/2)+30)))
    for ship in enemyShips:
        gameDisplay.blit(ENEMYSHIP_IMG, (ship.x, ship.y))
    for bullet in homeShipBullets:
        # pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        pygame.draw.circle(gameDisplay, random.choice(randomColorList), (bullet.x+HOMESHIP_BULLET_RADIUS/2, bullet.y+HOMESHIP_BULLET_RADIUS/2), HOMESHIP_BULLET_RADIUS)    
    for bullet in enemyShipBullets:
        # pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        pygame.draw.circle(gameDisplay, RED, (bullet.x+HOMESHIP_BULLET_RADIUS/2, bullet.y+HOMESHIP_BULLET_RADIUS/2), HOMESHIP_BULLET_RADIUS)
    pygame.display.update()


def draw_end(winner_text, code):
    gameDisplay.fill(BLACK)
    if code == 2:
        draw_text = FONT.render(winner_text,1, WHITE)
    elif code == 1:
        draw_text = WINNER_FONT.render(winner_text,1, WHITE)
    gameDisplay.blit(draw_text,(WIDTH/2-(draw_text.get_width())/2, HEIGHT/2-(draw_text.get_height())/2))
    pygame.display.update()
    pygame.time.delay(1000*3) # 3 seconds




def check_for_and_post_events(homeship, enemyShips, homeShipBullets, enemyShipBullets):
    global SCORE
    condition1, bullets1 = homeship.is_homeship_hit(enemyShipBullets)
    condition2, ships1 = homeship.did_homeship_collide_enemyship(enemyShips)
    condition3, bullets2, hitEnemyShips = EnemyShip.is_enemyship_hit(enemyShips, homeShipBullets)

    if condition1 is True:
        channel3.play(BULLET_HIT_IMPACT)
        for bullet in bullets1:
            enemyShipBullets.remove(bullet) # bullet disappears after hitting
        homeship.health -= ENEMY_SHIP_BULLET_DAMAGE * len(bullets1)
        if homeship.health <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))


    if condition2 is True:
        channel3.play(CRASH_SOUND)
        for ship in ships1:
            enemyShips.remove(ship) # ship disappears after collision
        homeship.health -= HOMESHIP_ENEMYSHIP_COLLISION_DAMAGE * len(ships1)
        if homeship.health <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))


    if condition3 is True:
        channel3.play(ENEMYSHIP_HIT_SOUND)
        for bullet in bullets2:
            homeShipBullets.remove(bullet) # bullets disappears after hitting   
        for ship in hitEnemyShips:
            ship.health -= HOME_SHIP_BULLET_DAMAGE
            if ship.health <= 0:
                enemyShips.remove(ship)
                SCORE += SCORE_FOR_EACH

def ask_restart():
    end_text = "\n\n\n\n\n\n\n\n\nRestart The Game Press SpaceBar\nEnter Any Other Key To Quit.\n"
    while True:
        gameDisplay.fill(BLACK)
        gameDisplay.blit(BACKGROUND_IMG, (0, 0))
        blit_text(gameDisplay, end_text, (20, 20), FONT, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                else:
                    pygame.quit()
                    sys.exit(0)




def main():

    channel1.play(BACKGROUND_MUSIC, -1)
    running = True

    clock = pygame.time.Clock()

    homeship = HomeShip(HOMESHIP_INIT_X, HOMESHIP_INIT_Y) # homeship created
    enemyShips = []
    homeShipBullets = []
    enemyShipBullets = []
    InitialAnimation = INITIAL_ANIMATION
    global MAX_ENEMYSHIPS_ONSCREEN
    global INCDIFF
    global SCORE
    global HIGH_SCORE
    SCORE = 0
    INCDIFF = False
    CHECK_Y = True


    with open(os.path.join(fileLocation, ".debugging.txt"), "w"):
        pass # to clear the debugging file
    #################################################################
    with open(os.path.join(fileLocation, ".HighScore.txt"), "a+") as file1: # To create HighScore.txt file if it didn't exist
        print(file1.read())
    with open(os.path.join(fileLocation, ".HighScore.txt"), "r") as file1:
        if file1.read() == "":
            HIGH_SCORE = 0
        else:
            with open(os.path.join(fileLocation, ".HighScore.txt"), "r") as file2:
                HIGH_SCORE = int(file2.read())



    while CHECK_Y:
            gameDisplay.fill(BLACK)
            keys_pressed = pygame.key.get_pressed()
            text =  "\n\n\n\n\nWelcome To Space Invaders\n\n\n\n\n"\
                    "Controls:\n"\
                    "Go Up-> (UP, w)\n"\
                    "Go Down> (DOWN, s)\n"\
                    "Go Left-> (LEFT, a)\n"\
                    "Go Right-> (RIGHT, d)\n"\
                    "Shoot-> (LeftMouseClick, Spacebar)\n\n\n"\
                    "Start the Game:\n\n"\
                    "Enter 'Y' to increase difficulty and Start, Any other Key to Start by Not increasing difficulty"
            blit_text(gameDisplay, text, (20, 20), WELCOME_FONT, GREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                
                    # if keydown event happened
                    # than printing a string to output
                    if event.key == pygame.K_y:
                        INCDIFF = True
                        #################################################################
                        with open(os.path.join(fileLocation, ".HighScoreDiff.txt"), "a+") as file1: # To create HighScoreDiff.txt file if it didn't exist for recording difficult mode scores
                            print(file1.read())
                        with open(os.path.join(fileLocation, ".HighScoreDiff.txt"), "r") as file1:
                            if file1.read() == "":
                                HIGH_SCORE = 0
                            else:
                                with open(os.path.join(fileLocation, ".HighScoreDiff.txt"), "r") as file2:
                                    HIGH_SCORE = int(file2.read())
                        #################################################################
                        CHECK_Y = False
                    else:
                        CHECK_Y = False
            pygame.display.update()

    while InitialAnimation: # The Home Ship comes from the bottom of the Screen into the View
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # QUIT
                running = False
                pygame.quit()
                sys.exit(0)
                

        if (homeship.y + HOMESHIP_HEIGHT/2) <= HEIGHT * 0.75:
            InitialAnimation = False
            break
        else:
            homeship.y -= HOMESHIP_SPEED_Y * 0.5
            gameDisplay.blit(BACKGROUND_IMG, (0, 0))
            gameDisplay.blit(HOMESHIP_IMG, (homeship.x, homeship.y))
            pygame.display.update()



    while running:

        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # QUIT
                running = False
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN: # home ship shoots if left-mouse-click is detected
                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    homeShipBullets.append(homeship.bullet_spawn())
                    channel2.play(BULLET_FIRE_SOUND)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    homeShipBullets.append(homeship.bullet_spawn())
                    channel2.play(BULLET_FIRE_SOUND)
            if event.type == GAME_OVER:
                code = 0
                channel1.play(GAME_OVER_MUSIC)
                if SCORE > HIGH_SCORE:
                    text = "Congratulations! You beat the High Score, Your Score is " + str(SCORE)
                    code = 1
                    print(text)
                    if INCDIFF:
                        with open(os.path.join(fileLocation, ".HighScoreDiff.txt"), "w") as file1:
                            file1.write(str(SCORE))
                    else:
                        with open(os.path.join(fileLocation, ".HighScore.txt"), "w") as file1:
                            file1.write(str(SCORE))
                else:
                    text = "Your Score: " + str(SCORE) + ", High Score: " + str(HIGH_SCORE)
                    code = 2
                    print(text)
                running = False
                draw_end(text, code)
                ask_restart()

        if INCDIFF:
            if SCORE%50 == 0 and SCORE >= 200: # Code for inc difficulty every 5 ships destroyed
                MAX_ENEMYSHIPS_ONSCREEN = SCORE/50
        if len(enemyShips) < MAX_ENEMYSHIPS_ONSCREEN: # spawn new enemy ship if possible
            newShip = EnemyShip(enemyShips)
            enemyShips.append(newShip)

        for ship in enemyShips: # enemy ship shoots bullets if possible
            newEnemyBullet = ship.bullet_spawn()
            if newEnemyBullet:
                enemyShipBullets.append(newEnemyBullet)

        EnemyShip.movement(enemyShips) # enemy ship moves forward
        EnemyShip.bullet_movement(enemyShipBullets) # enemy ship bullets move forward
        enemyShipBullets = Bullets.bullets_remove(bullets=enemyShipBullets, HomeShip=False) # useless enemy ship bullets get destroyed

        homeship.movement(keys_pressed) # home ship movement
        HomeShip.bullet_movement(bullets=homeShipBullets) # home ship bullets move forward
        homeShipBullets = Bullets.bullets_remove(bullets=homeShipBullets, HomeShip=True) # useless home ship bullets get destroyed


        draw_display(homeship, enemyShips, homeShipBullets, enemyShipBullets) # draw display on screen
        check_for_and_post_events(homeship, enemyShips, homeShipBullets, enemyShipBullets) # check for all the events
        info_dict = {
            "homeshipHealth": homeship.health,
            "lengthOfEnemyShipList": len(enemyShips),
            "lengthOfEnemyShipBullets": len(enemyShipBullets),
            "lengthOfHomeShipBullets": len(homeShipBullets),
            "score": SCORE
        }
        with open(os.path.join(fileLocation, ".debugging.txt"), "a") as file1:
            file1.writelines(str(info_dict) + "\n\n\n")


    pygame.quit()

if __name__ == '__main__':
    main()