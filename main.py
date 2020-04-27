import random
import pygame
import time
from enum import Enum

#----------------------------------M A I N------------------------------------

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))

FPS = 30
mainloop = False

gm = pygame.image.load("game-over.png")
pl = pygame.image.load('laptop.png')

smallfont = pygame.font.SysFont("comicsansms", 20)
mediumfont = pygame.font.SysFont("comicsansms", 40)
bigfont = pygame.font.SysFont('laomn', 70)

clock = pygame.time.Clock()
pressed = pygame.key.get_pressed() 

pygame.display.set_caption("Tanks War")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

gamemusic = pygame.mixer.Sound('gamemusic.wav')
sound1 = pygame.mixer.Sound('shoot1.wav')
sound2 = pygame.mixer.Sound('shoot2.wav')
gameover = pygame.mixer.Sound('gameover.wav')

gamemusic.play(-1)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

#----------------------------------T A N K---------------------------------

class Tank:

    def __init__(self, x, y, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.bulcnt = 0
        self.speed = 5
        self.color = color
        self.width = 40
        #self.life = 3
        self.life = 3
        self.images = [pygame.image.load('life_1.png'), pygame.image.load('life_2.png'), pygame.image.load('life_3.png')]
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}


    def draw(self):
        tank_c = (self.x + 20, self.y + 20)
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 10)
        pygame.draw.circle(screen, self.color, tank_c, 20 - 7)

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + 17, self.y + 20), 7)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - 17, self.y + 20), 7)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + 20, self.y - 17), 7)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + 20, self.y + self.width + 17), 7)


    def change_direction(self, direction):
        self.direction = direction


    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        self.draw()


    def borders(self):
        if self.x > width or self.x < -30:
            self.x = (self.x + width) % width
        if self.y > height or self.y < -30:
            self.y = (self.y + height) % height
    

    def game_over(self):
        global mainloop
        global run
        if self.life == 0:
            gameover.play()
            screen.fill((195, 155, 255))
            # res = bigfont.render('G a m e   O v e r', True, (0, 90, 255))
            # screen.blit(res, (120, 150))
            if run == 0:
                screen.blit(gm, (135,50))
            pygame.display.flip()
            time.sleep(3)
            mainloop = False
            run = True
            intro()
            self.life = 3
            self.x = random.randint(100,700)
            self.y = random.randint(100,500)
            
#------------------------------------B U L L E T---------------------------------

class Bullet:
    def __init__(self, x, y, dy, dx, d_space = pygame.K_SPACE):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bul = False
        self.speed = 12


    def draw(self):
        pygame.draw.rect(screen, (30, 70, 30), (self.x, self.y, 10, 7))


    def move(self):
        if self.bul:
            self.x += self.dx
            self.y += self.dy
        self.draw()


    def borders(self):
        if self.x < -30 or self.x > width or self.y < -30 or self.y > height:
            self.bul = False
    

    def shooting(self, Tank):
        if Tank.direction == Direction.RIGHT:
            self.x = Tank.x + 50
            self.y = Tank.y + 18
            self.dx = self.speed
            self.dy = 0 

        if Tank.direction == Direction.LEFT:
            self.x = Tank.x - 15
            self.y = Tank.y + 15
            self.dx = -self.speed
            self.dy = 0 

        if Tank.direction == Direction.UP:
            self.x = Tank.x + 15
            self.y = Tank.y - 20
            self.dx = 0
            self.dy = -self.speed

        if Tank.direction == Direction.DOWN:
            self.x = Tank.x + 15
            self.y = Tank.y + 50
            self.dx = 0
            self.dy = self.speed

#--------------show life scores------------------------------------------

def lifes (x, y, Tank, n, tx, ty):
    if Tank.life == 3:
        screen.blit(Tank.images[2], (x, y))
    if Tank.life == 2:
        screen.blit(Tank.images[1], (x, y))
    if Tank.life == 1:
        screen.blit(Tank.images[0], (x, y))
    res = smallfont.render('PLAYER ' + str(n), True, (110, 30, 40))
    screen.blit(res, (tx, ty))


#---------------collission tank with opponent's bullet--------------------

def collision(tank, bullet):
    if bullet.x in range(tank.x, tank.x + 50) and bullet.y in range(tank.y, tank.y + 50):
        sound2.play()
        bullet.bul = False
        bullet.x = -100
        bullet.y = -100
        return True
    return False


tank1 = Tank(300, 300,  (146,21,37))
tank2 = Tank(100, 100,  (59,40,96), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]

bullet1 = Bullet(-100, -100, 0, 0)
bullet2 = Bullet(-100, -100, 0, 0, pygame.K_RETURN)
bullets = [bullet1, bullet2]

run = True
tap = False

 
#-----------------------------------M E N U----------------------------------

def intro():
    global tap
    global run
    global mainloop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            screen.fill((168, 143, 200))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            #------------------------S T A R T button----------------------

            if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
                pygame.draw.rect(screen, (170,25,30),(150,450,100,50))
                if click[0] == 1: #and action != None:
                    mainloop = True
                    run = False
            else:
                pygame.draw.rect(screen, (110, 30, 40),(150,450,100,50))

            #----------------------E X I T button--------------------------

            if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:
                pygame.draw.rect(screen, (170, 29, 34), (550,450,100,50))
                if click[0] == 1: #and action != None:
                    mainloop = False
                    run = False
            else:
                pygame.draw.rect(screen, (110, 30, 40), (550,450,100,50))
            
            #---------------------Choose level button--------------------

            if 300 + 190 > mouse[0] > 300 and 170 + 50 > mouse[1] > 170:
                pygame.draw.rect(screen, ((27, 49, 255)), (300, 170, 190, 50))
                
            else:
                pygame.draw.rect(screen, ((27, 49, 150)), (300, 170, 190, 50))

                
            #---------------------E A S Y level--------------------------

            if 100 + 100 > mouse[0] > 100 and 270 + 50 > mouse[1] > 270:
                pygame.draw.rect(screen, (51,178,231), (100, 270, 100, 50))
                if click[0] == 1: #and action != None:
                    tank1.speed = 2
                    tank2.speed = 2
                    bullet1.speed = 7
                    bullet2.speed = 7
                    mainloop = True
                    run = False
            else:
                pygame.draw.rect(screen, (117,217,242), (100, 270, 100, 50))

            easy = smallfont.render('Easy', True, (59,40,96))
            screen.blit(easy, (125, 275))

            #---------------------M E D I U M level----------------------

            if 350 + 100 > mouse[0] > 350 and 270 + 50 > mouse[1] > 270:
                pygame.draw.rect(screen, (29, 110, 34), (350, 270, 100, 50))
                if click[0] == 1: #and action != None:
                    tank1.speed = 5
                    tank2.speed = 5
                    bullet1.speed = 13
                    bullet2.speed = 13
                    mainloop = True
                    run = False
            else:
                pygame.draw.rect(screen, (29, 170, 34), (350, 270, 100, 50))

            med = smallfont.render('Medium', True, (255,226,0))
            screen.blit(med, (365, 275))

            #--------------------H A R D level-------------------------------

            if 600 + 100 > mouse[0] > 600 and 270 + 50 > mouse[1] > 270:
                pygame.draw.rect(screen, (200,75,109), (600, 270, 100, 50)) 
                if click[0] == 1: #and action != None:
                    tank1.speed = 10
                    tank2.speed = 10
                    bullet1.speed = 25
                    bullet2.speed = 25
                    mainloop = True
                    run = False
            else:
                pygame.draw.rect(screen, (235,126,145), (600, 270, 100, 50))

            hard = smallfont.render('Hard', True, (33,64,95))
            screen.blit(hard, (625, 275))
            
        #-----------------NAME of the buttons------------------------------

        stngs = smallfont.render('Tap to change level', True, (255,255,255))
        screen.blit(stngs, (305, 177))

        go = smallfont.render('START', True, (255, 255, 255))
        screen.blit(go, (167, 457))

        ex = smallfont.render('EXIT', True, (255, 255, 255))
        screen.blit(ex, (575, 457))

        screen.blit(pl, (320,400))
        hi = bigfont.render('Welcome to Tank game!', True, (110, 30, 40))
        screen.blit(hi, (20, 50))
        
        pygame.display.flip()
        # clock.tick(5)


intro() # menu



#--------------------------------M A I N   L O O P--------------------------------


while mainloop:
    
    millis = clock.tick(FPS)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mainloop = False

        if event.type == pygame.KEYDOWN:

            if event.key in tank1.KEY.keys():
                tank1.change_direction(tank1.KEY[event.key])

            if event.key in tank2.KEY.keys():
                tank2.change_direction(tank2.KEY[event.key])


            if event.key == pygame.K_SPACE and bullet1.bul == False:
                    bullet1.bul = True
                    sound1.play()
                    bullet1.shooting(tank1)


            if event.key == pygame.K_RETURN and bullet2.bul == False:
                    bullet2.bul = True
                    sound1.play()
                    bullet2.shooting(tank2)


            if event.key == pygame.K_ESCAPE:  
                mainloop = False


    screen.fill((100,165,187))
    tank1.move()
    tank2.move()

    if collision(tank1, bullet2):
        tank1.life -=1

    if collision(tank2, bullet1):
        tank2.life -=1

    for tank in tanks:

        if tank.game_over():
            tank.life = 3

        tank.borders()
        lifes(15, 35, tank1, 1, 15, 5)
        lifes(width - 100, 35, tank2, 2, width - 100, 5)
        
    bullet1.move()
    bullet2.move()

    bullet1.borders()
    bullet2.borders()

    pygame.display.flip()
pygame.quit()