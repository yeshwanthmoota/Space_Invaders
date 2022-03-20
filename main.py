


import pygame
import sys, os, random
from SpaceShip import *
from constants import *

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()


gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

fileLocation = os.path.dirname(os.path.abspath(__file__)) # now inside directory 'Space_Invaders'
# print(fileLocation) # for debugging

with open(fileLocation + "/.debugging.txt", "w"):
    pass # to clear the debugging file
with open(fileLocation + "/.HighScore.txt", "a+") as file1: # To create HighScore.txt file if it didn't exist
    print(file1.read())
with open(fileLocation + "/.HighScore.txt", "r") as file1:
    if file1.read() == "":
        HIGH_SCORE = 0
    else:
        with open(fileLocation + "/.HighScore.txt", "r") as file2:
            HIGH_SCORE = int(file2.read())
        


# background image
HOMESHIP_IMG = pygame.image.load(fileLocation + "/Assets" + "/spaceship1.png")
HOMESHIP_IMG = pygame.transform.scale(HOMESHIP_IMG, (HOMESHIP_WIDTH, HOMESHIP_HEIGHT))
ENEMYSHIP_IMG = pygame.image.load(fileLocation + "/Assets" + "/spaceship2.png")
ENEMYSHIP_IMG = pygame.transform.rotate(pygame.transform.scale(ENEMYSHIP_IMG, (ENEMYSHIP_WIDTH, ENEMYSHIP_HEIGHT)), 180)
BACKGROUND_IMG = pygame.image.load(fileLocation + "/Assets" + "/spaceBackground.jpg").convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))


GAME_OVER = pygame.USEREVENT + 1 # GAME OVER

SCORE = 0



def draw_display(homeship, enemyShips, homeShipBullets, enemyShipBullets):
    gameDisplay.blit(BACKGROUND_IMG, (0, 0))
    gameDisplay.blit(HOMESHIP_IMG, (homeship.x, homeship.y))
    for ship in enemyShips:
        gameDisplay.blit(ENEMYSHIP_IMG, (ship.x, ship.y))
    for bullet in homeShipBullets:
        # pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        pygame.draw.circle(gameDisplay, random.choice(randomColorList), (bullet.x+HOMESHIP_BULLET_RADIUS/2, bullet.y+HOMESHIP_BULLET_RADIUS/2), HOMESHIP_BULLET_RADIUS)    
    for bullet in enemyShipBullets:
        # pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        pygame.draw.circle(gameDisplay, RED, (bullet.x+HOMESHIP_BULLET_RADIUS/2, bullet.y+HOMESHIP_BULLET_RADIUS/2), HOMESHIP_BULLET_RADIUS)
    pygame.display.update()







def check_for_and_post_events(homeship, enemyShips, homeShipBullets, enemyShipBullets):
    global SCORE
    condition1, bullets1 = homeship.is_homeship_hit(enemyShipBullets)
    condition2, ships1 = homeship.did_homeship_collide_enemyship(enemyShips)
    condition3, bullets2, hitEnemyShips = EnemyShip.is_enemyship_hit(enemyShips, homeShipBullets)

    if condition1 is True:
        for bullet in bullets1:
            enemyShipBullets.remove(bullet) # bullet disappears after hitting
        homeship.health -= ENEMY_SHIP_BULLET_DAMAGE * len(bullets1)
        if homeship.health <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))


    if condition2 is True:
        for ship in ships1:
            enemyShips.remove(ship) # ship disappears after collision
        homeship.health -= HOMESHIP_ENEMYSHIP_COLLISION_DAMAGE * len(ships1)
        if homeship.health <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))


    if condition3 is True:
        for bullet in bullets2:
            homeShipBullets.remove(bullet) # bullets disappears after hitting   
        for ship in hitEnemyShips:
            ship.health -= HOME_SHIP_BULLET_DAMAGE
            if ship.health <= 0:
                enemyShips.remove(ship)
                SCORE += SCORE_FOR_EACH






def main():
    running = True

    clock = pygame.time.Clock()

    homeship = HomeShip(HOMESHIP_INIT_X, HOMESHIP_INIT_Y) # homeship created
    enemyShips = []
    homeShipBullets = []
    enemyShipBullets = []

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
            if event.type == GAME_OVER:
                if SCORE > HIGH_SCORE:
                    print("Congratulations! You beat the High Score, Your Score is " + str(SCORE))
                    with open(fileLocation + "/.HighScore.txt", "w") as file1:
                        file1.write(str(SCORE))
                else:
                    print("Your Score: " + str(SCORE))
                    print("High Score: " + str(HIGH_SCORE))
                running = False
                pygame.quit()
                sys.exit(0)


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
        # print("homeship bullets----> " + str(len(homeShipBullets)) + " <----") # for debugging
        # print("enemyship bullets----> " + str(len(enemyShipBullets)) + " <----") # for debugging
        info_dict = {
            "homeshipHealth": homeship.health,
            "lengthOfEnemyShipList": len(enemyShips),
            "lengthOfEnemyShipBullets": len(enemyShipBullets),
            "lengthOfHomeShipBullets": len(homeShipBullets),
            "score": SCORE
        }
        with open(fileLocation+"/.debugging.txt", "a") as file1:
            file1.writelines(str(info_dict) + "\n\n\n")


    pygame.quit()

if __name__ == '__main__':
    main()