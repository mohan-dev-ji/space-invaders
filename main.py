import turtle
import math
import random

################################# CLASSES #################################

# Create Player class
class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("img/player.gif")
        self.penup()
        self.speed(0)
        self.setposition(0, -250)
        self.setheading(90)
        self.lives = 3
        self.player_speed = 15

    def move_left(self):
        if not game_on:
            return
        x = self.xcor()
        x -= player_speed
        if x < -380:
            x = -380
        self.setx(x)

    def move_right(self):
        if not game_on:
            return
        x = self.xcor()
        x += player_speed
        if x > 380:
            x = 380
        self.setx(x)

    # to do add shoot function after creating the Bullet class  
    def shoot(self):
        global game_on
        if game_on:
            if not bullet.isvisible():
                bullet.setposition(self.xcor(), self.ycor() + 10)
                bullet.showturtle()

# Create Bullet class
class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("img/bullet.gif")
        self.penup()
        self.speed(0)
        self.setheading(90)
        self.shapesize(stretch_wid=0.5, stretch_len=1)
        self.hideturtle()

    def move(self):
        if self.isvisible():
            y = self.ycor()
            y += bullet_speed
            self.sety(y)
            if self.ycor() > 275:
                self.hideturtle()

# Create Enemy class
class Enemy(turtle.Turtle):
    def __init__(self, color, x, y):
        super().__init__()
        if color == "red":        
            self.shape("img/alien1.gif")
        if color == "yellow":        
            self.shape("img/alien2.gif")
        self.color(color)
        self.penup()
        self.speed(0)
        self.goto(x, y)

# Enemy bullet class
class EnemyBullet(turtle.Turtle):
    def __init__(self, color, speed):
        super().__init__()
        self.color(color)
        self.shape("img/enemy-bullet.gif")
        self.penup()
        self.speed(0)
        # self.setheading(270)
        
        self.hideturtle()

    def move(self):
        if self.isvisible():
            y = self.ycor()
            y -= 5
            self.sety(y)
            if self.ycor() < -300:
                self.hideturtle()

    def shoot_from(self, shooter):
        if not self.isvisible():
            self.setposition(shooter.xcor(), shooter .ycor() - 10)
            self.showturtle()
class Explosion(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("img/explosion.gif")
        self.penup()
        self.hideturtle()

    def explode(self, x, y):
        self.goto(x, y)
        self.showturtle()
        win.update()
        turtle.ontimer(self.hideturtle, 10)  # Hide after 300ms

################################# FUNCTIONS #################################
def move_enemies():
    global enemy_speed, enemies, bullet
    if not game_on:
        return
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
        
        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet.setposition(0, -10000)
            enemy.hideturtle()
            enemies.remove(enemy)
            update_score()

def move_bullet():
    if not game_on:
        return
    bullet.move()

def move_enemy_bullets():
    global e_bullet
    if not game_on:
        return
    for e_bullet in enemy_bullets:
        e_bullet.move()
        

def randomly_shoot_bullets():
    global enemies, enemy_bullets 
    if random.randint(1, 50) == 1:
        if enemies:
            shooter = random.choice(enemies)
            e_bullet = random.choice(enemy_bullets)
            e_bullet.shoot_from(shooter)
        else:
            print("no enemies")

def is_collision(t1, t2):
    global explosion
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    if distance < 20:
        explosion.explode(t1.xcor(), t1.ycor())
    return distance < 20

def update_score():
    global score
    score += 10
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="left", font=("Arial", 16, "bold"))

def check_game_over():
    global e_bullet
    for enemy in enemies:
        if enemy.ycor() < -250:
            return True
    for e_bullet in enemy_bullets:
        if is_collision(player, e_bullet):
            player.hideturtle()
            e_bullet.hideturtle()
            print("Game Over")
            return True
    return False

def create_enemies():
    global enemies
    # Red enemies
    for i in range(2):
        for j in range(10):
            x = -380 + j * 50
            y = 100 + i * 40
            enemies.append(Enemy("red", x, y))
    # Yellow enemies
    for i in range(2, 4):
        for j in range(10):
            x = -380 + j * 50
            y = 100 + i * 40
            enemies.append(Enemy("yellow", x, y))

def game_over_msg():
    global player, bullet
    go_turtle = turtle.Turtle()
    go_turtle.color("red")
    go_turtle.penup()
    go_turtle.hideturtle()
    go_turtle.goto(0, 0)
    go_turtle.write("GAME OVER", align="center", font=("Arial", 80, "bold"))
    press_enter()
    player.clear()
    bullet.clear() 

def you_win_msg():
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
    go_turtle.write("Press enter to play again", align="center", font=("Arial", 30, "normal"))

def break_out():
    global running, enemy_speed
    enemy_speed = 0
    running = False

################################# GAME SET UP #################################

def play_game():
    global win, player, bullet, enemies, enemy_bullets, score, player_speed, enemy_speed, bullet_speed, score_pen, running, game_on, explosion
    # Set up the screen
    win = turtle.Screen()
    win.bgcolor("black")
    win.title("Space Invaders")
    win.setup(width=800, height=600)
    win.tracer(0)
    # Register the custom GIFs
    win.addshape("img/player.gif")
    win.addshape("img/alien1.gif")
    win.addshape("img/alien2.gif")
    win.addshape("img/bullet.gif")
    win.addshape("img/enemy-bullet.gif")
    win.addshape("img/explosion.gif")

    player = Player()
    bullet = Bullet()
    explosion = Explosion()
    enemies = []
    enemy_bullets = [EnemyBullet("white", 5) for _ in range(10)]
    score = 0
    player_speed = 15
    enemy_speed = 1
    bullet_speed = 15   

    # Score display
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color("green")
    score_pen.penup()
    score_pen.hideturtle()
    score_pen.setposition(-390, 260)
    score_pen.write(f"Score: {score}", align="left", font=("Arial", 16, "bold"))

    # Keyboard bindings
    win.listen()
    win.onkey(player.move_left, "Left")
    win.onkey(player.move_right, "Right")
    win.onkey(player.shoot, "space") 

    create_enemies()

    ################################# GAME LOOP #################################
    running = True
    game_on = True
    while running:
        
        win.update()

        move_enemies()
        move_bullet()
        move_enemy_bullets()

        randomly_shoot_bullets()
        
        # if check_game_over or len(enemies) == 0:
        if check_game_over():
            game_over_msg()
            game_on = False
            win.listen()
            win.onkeypress(break_out, "Return")
                # break
        if len(enemies) == 0:
            you_win_msg()
            game_on = False
            win.listen()
            win.onkeypress(break_out, "Return")

    if enemies:
        for enemy in enemies:
            enemy.hideturtle()
        enemies.clear()
    if enemy_bullets:
        for e_bullet in enemy_bullets:
            e_bullet.hideturtle() 
        enemy_bullets.clear()
    bullet.clear()
    win.clearscreen()
    print("the end")
    play_game()

    win.mainloop()

play_game()
