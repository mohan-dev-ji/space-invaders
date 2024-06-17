import turtle
import math
import random

# Set up the screen
win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.setup(width=800, height=600)
win.tracer(0)


# Player setup
player = turtle.Turtle()
player.color("green")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player_speed = 15

def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -380:
        x = -380
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 380:
        x = 380
    player.setx(x)

# Bullet setup
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(stretch_wid=0.5, stretch_len=1)
bullet.hideturtle()

# Bullet state
bullet_speed = 20
bullet_state = "ready"

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        print("Bullet fired from", bullet.position())

def move_bullet():
    global bullet_state
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)
        if y > 275:
            bullet.hideturtle()
            bullet_state = "ready"
            print("Bullet reset to ready state")

# Create multiple enemies
class Enemy(turtle.Turtle):
    def __init__(self, color, x, y):
        super().__init__()
        self.color(color)
        self.shape("square")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        print(f"Created enemy with color: {color}, x: {x}, y: {y}")

    def __str__(self):
        return f"Enemy(color={self.pencolor()}, x={self.xcor()}, y={self.ycor()})"
    
# Enemy bullet class
class EnemyBullet(turtle.Turtle):
    def __init__(self, color, speed):
        super().__init__()
        self.color(color)
        self.shape("triangle")
        self.penup()
        self.speed(0)
        self.setheading(270)
        self.speed = speed
        self.hideturtle()

    def shoot_from(self, enemy):
        self.goto(enemy.xcor(), enemy.ycor() - 20)
        self.showturtle()

    def is_not_visible(self):
        return not self.isvisible()

# num_enemies = 8
enemies = []
enemy_speed = 1

# Red enemies
for i in range(2):
    for j in range(10):
        x = -380 + j * 40
        y = 100 + i * 40
        enemies.append(Enemy("red", x, y))

for i in range(2, 4):
    for j in range(10):
        x = -380 + j * 40
        y = 100 + i * 40
        enemies.append(Enemy("yellow", x, y))



# for enemy in enemies:
#     print(enemy)

# Create enemy bullets
enemy_bullets = [EnemyBullet("white", 5) for _ in range(10)]

def move_enemies():
    global enemy_speed
    for enemy in enemies:
        
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)
        
        # Reverse enemy direction at screen edges
        if x > 380 or x < -380:
            enemy_speed *= -1
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            


def is_collision(t1, t2):
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    return distance < 15

# Score setup
score = 0

# Score display
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("green")
score_pen.penup()
score_pen.setposition(-390, 260)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 16, "bold"))
score_pen.hideturtle()

def update_score():
    global score
    score += 10
    score_pen.clear()
    score_string = "Score: %s" % score
    score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
    print("Score updated:", score)

def check_collision():
    global bullet_state
        # Check for collision
    for enemy in enemies:
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            
            bullet.setposition(0, -400)
            enemy.hideturtle()
            enemies.remove(enemy)
            update_score()
            print("Collision detected! Enemy reset.")
            bullet_state = "ready"
            

        # Check for collision between player and enemy
        if is_collision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            return False
        
        if enemy.ycor() < -252:
            return False
    return True
        
def move_enemy_bullets():        
# Move enemy bullets
    for e_bullet in enemy_bullets:
        if e_bullet.isvisible():
            y = e_bullet.ycor()
            y -= e_bullet.speed
            e_bullet.sety(y)
            # Check for collision between player and enemy bullet
            if is_collision(player, e_bullet):
                player.hideturtle()
                e_bullet.hideturtle()
                print("Game Over")
                return False

        # Check if the enemy bullet has gone off screen
        if e_bullet.ycor() < -275:
            e_bullet.hideturtle()
    return True

# Randomly shoot bullets from enemies
def randomly_shoot_bullets():
    if random.randint(1, 50) == 1:
        shooter = random.choice(enemies)
        for e_bullet in enemy_bullets:
            if e_bullet.is_not_visible():
                e_bullet.shoot_from(shooter)
                break

def game_over():
    go_turtle = turtle.Turtle()
    go_turtle.color("red")
    go_turtle.penup()
    go_turtle.hideturtle()
    go_turtle.goto(0, 0)
    go_turtle.write("GAME OVER", align="center", font=("Arial", 80, "bold"))
    press_enter()

def you_win():
    go_turtle = turtle.Turtle()
    go_turtle.color("blue")
    go_turtle.penup()
    go_turtle.hideturtle()
    go_turtle.goto(0, 0)
    go_turtle.write("YOU WIN", align="center", font=("Arial", 80, "bold"))
    press_enter()

def press_enter():
    go_turtle = turtle.Turtle()
    go_turtle.color("white")
    go_turtle.penup()
    go_turtle.hideturtle()
    go_turtle.goto(0, -20)
    go_turtle.write("press enter to play again", align="center", font=("Arial", 30, "normal"))

# Keyboard bindings
win.listen()
win.onkey(move_left, "Left")
win.onkey(move_right, "Right")
win.onkey(fire_bullet, "space") 

# game_over = False
while True:
    win.update()

    move_enemies()
    move_bullet()

    if not check_collision():
        game_over()
        break

    if not move_enemy_bullets():
        game_over()
        break

    randomly_shoot_bullets()

    # Check if all enemies are shot
    if len(enemies) == 0:
        you_win()
        break
        
    
# Keep the window open
win.mainloop()