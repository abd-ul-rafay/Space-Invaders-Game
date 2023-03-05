import pygame
import random
import math
import time
from pygame import mixer
from pygame.locals import*

pygame.init()
pygame.mixer.init()

# Creating window
screen = pygame.display.set_mode((800 , 600))
pygame.display.set_caption("Matrix Invaders")
icon = pygame.image.load('assets\spaceship_32.png')
pygame.display.set_icon(icon)

# Loading background image
bgImg = pygame.image.load('assets/background.jpg')

# All levels music
easy_mode_music = 'assets/bg_music_easy.wav'
med_mode_music = 'assets/bg_music_med.wav'
diff_mode_music = 'assets/bg_music_hard.wav'

# Loading bullet music
bulletSound = mixer.Sound('assets/laser.wav')

# Rendering score and button fonts
font = pygame.font.Font('freesansbold.ttf', 24)
fontButton = pygame.font.SysFont('Arial Black', 16)
nameFont = pygame.font.SysFont('Arial Black', 30)

# Loading player and bullet image
playerImg = pygame.image.load('assets\spaceship_64.png')
bulletImg = pygame.image.load('assets/bullet.png')

# Global variables
isBulletFired = False
enemySpeed = 0.1 # It will be set according to difficulty mode
enemyWave = 0 # the many enemyWaves, the many ememies
howManyEnemyPerWave = 0 # It will be set according to difficulty mode

notExit = True

def player(x , y):
    screen.blit(playerImg, (x , y))

class Enemy:
    def __init__(self, xAxis, yAxis):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.image = pygame.image.load('assets\enemy.png')
        self.yChange = enemySpeed
    
    def move(self):
        self.yAxis += self.yChange
    
    def makeEnemy(self):
        screen.blit(self.image, (self.xAxis , self.yAxis))

def bullet(x , y):
    global isBulletFired
    isBulletFired = True

    bulletSound.play()

    # Adding 16 to make bullet at center of spaceship
    screen.blit(bulletImg, (x + 16 , y))

def distanceBw(x1 , y1 , x2 , y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2 , 2)))
    if distance < 27: # if the distance is less then 27 collision is done.
        return True
    else: return False

def showScore(score):
    scoreFont = font.render("Score: " + str(score), True, (235, 225, 215))
    screen.blit(scoreFont, (10, 20))

class Button():
    #button Color and size
    button_col = (0, 0, 0)
    hover_col  = (50, 50, 50)
    click_col  = (130, 10, 135)
    text_col   = (210, 210, 210)

    width = 150
    height = 50

    def __init__(self , x , y , text):
        self.x    = x
        self.y    = y
        self.text = text
        self.isButtonClicked = False

    def drawButton(self):
        action = False

        # to get mouse position
        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x , self.y , self.width , self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.isButtonClicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.isButtonClicked == True:
                self.isButtonClicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add text to Button
        text_img = fontButton.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img , (self.x + int(self.width/2) - int(text_len/2 ), self.y + 10))
        return action


# All buttons required
easy = Button(325 , 175 , 'Easy Mode')
medium = Button(325 , 250 , 'Medium Mode')
hard = Button(325 , 325 , 'Hard Mode')
quitGame = Button(325 , 400 , 'Quit Game')

def start():
    
    # Player spaceship properties
    playerxAxis = 370
    playeryAxis = 480
    playerXchange = 0 # this change will happen on pressing keys
    playerYchange = 0 # this change will happen on pressing keys

    # Bullet properties 
    bulletxAxis = 0
    bulletyAxis = playeryAxis # similar to ship y asix
    bulletYchange = 2.5 # speed of bullet
    global isBulletFired

    score = 0 # It will be updated as enemy killed
    
    enemies = [] # here we will store all upcoming enemies

    run = True
    while run:

        screen.fill((12 , 12 , 50)) 
        screen.blit(bgImg, (0, 0))

        showScore(score) # showing score at screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            playerXchange = -1.25
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            playerXchange = 1.25
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            playerYchange = -0.5
            bulletyAxis = playeryAxis
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            playerYchange = 0.5
            bulletyAxis = playeryAxis
        else:
            playerXchange = 0
            playerYchange = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_LCTRL]:
            if isBulletFired is False:
                bulletxAxis = playerxAxis # not to move along with spaceship
                bullet(bulletxAxis, bulletyAxis) 
        
        # Making player ship to move
        playerxAxis += playerXchange
        playeryAxis += playerYchange

        if playerxAxis <= 0:
            playerxAxis = 0
        elif playerxAxis >= 736:
            playerxAxis = 736
        
        if playeryAxis <= 0:
            playeryAxis = 0
        elif playeryAxis >= 536:
            playeryAxis = 536

        if bulletyAxis <= 0:
            isBulletFired = False
            bulletyAxis = 480

        global enemyWave
        global howManyEnemyPerWave

        if len(enemies) == 0:
            enemyWave += howManyEnemyPerWave
            for i in range(enemyWave):
                enemy = Enemy(random.randint(0, 736), random.randint(-250, 0))
                enemies.append(enemy)

        for i in enemies:
            
            if (i.yAxis >= 600):
                run = False

            if (distanceBw(playerxAxis, playeryAxis, i.xAxis, i.yAxis)): # If enemy hit player
                run = False

            i.makeEnemy()
            i.move()

            # Collision Detection
            iscollision = distanceBw(i.xAxis, i.yAxis, bulletxAxis, bulletyAxis)
            if iscollision:
                enemies.remove(i) 

                isBulletFired = False
                bulletyAxis = 480

                score += 1
                print(score)
        
        # Making bullet to move
        if isBulletFired:
            bulletyAxis -= bulletYchange
            bullet(bulletxAxis, bulletyAxis)

        # Rendering images
        player(playerxAxis , playeryAxis)
        
        pygame.display.update()
    
    mixer.music.load('assets/sad_sound.wav')
    mixer.music.play()

    youLoseFont = font.render("You Lose", True, (235, 225, 215))
    screen.blit(youLoseFont, (345, 260))

    scoreFont = font.render("Score: " + str(score), True, (235, 225, 215))
    screen.blit(scoreFont, (345, 285))

    pygame.display.update()
    time.sleep(3) # Hold for 3 seconds to show user "you lose"

def play():

    bg_music = mixer.music.load(easy_mode_music)
    mixer.music.play(-1)

    run = True
    while run:

        # screen.fill((12 , 12 , 50)) 
        screen.blit(bgImg, (0, 0))
        
        nameFontLoad = nameFont.render("Matrix Invaders", True, (235, 225, 215))
        screen.blit(nameFontLoad, (273, 75))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        global enemySpeed
        global enemyWave
        global howManyEnemyPerWave

        enemyWave = 0
        if easy.drawButton():
            mixer.music.load(easy_mode_music)
            mixer.music.play(-1)

            howManyEnemyPerWave = 2
            enemySpeed = 0.1
            start()

        elif medium.drawButton():
            mixer.music.load(med_mode_music)
            mixer.music.play(-1)

            howManyEnemyPerWave = 3
            enemySpeed = 0.2
            start()

        elif hard.drawButton():
            mixer.music.load(diff_mode_music)
            mixer.music.play(-1)

            howManyEnemyPerWave = 3
            enemySpeed = 0.25
            start()

        elif quitGame.drawButton():
            run = False
        
        pygame.display.update()

play() # Game will start from here
pygame.quit

