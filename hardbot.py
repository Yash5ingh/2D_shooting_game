import pygame
import random
import math
from pygame import mixer

play = True

while play:

    pygame.init()
    screenwidth = 1400
    screenheight = 750
    scr = pygame.display.set_mode((screenwidth, screenheight))
    run = True
    image = pygame.image.load("data/ball.png")
    clock = pygame.time.Clock()
    FPS = 60
    quitbutton = pygame.image.load("data/quitbutton.png").convert_alpha()
    restartbutton = pygame.image.load("data/restartbutton.png").convert_alpha()

    pygame.mouse.set_visible(False)

    cursor = pygame.image.load("data/crosshair.png").convert_alpha()

    # PLAYER
    playerexploded = False
    hitpoints = 100
    playerimg = pygame.image.load("data/player.png").convert_alpha()
    healthbox = pygame.image.load("data/healthbox.png").convert_alpha()
    healanimationposx = -200
    healanimationposy = -200
    heal = 0
    healanimation = 1000
    healthboxtimer = 0
    healpos = (-200, -200)
    healonscreen = False
    playerx = 1200
    playery = 560
    movey = 0
    movex = 0
    playerspeed = 5
    pmoveup = False
    pmovedown = False
    pmoveright = False
    pmoveleft = False
    playerspeedsave = playerspeed
    playerspeeddiag = playerspeed / 1.414
    touch = False

    # ENEMY
    enemyimg = pygame.image.load("data/enemy.png").convert_alpha()
    enemyx = random.randint(1, 400)
    enemyy = random.randint(1, 400)
    enemyspeed = 6
    enemymovey = enemyspeed
    enemymovex = enemyspeed

    # bullet
    bulletimg = pygame.image.load("data/bullet.png").convert_alpha()
    bulletx = 0
    bullety = 0
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
    ebulletimg = pygame.image.load("data/bullet.png").convert_alpha()
    ebulletx = 0
    ebullety = 0
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
    highscore = open("data/hardhigh.txt", "r")
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
        pygame.draw.rect(scr, (0, 0, 0), (x + 142, y - 3, 156, 36))
        pygame.draw.rect(scr, (250, 0, 0), (x + 145, y, 150, 30))
        pygame.draw.rect(scr, (0, 250, 0), (x + 145, y, hitpoints * 1.5, 30))


    def high(x, y):
        highdis = oldhighimg.render("High score: " + str(hs), True, (0, 255, 0))
        scr.blit(highdis, (x, y))


    def newhigh(x, y):
        newhighdis = newhighimg.render("NEW High score: " + str(score), True, (0, 255, 0))
        scr.blit(newhighdis, (x, y))


    def criticalhit(x, y):
        hiit = critimg.render(str(damage), True, (200, 0, 0))
        scr.blit(hiit, (x, y))


    def healing(x, y):
        heall = critimg.render(str(heal), True, (0, 200, 0))
        scr.blit(heall, (x, y))


    topscoredis = True


    def scoredis(x, y):
        scor = scoreimg.render("score: " + str(score), True, (255, 255, 255))
        scr.blit(scor, (x, y))
        healthbar(x + 30, y)


    def gameover(x, y):
        gover = overimg.render("GAME OVER", True, (0, 255, 70))
        scr.blit(gover, (x, y))


    def buttons(x, y):
        scr.blit(quitbutton, (x + 1100, y))
        scr.blit(restartbutton, (x, y))


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

    def vec(x, y, ex, ey, mag):
        i = ex - x
        j = ey - y
        m = math.sqrt((i * i) + (j * j))
        ic = i / m
        jc = j / m
        return ((ic * mag), (jc * mag))


    def collision(bx, by, ex, ey, d):
        distance = math.dist((bx, by), (ex, ey))
        if distance < d:
            return True
        else:
            return False


    # game loop
    while run:
        clock.tick(FPS)
        playerspeed = playerspeedsave

        scr.fill((7, 5, 20))

        healthboxtimer = random.randint(0, 1500)
        if not healonscreen and healthboxtimer == 11:
            healpos = (random.randint(0, screenwidth - 32), random.randint(150, screenheight - 32))
            scr.blit(healthbox, healpos)
            healonscreen = True

        scr.blit(healthbox, healpos)

        playerheal = collision(playerx + 32, playery + 32, healpos[0] + 16, healpos[1] + 16, 48)

        if playerheal:
            healsound = mixer.Sound("data/heal.wav")
            healsound.play()
            heal = random.randint(10, 25)
            hitpoints += heal
            healpos = (-200, -200)
            healanimation = 0
            healanimationposx = playerx + 10
            healanimationposy = playery + 10
            if hitpoints > 100:
                hitpoints = 100
            healonscreen = False

        for event in pygame.event.get():

            # player controls
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    pmoveup = True
                if event.key == pygame.K_s:
                    pmovedown = True
                if event.key == pygame.K_a:
                    pmoveleft = True
                if event.key == pygame.K_d:
                    pmoveright = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_w:
                    pmoveup = False
                if event.key == pygame.K_s:
                    pmovedown = False
                if event.key == pygame.K_a:
                    pmoveleft = False
                if event.key == pygame.K_d:
                    pmoveright = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bulletfired == "no":
                    pos = pygame.mouse.get_pos()
                    bulletsound = mixer.Sound("data/laser.mp3")
                    bulletsound.play()
                    aim = vec(playerx, playery, pos[0], pos[1], playerspeedsave * 4)
                    bulletmovex = aim[0]
                    bulletmovey = aim[1]
                    bulletx = playerx + 24
                    bullety = playery + 24
                    bullet(bulletx, bullety)

            if event.type == pygame.QUIT:
                run = False
                play = False

        # player movement

        if (pmoveup or pmovedown) and (pmoveleft or pmoveright):
            playerspeed = playerspeeddiag

        if pmoveup:
            movey = -playerspeed
        if pmovedown:
            movey = playerspeed
        if pmoveright:
            movex = playerspeed
        if pmoveleft:
            movex = -playerspeed

        if not pmoveup and not pmovedown:
            movey = 0
        if not pmoveright and not pmoveleft:
            movex = 0

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
                bulletsound = mixer.Sound("data/laser.mp3")
                bulletsound.play()
                ev = vec(enemyx, enemyy, (playerx + random.randint(-70, 70)), (playery + random.randint(-70, 70)),
                         playerspeedsave * 4)
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
            explode = mixer.Sound("data/explosion.wav")
            explode.play()
            damage = random.randint(20, 50)
            hitpoints -= damage
            enemyx = random.randint(10, 200)
            enemyy = random.randint(10, 650)

        if hitpoints <= 0:
            over = True
            enemyx = 2000

        if ecollided:
            hit = mixer.Sound("data/hit2.mp3")
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
                highscore = open("data/hardhigh.txt", "w")
                highscore.write(str(score))
                highscore.close()
                oldhigh = False
                newhigh(450, 500)

            if not playerexploded:
                explode = mixer.Sound("data/explosion.wav")
                explode.play()
                playerexploded = True
            canshoot = False
            topscoredis = False
            hitpoints = 0
            gameover(300, 300)
            scoredis(560, 430)
            buttons(100, 600)
            if collision(150, 650, bulletx + 8, bullety + 8, 60):
                reload = mixer.Sound("data/reload.wav")
                reload.play()
                run = False
            if collision(1250, 650, bulletx + 8, bullety + 8, 60):
                run = False
                play = False

        if collided:
            explode = mixer.Sound("data/hit.mp3")
            explode.play()
            score += 1
            bulletfired = "no"
            enemyx = random.randint(100, 1300)
            enemyy = random.randint(0, 100)
            collided = False
        if oldhigh:
            high(10, 50)

        if topscoredis:
            scoredis(10, 10)

        if critim < 30:
            crity -= 1.5
            criticalhit(critx, crity)
            critim += 1

        if healanimation < 50:
            healanimation += 1
            healanimationposy -= 2
            healing(healanimationposx, healanimationposy)

        # MOUSE
        cursorpos = pygame.mouse.get_pos()
        scr.blit(cursor, (cursorpos[0] + 16, cursorpos[1] + 16))

        pygame.display.update()
