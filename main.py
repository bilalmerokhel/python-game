######################
#  Important modules #
#####################

import turtle
import os
import math
import random

#Set the screen
window = turtle.Screen()
window.bgcolor("black")
window.title("Space Invaders")
window.bgpic("bg.gif")

#Register shapes images must be in gif formate
turtle.register_shape("alien.gif")
turtle.register_shape("air.gif")
turtle.register_shape("bullet.gif")

#Game border
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.setposition(-300,-300)
border.pendown()

#Default score set to 0
score = 0

#Drawing score
scorepen = turtle.Turtle()
scorepen.speed(0)
scorepen.color("white")
scorepen.penup()
scorepen.setposition(-290,280)
scorestore = "Score: %s" %score
scorepen.write(scorestore, False, align="Left", font=("Arial,",14,"normal"))
scorepen.hideturtle()


#Creating the player
player = turtle.Turtle()
player.color("blue")
player.shape("air.gif")
player.penup()
player.speed(50)
player.setposition(0, -250)
player.setheading(90)
playerspeed = 15

#Aliens list
number_of_aliens = 5
aliens = []

#Add aliens to list
for i in range(number_of_aliens):
    # Creating Aliens
    aliens.append(turtle.Turtle())

for alien in aliens:
    alien.color("red")
    alien.shape("alien.gif")
    alien.penup()
    alien.speed(0)
    alien.shapesize(2,4)
    xpos = random.randint(-200,200)
    ypos = random.randint(100,250)
    alien.setposition(xpos, ypos)

alienspeed = 5

#Create weapon
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bulletspeed = 20
bulletstate = "ready"

#Function to move player to left
def moveLeft():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

#Function to move player to right
def moveRight():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def firebullet():
    #Firing a bullet
    global bulletstate
    if bulletstate == "ready":
        if os.name == "nt":
            os.system("aplay fire.wav&")
        else:
            os.system("afplay fire.wav&")
        bulletstate = "fire"

        #Bullet position
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y +10)
        bullet.showturtle()

#Functions fo cheking for the collision between player and aliens and between aliens and bullet
def isShooted(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 20:
        return True
    else:
        return False

#Keyboard key events
turtle.listen()
turtle.onkey(moveLeft, "Left")
turtle.onkey(moveRight, "Right")
turtle.onkey(firebullet, "space")

#Main game loop
while True:

    for alien in aliens:
        #Move the aliens
        x = alien.xcor()
        x += alienspeed
        alien.setx(x)

        #Move the aliens back and down
        if alien.xcor() > 280:
            for a in aliens:
                y = a.ycor()
                y -= 40
                a.sety(y)
            alienspeed *= -1

        if alien.xcor() < -280:
            for a in aliens:
                y = a.ycor()
                y -= 40
                a.sety(y)
            alienspeed *= -1

        if isShooted(bullet, alien):
            if os.name == "nt":
                os.system("aplay blast.wav&")
            else:
                os.system("afplay blast.wav&")
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            #Reset the aliens
            xpos = random.randint(-200, 200)
            ypos = random.randint(100, 250)
            alien.setposition(xpos, ypos)

            #Update score
            score += 10
            scorestore = "Score: %s" %score
            scorepen.clear()
            scorepen.write(scorestore, False, align="Left", font=("Arial,", 14, "normal"))

            #Collision between player and aliens
        if isShooted(player, alien):
            player.hideturtle()
            alien.hideturtle()
            print("Game Over!")
            break

    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #Checking if the bullet is gone above
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"