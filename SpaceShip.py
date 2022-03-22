

import math
import pygame
import random
from constants import *


class HomeShip:

    # constructor class
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y
        self.health = 100
    

    def movement(self, keys_pressed):

        # up and down
        if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and self.y > 0 + PADDING_Y:
            self.y -= HOMESHIP_SPEED_Y
        elif (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) and self.y < HEIGHT - HOMESHIP_HEIGHT - PADDING_Y:
            self.y += HOMESHIP_SPEED_Y
        
        # left right
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and self.x > 0 + PADDING_X:
            self.x -= HOMESHIP_SPEED_X
        elif (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and self.x < WIDTH - HOMESHIP_WIDTH - PADDING_X:
            self.x += HOMESHIP_SPEED_X


    def bullet_spawn(self):
        bullet_x_spawn = self.x + HOMESHIP_WIDTH/2
        bullet_y_spawn = self.y - 10
        bullet = Bullets(bullet_x_spawn, bullet_y_spawn)
        return bullet
    
    @staticmethod
    def bullet_movement(bullets):
        for bullet in bullets:
            bullet.y -= HOMESHIP_BULLET_SPEED
    
    def is_homeship_hit(self, enemyShipBullets): # reduces health and checks if game over
        homeship = pygame.Rect(self.x, self.y, HOMESHIP_WIDTH, HOMESHIP_HEIGHT)
        hitBullets = []
        isHit = False
        for bullet in enemyShipBullets:
            bulletRect = pygame.Rect(bullet.x, bullet.y, ENEMYSHIP_BULLET_RADIUS*2, ENEMYSHIP_BULLET_RADIUS*2)
            if homeship.colliderect(bulletRect):
                hitBullets.append(bullet)
                isHit = True
        if isHit:
            return True, hitBullets
        else:
            return False, None
            

    def did_homeship_collide_enemyship(self, enemyShips): # reduces health and checks if game over
        homeship = pygame.Rect(self.x, self.y, HOMESHIP_WIDTH, HOMESHIP_HEIGHT)
        hitShips = []
        isHit = False
        for ship in enemyShips:
            shipRect = pygame.Rect(ship.x, ship.y, ENEMYSHIP_WIDTH, ENEMYSHIP_HEIGHT)
            if homeship.colliderect(shipRect):
                hitShips.append(ship)
                isHit = True
        if isHit:
            return True, hitShips
        else:
            return False, None
    
class Bullets:

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    @staticmethod
    def bullets_remove(bullets, HomeShip=True):
        if HomeShip == True:
            for bullet in bullets:
                if bullet.y + HOMESHIP_BULLET_RADIUS*2 < 0:
                    bullets.remove(bullet)
                elif bullet.y > HEIGHT:
                    bullets.remove(bullet)
            return bullets
        else:
            for bullet in bullets:
                if bullet.y + ENEMYSHIP_BULLET_RADIUS*2 < 0:
                    bullets.remove(bullet)
                elif bullet.y > HEIGHT:
                    bullets.remove(bullet)
            return bullets


class EnemyShip:

    def __init__(self, ships):
        self.y = 0 - ENEMYSHIP_HEIGHT# fixed
        self.health = 100
        x = 0
        # Spawned at a random location but doesn't collide with locations of previous enemy ships
        while(True):
            x = math.floor(random.random() * WIDTH)
            repeat = False
            for ship in ships:
                if ((x > ship.x) and (x < (ship.x + ENEMYSHIP_WIDTH))) or ((x+ENEMYSHIP_WIDTH > ship.x) and (x+ENEMYSHIP_WIDTH < (ship.x + ENEMYSHIP_WIDTH))): # if it is not in range of an enemy ship
                    if (self.y + ENEMYSHIP_HEIGHT >= ship.y):
                        repeat = True
                        break 
                if (x < (0 + ENEMYSHIP_WIDTH + PADDING_X*2)) or (x > (WIDTH - ENEMYSHIP_WIDTH - PADDING_X*2)):
                    repeat = True
                    break
            if not repeat:
                break
        self.x = x
        

    @staticmethod
    def movement(ships):
        to_remove_ships = []
        for ship in ships:
            if ship.y >= HEIGHT:
                to_remove_ships.append(ship)
            else:
                ship.y += ENEMYSHIP_SPEED_Y
        for ship in to_remove_ships:
            ships.remove(ship) # removing ships that crossed bounds

    def bullet_spawn(self):
        choiceList = [0] * (BULLET_SPAWN_PROBABILITY - 1) # bullet chance of spawn -> 1 in 5 frames
        choiceList.append(1)
        choice = random.choice(choiceList)
        if choice == 1:
            bullet_x_spawn = self.x + ENEMYSHIP_WIDTH / 2
            bullet_y_spawn = self.y + ENEMYSHIP_HEIGHT
            bullet = Bullets(bullet_x_spawn, bullet_y_spawn)
            return bullet
        else:
            return None

    @staticmethod
    def bullet_movement(bullets):
        for bullet in bullets:
            bullet.y += ENEMYSHIP_BULLET_SPEED

    @staticmethod
    def is_enemyship_hit(enemyShips, homeShipBullets):
        isHit = False
        hitBullets = []
        hitShips = []
        for ship in enemyShips:
            shipRect = pygame.Rect(ship.x, ship.y, ENEMYSHIP_WIDTH, ENEMYSHIP_HEIGHT)
            for bullet in homeShipBullets:
                bulletRect = pygame.Rect(bullet.x, bullet.y, ENEMYSHIP_BULLET_RADIUS*2, ENEMYSHIP_BULLET_RADIUS*2)
                if shipRect.colliderect(bulletRect):
                    isHit = True
                    hitBullets.append(bullet)
                    hitShips.append(ship)
        if isHit:
            return True, hitBullets, hitShips
        else:
            return False, None, None

def blit_text(gameDisplay, text, pos, font, color=pygame.Color('black')): # function borrowed from stack overflow 😅
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = gameDisplay.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            gameDisplay.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.