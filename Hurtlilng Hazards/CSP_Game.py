'''Allow for user input.
Use color and movement.
Use list indexing.
Manipulate strings.
Respond to events.
Reduce duplication of code by using functions.
To help you in creating your artwork:
Use existing turtle methods. 
Choose descriptive variable names.
Comment code segments or blocks of statements.
lines that imitate background movement'''

#group roles
#william - controls movement and art/finding images timer
#otto - hurtle the hazards
#malachi - N/A
#kai - commentator 

#-----import modules-----
import turtle
import math
import random
import time

#-----Declare Variables-----
# Set player position variables directly based on player.pos()
player_start_x = 0
player_start_y = -250
flame_offset_y = -25 # Offset for the flame relative to the player
score = 0
stopwatch = 0
game_is_running = False
COLLISION_DISTANCE = 25 # Threshold for collision (based on default turtle sizes)

#-----Lists-----
fallingObjects = []

#-----Setup Turtle-----
wn = turtle.Screen()
wn.setup(width=800, height=700) # Increased window size for better display
wn.title("Hurtling Hazards")
wn.bgcolor("#111111")
wn.tracer(0) # Turn off screen updates for smoother animation

# Player Turtle
player = turtle.Turtle()
player.penup()
player.speed(0)
player.setheading(90)
player.shape("turtle")
player.shapesize(1.5)
player.color("#FFFFFF")
player.goto(player_start_x, player_start_y)

# Backdrop Drawer
backdrop_drawer = turtle.Turtle()
backdrop_drawer.hideturtle()
backdrop_drawer.speed(0)
backdrop_drawer.penup()
backdrop_drawer.pencolor("#aaaaaa")

# Score and Status Display
score_guy = turtle.Turtle()
score_guy.color("#ffffff")
score_guy.penup()
score_guy.hideturtle()
score_guy.speed(0)
score_guy.goto(0,0) # Position for score

#-----meteors-----
wn.addshape("meteor.gif")
wn.addshape("explosion.gif")

# Flame Turtle (Propulsion visual)
wn.addshape("turtleFlame.gif") # Assumes this GIF is available
flameTurtle = turtle.Turtle()
flameTurtle.shape("turtleFlame.gif")
flameTurtle.setheading(270)
flameTurtle.penup()
flameTurtle.goto(player_start_x, player_start_y + flame_offset_y)

# Falling Star (Unused in the collision logic, but kept for context)
falling_star = turtle.Turtle()
falling_star.color("#f5d33b")
falling_star.shape("circle")
falling_star.penup()
falling_star.hideturtle()

# Set Background Image
wn.bgpic("StarBackdrop.gif") # Uncomment if you have this file

#-----Create Backdrop-----
def draw_backdrop():
    """Draws the boundaries of the game area."""
    backdrop_drawer.goto(-200, -300)
    backdrop_drawer.pendown()
    backdrop_drawer.goto(200, -300)
    backdrop_drawer.goto(200, 300)
    backdrop_drawer.goto(-200, 300)
    backdrop_drawer.goto(-200,-300)
    backdrop_drawer.penup()

draw_backdrop()

#-----Define Functions-----

def update_player_pos(x_change):
    """Updates player and flame position, handles boundary checks."""
    global player
    
    # Calculate new x position
    new_x = player.xcor() + x_change
    
    # Boundary check (stay within -200 and 200)
    if new_x > 200:
        new_x = 200
    elif new_x < -200:
        new_x = -200

    # Move player and flame
    player.setx(new_x)
    flameTurtle.goto(new_x, player.ycor() + flame_offset_y)

def left():
    """Moves the player and flame left."""
    if game_is_running:
        update_player_pos(-20)

def right():
    """Moves the player and flame right."""
    if game_is_running:
        update_player_pos(20)

def create_new_hazard():
    """Creates a new hazard turtle and adds it to the list."""
    
    if len(fallingObjects) < 100:
        new_hazard = turtle.Turtle()
        new_hazard.speed(0)
        new_hazard.penup()
        new_hazard.shape("square") # Changed to square for better hazard visibility
        new_hazard.shapesize(1.2)
        new_hazard.color("#FF6F61") # Hazard color
        
        new_hazard.shape("meteor.gif")

        objectX = random.randint(-190, 190) # Start within boundaries
        objectY = 320 # Start just above the screen
        new_hazard.goto(objectX, objectY)
        
        fallingObjects.append(new_hazard)

def hazard_spawner():
    """Spawns a new hazard and schedules the next spawn."""
    if game_is_running:
        # Increase spawn rate slightly as score increases
        spawn_delay = max(1000 - (score // 100), 500) # Min delay 0.5s
        
        create_new_hazard()
        wn.ontimer(hazard_spawner, spawn_delay)

def check_collision(t1, t2):
    """Checks if the distance between two turtles is within the collision threshold."""
    # Use the distance() method to find the Euclidean distance
    if t1.distance(t2) < COLLISION_DISTANCE:
        return True
    return False

def move_hazards():
    global fallingObjects, score
    
    if not game_is_running:
        return


    for hazard in fallingObjects:
        current_y = hazard.ycor()
        
        if check_collision(player, hazard):
            game_over("COLLISION")
            return
        if current_y < -320:
            new_x = random.randint(-190, 190)
            hazard.goto(new_x, 320)
            continue


        dynamic_speed = 10 + (score // 1000) 
        hazard.sety(current_y - dynamic_speed) 
        
    wn.update() # Update the screen once per loop for smoothness
    wn.ontimer(move_hazards, 50) # Repeat this function after 50ms

def timer():
    """Updates the game timer and score display."""
    global game_is_running, stopwatch, score
    
    if game_is_running:
        score_guy.goto(200, 300)
        score += 50
        stopwatch += 1
        score_guy.clear()
        
        # --- String Manipulation and Score Display ---
        # Format score with leading zeros for visual uniformity
        score_string = str(score).zfill(5) 
        time_string = str(stopwatch)
        
        score_guy.write(f"SCORE: {score_string}\nTIME: {time_string}s", align="center", font=("Courier", 18, "normal"))
    
    wn.ontimer(timer, 1000) # Update every 1 second

def game_over(reason):
    """Stops the game and displays the game over message."""
    global game_is_running
    game_is_running = False
    
    # Stop all timers/loops
    # We rely on the `if game_is_running` checks in the functions
    
    player.shape("explosion.gif")
    flameTurtle.hideturtle()
    

    score_guy.clear()
    score_guy.goto(0, 50)
    
    final_message = "GAME OVER"
    if reason == "COLLISION":
        final_message = final_message + " - HAZARD HIT!"
    
    final_score_line = f"Final Score: {str(score).zfill(5)}"
    final_time_line = f"Time Survived: {stopwatch} seconds"
    
    score_guy.write(f"{final_message}\n\n{final_score_line}\n{final_time_line}", 
                    align="center", font=("Courier", 24, "bold"))
    
    
    for hazard in fallingObjects:
        hazard.hideturtle()
        
    wn.update() 


def game_started():
    """Initializes and starts the main game loops."""
    global game_is_running
    if not game_is_running: # Prevent multiple starts
        game_is_running = True
        hazard_spawner() # Start hazard creation
        move_hazards()   # Start hazard movement and collision checking
        timer()          # Start score/time tracking
    
#-----Event Handling-----
wn.onkeypress(left, "a")
wn.onkeypress(right, "d")
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(game_started, "space") # Use space bar to start the game
wn.listen()

# Display initial instructions
score_guy.write("Press SPACE to Start!", align="center", font=("Courier", 24, "bold"))

# Start the main turtle loop
wn.mainloop()