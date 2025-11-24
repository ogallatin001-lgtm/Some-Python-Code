import turtle
import random
import time
import os

#-----Setup Game-----
MazesCompleted = 0
background_color = "black"
tess_color = "red"
mazeColor = "blue"
turtle.setup(1000,1000) 
wn = turtle.Screen() 
wn.title("Handling keypresses!") 
wn.bgcolor(background_color) 
tess = turtle.Turtle() 
tess.color(tess_color) 
tess.penup()
mazeMaker = turtle.Turtle() 
mazeCorners = []
iteration = 0
timer_turtle = turtle.Turtle()
timer_turtle.hideturtle()
timer_turtle.penup()
timer_turtle.color("white") 
timer_turtle.goto(0, 450)
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.color("white")
score_turtle.goto(-450, 450)
score_turtle.clear()
score_turtle.write(f"Mazes Completed: {MazesCompleted}", align="left", font=("Arial", 20, "normal"))

#-----Load Shapes-----

#-----Declare Variables-----
game_time = 30  # How many seconds for the countdown
game_running = True # Is the game active?
jumpscare_counter = 0
jumpscare_shown = False
Wall_length = 100
width = 20
mazeMaker_x = int(mazeMaker.xcor())
mazeMaker_y = int(mazeMaker.ycor())
wall_portion = 0

#Create Maze Boudaries

mazeMaker.color(mazeColor)
mazeMaker.speed(0)
mazeMaker.penup()
mazeMaker.goto(-40,-60)
mazeMaker.pendown()
mazeMaker.pensize(3)

def create_new_maze():
    global iteration, Wall_length, mazeCorners, width
    
    # --- Reset the maze variables ---
    mazeMaker.clear()
    mazeCorners = []
    iteration = 0
    Wall_length = 100
    width = 20
    # --------------------------------
    
    # Reset position and orientation
    mazeMaker.penup()
    mazeMaker.goto(-40,-60)
    mazeMaker.setheading(0) # Ensure it starts facing East
    mazeMaker.pendown()
    tess.penup()
    tess.goto(0, 0)  # Reset player position

    for i in range (15):
        iteration += 1
        door_bool = random.choice([1, 2, 3])
        if door_bool == 1 or door_bool == 2:  
            wall_portion = random.randint(20, Wall_length - 60)
            mazeMaker.forward(wall_portion)
            mazeMaker.penup()
            door_width = 40
            mazeMaker.forward(door_width)
            mazeMaker.pendown()
            wall_portion = Wall_length - wall_portion - door_width
            mazeMaker.forward(wall_portion)
        else:
            mazeMaker.forward(Wall_length)
        mazeCorners.append((mazeMaker.xcor(), mazeMaker.ycor()))
        wall_bool = random.choice([1, 2, 3])
        if wall_bool == 1 or wall_bool == 2:
            if iteration < 12:
                mazeMaker.forward(width * 2)
                mazeMaker.left(180)
                mazeMaker.forward(width * 2)
                mazeMaker.left(180)
        mazeMaker.left(90)
        Wall_length += width

    mazeMaker.hideturtle()
    
#-----define functions-----

def Check_for_win():
    """Check if the player has reached the exit."""
    global game_running, game_time, jumpscare_shown, jumpscare_counter, score_turtle, MazesCompleted

    if not game_running:
        return

    # Define exit area (You may need to adjust this)
    exit_x = 180
    exit_y = 180

    if (tess.xcor() >= exit_x or
        tess.ycor() >= exit_y or tess.xcor() <= -exit_x or tess.ycor() <= -exit_y):
        
        game_running = False # Stop the game
        
        #-----update_score-----
        MazesCompleted += 1
        score_turtle.clear()
        score_turtle.write(f"Mazes Completed: {MazesCompleted}", align="left", font=("Arial", 20, "normal"))
        
        # Unbind movement keys
        wn.onkey(None, "Up")
        wn.onkey(None, "Left")
        wn.onkey(None, "Right")
        
        # Display "You Win!"
        timer_turtle.clear()
        timer_turtle.goto(0, 0)
        timer_turtle.write("You Win!", align="center", font=("Arial", 40, "bold"))
        
        # Define a function to reset the game after 2 seconds
        def reset_game():
            global game_running, game_time, jumpscare_shown, jumpscare_counter
            
            # Reset all game state variables
            game_time = 30
            jumpscare_counter = 0
            jumpscare_shown = False
            tess.goto(0, 0) # Reset player position
            
            # Re-bind keys
            wn.onkey(h1, "Up")
            wn.onkey(h2, "Left")
            wn.onkey(h3, "Right")

            # Start a new game
            game_running = True
            create_new_maze()
            countdown() # Start the timer again
            
        wn.ontimer(reset_game, 2000) # Wait 2 seconds before resetting

def game_over():
    """Stops the game and displays 'Game Over'."""
    global game_running
    game_running = False
    
    MazesCompleted = 0
    # Unbind movement keys
    wn.onkey(None, "Up")
    wn.onkey(None, "Left")
    wn.onkey(None, "Right")
    
    # Display "Game Over"
    timer_turtle.clear()
    timer_turtle.goto(0, 0) # Center of the screen
    timer_turtle.write("Game Over", align="center", font=("Arial", 40, "bold"))

def countdown():
    """The main timer loop."""
    global game_time
    global game_running

    if not game_running: # Stop the timer if game ended for another reason
        return

    timer_turtle.clear() # Clear the old time
    timer_turtle.write(f"Time: {game_time}", align="center", font=("Arial", 20, "normal"))
    
    if game_time > 0:
        game_time -= 1
        wn.ontimer(countdown, 1000) # Schedule this function to run again in 1 second (1000 ms)
    else:
        game_over() # Time's up!

def check_jumpscare(): 
    global jumpscare_counter, jumpscare_shown
    
    if jumpscare_shown:
        return

    if jumpscare_counter >= 10:
        jumpscare_shown = True
        
        try:
            wn.bgpic("turtle_jumpscare.gif") 
            wn.update()
        except Exception as e:
            print(f"Error loading 'turtle_jumpscare.gif': {e}")
            return # Stop if the image failed

        # Clear the jumpscare after 2 seconds without blocking
        def clear_bg():
            wn.bgpic(None)
            wn.update()

        wn.ontimer(clear_bg, 2000)

# The next four functions are our "event handlers".
def h1():
    if not game_running: return
    global jumpscare_counter
    tess.forward(20)
    jumpscare_counter += 1
    check_jumpscare()
    Check_for_win() # <-- Check for win after moving
    wn.title(f"turtle coords: ({int(tess.xcor())}, {int(tess.ycor())})")

def h2():
    if not game_running: return
    tess.left(45)

def h3():
    if not game_running: return
    tess.right(45)

def h4():
    wn.bye() 

# These lines "wire up" keypresses to the handlers we've defined.
wn.onkey(h1, "Up")
wn.onkey(h2, "Left")
wn.onkey(h3, "Right")
wn.onkey(h4, "q")

# --- Correct way to start the game ---

# 1. Draw the first maze
create_new_maze() 
# 2. Start the countdown timer
countdown() 
# 3. Start listening for key presses
wn.listen()
# 4. Start the main event loop
wn.mainloop()