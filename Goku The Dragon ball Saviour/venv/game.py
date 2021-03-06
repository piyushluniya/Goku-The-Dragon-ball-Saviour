import pygame
import math
import random
from pygame.locals import *

#initialize the game
pygame.init() #initialize the game engine
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Goku The DragonBall Saviour")
pygame.mixer.init()

# Now we set up a timer so that the game adds a new badger after some time has elapsed, decrease the badtimer every
# frame until it is zero and then spawn a new badger(bad guy).
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194

acc = [0, 0] #keeps track of players accuracy(accuracy variable is essentially a list of the number of shots fired and the number of badgers hit)
arrows = []  #tracks all the arrows

#The keys array keeps track of the keys being pressed in the following order: WASD.
keys = [False, False, False, False]
#The playerpos variable is where the program draws the player. Since the game will move the player to different
# positions, it’s easier to have a variable that contains the player position and then simply draw the player at that position
playerpos = [100, 100]

#load image that will be used in the game
player = pygame.image.load("../resources/images/goku.png")
grass = pygame.image.load("../resources/images/grass.png")
castle = pygame.image.load("../resources/images/dragon ball.png")
arrow = pygame.image.load("../resources/images/kamehameha.png")
badguyimg1 = pygame.image.load("../resources/images/red beam.png")
badguyimg = badguyimg1 # copy of image so that we can animate bad guy much more easily
healthbar = pygame.image.load("../resources/images/healthbar.png")
health = pygame.image.load("../resources/images/health.png")
gameover = pygame.image.load("../resources/images/gameover.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("../resources/audio/explode.wav")
enemy = pygame.mixer.Sound("../resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("../resources/audio/shoot.wav")
hit.set_volume(2.05)
enemy.set_volume(1.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('../resources/audio/moonlight.wav') # background music for the game
pygame.mixer.music.play(-1, 0.0) # looping the background music forever
pygame.mixer.music.set_volume(0.25)


# The running variable keeps track of if the game is over and the exit code variable keeps track of whether the player won or lost.
running = 1
exitcode = 0
frame_count = 0
frame_rate = 60
GREEN = (0, 255, 0)

# keep looping through
while running:
    badtimer -= 1
    frame_count += 1
    #clear the screen before drawing it again i.e fill the screen with black before drawing anything
    screen.fill(0)
    #adding grass in the backgroung and adjusting it according to our games display dimensions
    #As you can see, the for statement loops through x first. Then, within that for loop, it loops through y and draws
    #the grass at the x and y values generated by the for loops.
    for x in range(int(width/grass.get_width())+1):
        for y in range(int(height/grass.get_height())+1):
            screen.blit(grass,(x*100, y*100))

    screen.blit(castle, (0,30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0,240))
    screen.blit(castle, (0,345))
    #add the blit(our bunny image before drawing anything) at the screen which you loaded at x=100, y=100
    # screen.blit(player, playerpos)

    # First you get the mouse and player positions. Then you feed those into the atan2 function. After that, you convert
    # the angle received from the atan2 function from radians to degrees
    position = pygame.mouse.get_pos() #getting moise position
    angle = math.atan2(position[1] - (playerpos[1]+32), position[0] - (playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360 - angle*57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width/2, playerpos[1] - playerrot.get_rect().height/2) #the bunny will be rotated, its position will change. So now you calculate the new bunny position and
    screen.blit(playerrot, playerpos1)  #display the bunny on screen

    # 6.2 - Draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10 #velocity in X- direction
        vely = math.sin(bullet[0]) * 10 #velocity in Y- direction
        bullet[1] += velx
        bullet[2] += vely
        #if statement just checks if the bullet is out of bounds and if it is, it deletes the arrow
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))



    #draw badgers
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0] < -64: #if badger is smaller than 64 then it disappears
            badguys.pop(index)
        badguy[0] -= 7  #this step controls the speed of badger with which it moves in -ve x direction


        # badguy Attack castle If the badger's x value is less than 64 to the right, then delete that bad guy and
        # decrease the game health value by a random value between 5 and 20.
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5, 20)
            badguys.pop(index)

        #6.3.2 - Check for collisions
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1

        # 6.3.3 - Next bad guy
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - Draw clock
    #  creates a new font using the default PyGame font set to size 24. Then that font is used to render the text of the
    #  time onto a surface. After that, the text is positioned and drawn onscreen.
    font = pygame.font.Font(None, 24)
    total_sec = frame_count // frame_rate
    minutes = total_sec // 60
    seconds = total_sec % 60
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

    # Blit to the screen
    text = font.render(output_string, True, GREEN)
    screen.blit(text, [550, 5])

    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5)) # drwaing a all red health bar
    for health1 in range(healthvalue): # drawing a green health bar according to how much health is remaining
        screen.blit(health, (health1+8,8))

    #update the screen
    pygame.display.flip()

    #loop through the events(i.e check for new events and if there is one, and if it is a qit command exit the program)
    for event in pygame.event.get():
        #check if event is in 'X' button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        # update the keys array based on which key is being pressed. we can do that by using even.key function
        # First you check to see if a key is being pressed down or released. Then you check which key is being pressed or
        # released, and if the key being pressed or released is one of the keys you’re using, you update the keys variable
        #  accordingly
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

        # This code checks if the mouse was clicked and if it was, it gets the mouse position and calculates the arrow
        # rotation based on the rotated player position and the cursor position. This rotation value is stored in the arrows array
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                           playerpos1[0] + 32,playerpos1[1] + 32]) #here +32 is done to define the position from where arrow shoot diplays


    # updating bunny's position based on key being pressed key 0,2 = vertical and key 1,3 = horizontal

    if ( keys[0] and playerpos[1]>45) :
        playerpos[1]-=5
    elif ( keys[2] and playerpos[1] <435):
        playerpos[1] += 5


    if ( keys[1] and playerpos[0] > 85):
        playerpos[0] -= 5
    elif ( keys[3] and playerpos[0] < 600):
        playerpos[0] += 5

    # 10 - Win/Lose check
    if healthvalue <= 0: #checks if health is destroyed
        running = 0
        exitcode = 0
    if acc[1] != 0: #calculates accuracy
        accuracy = acc[0] * 1.0 / acc[1] * 100 # acc[1] = number of arrows fired acc[0] = number of arrows on target
    else:
        accuracy = 0
# 11 - Win/lose display
pygame.font.init()
font = pygame.font.Font(None, 24)
text2 = font.render("Accuracy: " + str(accuracy) + "%", True, (0, 255, 0))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24

screen.blit(gameover, (0, 0))
screen.blit(text, textRect)
screen.blit(text2, [200, 280])
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()



