import pygame
import random
import math
from pygame import mixer
import vector


pygame.init()

scr = pygame.display.set_mode((1400, 750))
run = True
image = pygame.image.load("ball.png")
clock = pygame.time.Clock()
FPS = 200

# PLAYER
playerexploded = False
hitpoints = 100
playerimg = pygame.image.load("player.png")
playerx = 1200
playery = 560
movey = 0
movex = 0
playerspeed = 7
playerspeedsave = playerspeed
playerspeeddiag = playerspeed / 1.414
touch = False

# ENEMY
enemyimg = pygame.image.load("enemy.png")
enemyx = random.randint(1, 400)
enemyy = random.randint(1, 400)
enemyspeed = 8
enemymovey = enemyspeed
enemymovex = enemyspeed

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 0
bulletaimx = playerspeed * 4
bulletaimy = 0
bulletmovey = 0
bulletmovex = 0
bulletfired = "no"
collided = False

# enemy bullet
damage = 0
critim = 0
critim10 = 0
critx = 0
crity = 0
crit = False
canshoot = True
ebulletimg = pygame.image.load("bullet.png")
ebulletx = 0
ebullety = 0
ebulletaimx = 0
ebulletaimy = 0
ebulletmovey = 0
ebulletmovex = 0
ebulletfired = "no"
ecollided = False

pygame.display.set_caption("ballS 619")
pygame.display.set_icon(image)

# score
over = False
score = 0

# highscore
highscore = open("highscore.txt", "r")
hs = int(highscore.read())
highscore.close()

scoreimg = pygame.font.Font("freesansbold.ttf", 32)
critimg = pygame.font.Font("freesansbold.ttf", 15)
overimg = pygame.font.Font("freesansbold.ttf", 120)
oldhighimg = pygame.font.Font("freesansbold.ttf", 20)
newhighimg = pygame.font.Font("freesansbold.ttf", 50)

# blit

oldhigh = True


def healthbar(x, y):
    pygame.draw.rect(scr, (0, 0, 0), (x + 207, y - 1, 156, 36))
    pygame.draw.rect(scr, (250, 0, 0), (x + 210, y + 2, 150, 30))
    pygame.draw.rect(scr, (0, 250, 0), (x + 210, y + 2, hitpoints * 1.5, 30))


def high(x, y):
    highdis = oldhighimg.render("High score: " + str(hs), True, (0, 255, 0))
    scr.blit(highdis, (x, y))


def newhigh(x, y):
    newhighdis = newhighimg.render("NEW High score: " + str(score), True, (0, 255, 0))
    scr.blit(newhighdis, (x, y))


def criticalhit(x, y):
    hiit = critimg.render(str(damage), True, (200, 0, 0))
    scr.blit(hiit, (x, y))


topscoredis = True


def scoredis(x, y):
    scor = scoreimg.render("score: " + str(score) + "   HP:", True, (255, 255, 255))
    scr.blit(scor, (x, y))
    healthbar(x, y)


def gameover(x, y):
    gover = overimg.render("GAME OVER", True, (0, 255, 70))
    scr.blit(gover, (x, y))


def player(x, y):
    scr.blit(playerimg, (x, y))


def enemy(x, y):
    scr.blit(enemyimg, (x, y))


def bullet(x, y):
    global bulletfired
    bulletfired = "yes"
    scr.blit(bulletimg, (x, y))


def ebullet(x, y):
    global ebulletfired
    ebulletfired = "yes"
    scr.blit(ebulletimg, (x, y))


# Collision

def collision(bx, by, ex, ey, d):
    distance = math.dist((bx, by), (ex, ey))
    if distance < d:
        return True
    else:
        return False


# game loop
while run:
    clock.tick(30)

    scr.fill((15, 20, 10))

    for event in pygame.event.get():

        # player controls
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                movey = -playerspeed
            if event.key == pygame.K_s:
                movey = playerspeed
            if event.key == pygame.K_a:
                movex = -playerspeed
            if event.key == pygame.K_d:
                movex = playerspeed

            if movex != 0 and movey != 0:
                movex = (movex / playerspeed) * playerspeeddiag
                movey = (movey / playerspeed) * playerspeeddiag

            if bulletfired == "no":
                if event.key == pygame.K_SPACE:
                    bulletsound = mixer.Sound("laser.mp3")
                    bulletsound.play()
                    bulletmovex = bulletaimx
                    bulletmovey = bulletaimy
                    bulletx = playerx + 24
                    bullety = playery + 24
                    bullet(bulletx, bullety)
            if event.key != pygame.K_SPACE:
                bulletaimx = movex * 4
                bulletaimy = movey * 4

        if event.type == pygame.KEYUP:

            if movex != 0 and movey != 0:
                movex = (movex / playerspeeddiag) * playerspeed
                movey = (movey / playerspeeddiag) * playerspeed
            if event.key == pygame.K_w:
                if bulletaimx != 0:
                    bulletaimy = 0
                movey = 0
            if event.key == pygame.K_s:
                if bulletaimx != 0:
                    bulletaimy = 0
                movey = 0
            if event.key == pygame.K_a:
                if bulletaimy != 0:
                    bulletaimx = 0
                movex = 0
            if event.key == pygame.K_d:
                if bulletaimy != 0:
                    bulletaimx = 0
                movex = 0

        if event.type == pygame.QUIT:
            run = False

    # player movement
    if playerx < 0:
        playerx = 0
    if playerx > 1336:
        playerx = 1336
    if playery < 0:
        playery = 0
    if playery > 686:
        playery = 686

    # bullet movement
    if bulletx < 0:
        bulletfired = "no"
    if bulletx > 1400:
        bulletfired = "no"
    if bullety < 0:
        bulletfired = "no"
    if bullety > 750:
        bulletfired = "no"

    bulletx += bulletmovex
    bullety += bulletmovey

    if bulletfired == "yes":
        collided = collision(bulletx + 8, bullety + 8, enemyx + 32, enemyy + 32, 40)
        bullet(bulletx, bullety)

    # enemy bullet movement
    if canshoot:
        if ebulletfired == "no":
            bulletsound = mixer.Sound("laser.mp3")
            bulletsound.play()
            ev = vector.vec(enemyx, enemyy, playerx, playery, playerspeed*4)
            ebulletmovex = ev[0]
            ebulletmovey = ev[1]
            ebulletx = enemyx + 24
            ebullety = enemyy + 24
            ebullet(ebulletx, ebullety)

    if ebulletx < 0:
        ebulletfired = "no"
    if ebulletx > 1400:
        ebulletfired = "no"
    if ebullety < 0:
        ebulletfired = "no"
    if ebullety > 750:
        ebulletfired = "no"

    ebulletx += ebulletmovex
    ebullety += ebulletmovey

    if ebulletfired == "yes":
        ecollided = collision(ebulletx + 8, ebullety + 8, playerx + 32, playery + 32, 40)
        ebullet(ebulletx, ebullety)

    # enemy movement
    if enemyx < 0:
        enemymovex = -enemymovex
    if enemyx > 1336:
        enemymovex = -enemymovex
    if enemyy < 0:
        enemymovey = -enemymovey
    if enemyy > 686:
        enemymovey = -enemymovey

    enemyx += enemymovex
    enemyy += enemymovey
    enemy(enemyx, enemyy)

    playerx += movex
    playery += movey
    player(playerx, playery)

    # player collision
    touch = collision(playerx + 32, playery + 32, enemyx + 32, enemyy + 32, 64)

    if touch:
        explode = mixer.Sound("explosion.wav")
        explode.play()
        damage = random.randint(20, 50)
        hitpoints -= damage
        enemyx = random.randint(10, 200)
        enemyy = random.randint(10, 650)

    if hitpoints <= 0:
        over = True
        enemyx = 2000

    if ecollided:
        hit = mixer.Sound("hit2.mp3")
        hit.play()
        damage = random.randint(1, 10)
        hitpoints -= damage
        if 0 <= damage:
            critim = 0
            crit = True
            critx = playerx + 5
            crity = playery + 2
            criticalhit(critx, crity)
        ebulletfired = "no"
        ecollided = False

    if touch:
        critim = 0
        crit = True
        critx = playerx + 5
        crity = playery + 2
        criticalhit(critx, crity)

    if over:
        if hs < score:
            highscore = open("highscore.txt", "w")
            highscore.write(str(score))
            highscore.close()
            oldhigh = False
            newhigh(450, 500)

        if not playerexploded:
            explode = mixer.Sound("explosion.wav")
            explode.play()
            playerexploded = True
        canshoot = False
        topscoredis = False
        hitpoints = 0
        gameover(300, 300)
        scoredis(560, 430)

    if collided:
        explode = mixer.Sound("hit.mp3")
        explode.play()
        score += 1
        enemyx = random.randint(100, 1300)
        enemyy = random.randint(0, 100)
        bulletfired = "no"
        collided = False
    if oldhigh:
        high(10, 50)

    if topscoredis:
        scoredis(10, 10)

    if critim < 30:
        crity -= 1.5
        criticalhit(critx, crity)
        critim += 1

    pygame.display.update()