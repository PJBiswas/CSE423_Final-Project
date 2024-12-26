from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin, cos, pi

# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

CATCHER_WIDTH = 150 #the width and height of the catcher
CATCHER_HEIGHT = 30
WHITE = (1.0, 1.0, 1.0)
catcher_color = WHITE
catcher_x = SCREEN_WIDTH - 50 #x-coordinate of the catcher's position
catcher_y = SCREEN_HEIGHT // 2 #y-coordinate of the catcher's position


game_over = False
paused = False
exit_game = False
RETRY_BUTTON_LOCATION = (20, SCREEN_HEIGHT - 50)
PAUSE_BUTTON_LOCATION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

retry_color =  (1.0, 1.0, 1.0)
pause_color =  (1.0, 1.0, 1.0)
exit_color =  (1.0, 1.0, 1.0)

# New variable for football field color
football_field_color = [0.529, 0.808, 0.922]  # Default color: light blue
current_color_flag = 0  # 0: Default, 1: Green, 2: Blue, 3: Red 4: back to default

# Football variables
ball_radius = 15
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed = 1
ball_direction = [0, 0]  # Initial direction 

# Player variables
player_radius = 30
player1_x = SCREEN_WIDTH // 3
player1_y = SCREEN_HEIGHT // 2

player2_x = 2 * SCREEN_WIDTH // 3
player2_y = SCREEN_HEIGHT // 2

player1_speed = 5
player2_speed = 5

player1_score = 0
player2_score = 0

player1_movement = {'W': False, 'A': False, 'S': False, 'D': False}
player2_movement = {'I': False, 'J': False, 'K': False, 'L': False}

#_______________________________________________________________Football______________________________________________________

class Football:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = [0, 0]  # Initial direction 

    def move(self): #updating the position of the ball
        # Update ball position
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        # Check collision with walls
        if self.x - self.radius < 50 or self.x + self.radius > SCREEN_WIDTH - 50:
            self.direction[0] *= -1  # Reverse the x-direction

        if self.y - self.radius < 50 or self.y + self.radius > SCREEN_HEIGHT - 50:
            self.direction[1] *= -1  # Reverse the y-direction
            
#___________________________________________button______________________________________________________________________________________________________________________________________________________________

# Draw functions
def draw_retry_button(x, y, color=retry_color):
    draw_midpoint_line(x, y, x + 20, y - 20, color)
    draw_midpoint_line(x, y, x + 20, y + 20, color)
    draw_midpoint_line(x, y, x + 50, y, color)

def draw_pause_button(x, y, color=pause_color):
    draw_midpoint_line(x + 10, y + 20, x + 10, y - 20, color)
    draw_midpoint_line(x - 10, y + 20, x - 10, y - 20, color)

def draw_play_button(x, y, color=pause_color):
    draw_midpoint_line(x - 10, y + 20, x - 10, y - 20, color)
    draw_midpoint_line(x - 10, y + 20, x + 10, y, color)
    draw_midpoint_line(x - 10, y - 20, x + 10, y, color)

def draw_exit(x, y, color=exit_color):
    draw_midpoint_line(x - 10, y + 10, x + 10, y - 10, color)
    draw_midpoint_line(x - 10, y - 10, x + 10, y + 10, color)
    

def handle_mouse(button, state, x, y): #represent the mouse button, button state, and coordinates of the mouse click.
    global paused, exit_game, game_over, player1_score, player2_score

    # Transform y to match OpenGL coordinate system
    y = SCREEN_HEIGHT - y #adjusts the y-coordinate to match the OpenGL system.

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: #checks if the left mouse button is pressed down

        #checks if the mouse click is within the bounds of the pause button
        if (PAUSE_BUTTON_LOCATION[0] - 20 <= x <= PAUSE_BUTTON_LOCATION[0] + 20 #checks if the mouse click is within the bounds of the pause button
            and PAUSE_BUTTON_LOCATION[1] - 20 <= y <= PAUSE_BUTTON_LOCATION[1] + 20):
            paused = not paused
            if paused:
                print("Game Paused")
            else:
                print("Game Resumed")

        #checks if the mouse click is within the bounds of the exit button
        elif (EXIT_BUTTON_LOCATION[0] - 10 <= x <= EXIT_BUTTON_LOCATION[0] + 10 
            and EXIT_BUTTON_LOCATION[1] - 10 <= y <= EXIT_BUTTON_LOCATION[1] + 10):
            print("Exiting Game")
            glutLeaveMainLoop()  # This will close the window

        #This block checks if the mouse click is within the bounds of the retry button.
        elif (RETRY_BUTTON_LOCATION[0] <= x <= RETRY_BUTTON_LOCATION[0] + 50
            and RETRY_BUTTON_LOCATION[1] <= y <= RETRY_BUTTON_LOCATION[1] + 20):
            print("Resetting Game")
            reset_game()
            reset_ball()


#___________________________________________CATCHER________________________________________________________________________________________
def draw_catcher():
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(catcher_x, catcher_y, 0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)  #rotates the catcher by 90 degrees counterclockwise around the z-axis
    glTranslatef(-catcher_x, -catcher_y, 0.0)

    # Draw the catcher
    x1, x2 = catcher_x - CATCHER_WIDTH / 2, catcher_x + CATCHER_WIDTH / 2 #define the x-coordinates for the left and right edges of the catcher
    x3, x4 = x1 + 40, x2 - 40 #create a smaller width for the top part of the catcher
    y1, y2 = catcher_y, catcher_y - 40 #represent the top and bottom y-coordinates of the catcher.
    draw_midpoint_line(x1, y1, x2, y1, catcher_color)
    draw_midpoint_line(x3, y2, x4, y2, catcher_color)
    draw_midpoint_line(x2, y1, x4, y2, catcher_color)
    draw_midpoint_line(x1, y1, x3, y2, catcher_color)

    glPopMatrix()

def draw_second_catcher():
    # Move the second catcher more to the left
    second_catcher_x = SCREEN_WIDTH // 30  #sets the x-coordinate for the second catcher

    # Set the position for the second catcher
    second_catcher_y = SCREEN_HEIGHT // 2 #sets the y-coordinate for the second catcher

    # Rotate the second catcher by 90 degrees clockwise
    glPushMatrix()
    glTranslatef(second_catcher_x, second_catcher_y, 0.0)
    glRotatef(-90.0, 0.0, 0.0, 1.0)  # Rotate around the z-axis (0.0, 0.0, 1.0)
    glTranslatef(-second_catcher_x, -second_catcher_y, 0.0)

    # Draw the second catcher
    x1, x2 = second_catcher_x - CATCHER_WIDTH / 2, second_catcher_x + CATCHER_WIDTH / 2
    x3, x4 = x1 + 40, x2 - 40
    y1, y2 = second_catcher_y, second_catcher_y - 40
    draw_midpoint_line(x1, y1, x2, y1, catcher_color)
    draw_midpoint_line(x3, y2, x4, y2, catcher_color)
    draw_midpoint_line(x2, y1, x4, y2, catcher_color)
    draw_midpoint_line(x1, y1, x3, y2, catcher_color)

    glPopMatrix()


#_______________________________________________________Midpoint Line Algo___________________________________________________

def draw_midpoint_line(x1, y1, x2, y2, color): #defines the two endpoints of the line and color
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = to_zone0(zone, x1, y1) #call the zone0converter function used to convert the coordinates based on the determined zone.
    x2, y2 = to_zone0(zone, x2, y2)

    dx = x2 - x1 #change in x
    dy = y2 - y1 #change in y

    d = 2 * dy - dx #initial decision
    incrE = 2 * dy #for updating d if east is chosen
    incrNE = 2 * (dy - dx) #for updating d if northeast is chosen

    x = x1 
    y = y1
    x0, y0 = to_zoneM(zone, x, y)

    draw_points(x0, y0, color)
    while x < x2:
        if d <= 0:  
            d = d + incrE #if dinit less than zero then d is updated by adding dinit and de
            x = x + 1 #move the iteration to the next pixel in the east direction
        else:
            d = d + incrNE #if dinit greater than or equal to zero then d is updated by adding dinit and dne
            x = x + 1 #move the iteration to the next pixel in the northeast direction
            y = y + 1 ##move the iteration to the next pixel in the northeast direction
        x0, y0 = to_zoneM(zone, x, y)

        draw_points(x0, y0, color)

    
def to_zone0(zone, x, y): #for converting to zone zero coordinates
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def to_zoneM(zone, x, y): ##for converting coordinates from Zone 0 to their original zone
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def find_zone(x1, y1, x2, y2): #determines the zone of a line based on the signs of the differences in x and y coordinates between its two endpoints
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy): # For Zone 0, 3, 4 and 7
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy <= 0:
            return 7
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
    else:                 #For zone 1, 2, 5, and 6
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6
        
def draw_points(x, y, color=WHITE, size=2):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
     
#_____________________________________________Midpoint Circle Algo_________________________________________________________    

def circ_point(x, y, cx, cy):               
    glVertex2f(cx + x, cy + y) #south
    glVertex2f(cx + y, cy + x) #southeast
    glVertex2f(cx + y, cy - x) #east
    glVertex2f(cx + x, cy - y) #northeast
    glVertex2f(cx - x, cy - y) #north
    glVertex2f(cx - y, cy - x) #northwest
    glVertex2f(cx - y, cy + x) #west
    glVertex2f(cx - x, cy + y) #southwest

def mid_circle(cx, cy, radius): #implementing midpoint circle algorithm
    d = 1 - radius #initial decision parameter
    x = 0
    y = radius

    glBegin(GL_POINTS) #for drawing points for the circle
    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0: #if initial decision parameter is negative then east pixel is chosen
            d = d + 2 * x + 3 #updating decision parameter accordingly
        else: #if decision parameter is positive southeast pixel is chosen
            d = d + 2 * x - 2 * y + 5 #updating decision parameter accordingly
            y = y - 1 #value of y is decremented by 1

        x = x + 1 #in both cases value of x will increment by 1
        circ_point(x, y, cx, cy)

    glEnd()

def draw_circle(x, y, radius):
    mid_circle(x, y, radius)

def draw_filled_circle(x, y, radius):
    num_segments = 100
    delta_theta = 2.0 * pi / num_segments

    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        theta = _ * delta_theta
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()

#________________________________________________Simple Line Drawing________________________________________________________

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_football_field():
    glColor3fv(football_field_color)
    glBegin(GL_QUADS)
    glVertex2f(50, 50)
    glVertex2f(SCREEN_WIDTH - 50, 50)
    glVertex2f(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
    glVertex2f(50, SCREEN_HEIGHT - 50)
    glEnd()

    # Set color for lines
    glColor3f(1.0, 1.0, 1.0)  # White for the lines

    # Draw field outline
    draw_line(50, 50, SCREEN_WIDTH - 50, 50)
    draw_line(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
    draw_line(50, 50, 50, SCREEN_HEIGHT - 50)
    draw_line(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

    # Draw midfield line
    draw_line(SCREEN_WIDTH // 2, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    # Draw center circle using midpoint circle algorithm
    mid_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)

    # Draw penalty areas (adjust coordinates to make them the same size)
    draw_rectangle(50, SCREEN_HEIGHT // 2 - 100, 150, SCREEN_HEIGHT // 2 + 100)
    draw_rectangle(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 100, SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 + 100)
    
    
    

def draw_rectangle(x1, y1, x2, y2): #for the Dbox
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_player(x, y):
    glColor3f(1.0, 1.0, 1.0)                           # White color for player 1
    mid_circle(x, y, player_radius)
    draw_filled_circle(x, y, player_radius)

def draw_player2(x, y):
    glColor3f(0.0, 0.0, 0.0)                           # Black color for player 2
    mid_circle(x, y, player_radius)
    draw_filled_circle(x, y, player_radius)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


#________________________________________________Player Movement_________________________________________________________________

from math import sqrt

def update_player_positions():
    global player1_x, player1_y, player2_x, player2_y, player1_speed, player2_speed, paused

    if not paused:
        # Update player 1 position
        player1_dx = 0
        player1_dy = 0
        if player1_movement['W']:
            player1_dy += player1_speed
        if player1_movement['A']:
            player1_dx -= player1_speed
        if player1_movement['S']:
            player1_dy -= player1_speed
        if player1_movement['D']:
            player1_dx += player1_speed

        # Calculate new positions
        new_player1_x = player1_x + player1_dx
        new_player1_y = player1_y + player1_dy

        # Check boundaries for player 1
        if 50 + player_radius <= new_player1_x <= SCREEN_WIDTH - 50 - player_radius:
            player1_x = new_player1_x
        if 50 + player_radius <= new_player1_y <= SCREEN_HEIGHT - 50 - player_radius:
            player1_y = new_player1_y

        # Update player 2 position
        player2_dx = 0
        player2_dy = 0
        if player2_movement['I']:
            player2_dy += player2_speed
        if player2_movement['J']:
            player2_dx -= player2_speed
        if player2_movement['K']:
            player2_dy -= player2_speed
        if player2_movement['L']:
            player2_dx += player2_speed

        # Calculate new positions
        new_player2_x = player2_x + player2_dx
        new_player2_y = player2_y + player2_dy

        # Check boundaries for player 2
        if 50 + player_radius <= new_player2_x <= SCREEN_WIDTH - 50 - player_radius:
            player2_x = new_player2_x
        if 50 + player_radius <= new_player2_y <= SCREEN_HEIGHT - 50 - player_radius:
            player2_y = new_player2_y

        # Check for overlap between players
        dx = player2_x - player1_x
        dy = player2_y - player1_y
        distance = sqrt(dx**2 + dy**2)

        # If players overlap, resolve the collision
        if distance < 2 * player_radius:
            overlap = 2 * player_radius - distance
            dx_normalized = dx / distance if distance != 0 else 1
            dy_normalized = dy / distance if distance != 0 else 1

            # Push players apart equally
            player1_x -= dx_normalized * overlap / 2
            player1_y -= dy_normalized * overlap / 2
            player2_x += dx_normalized * overlap / 2
            player2_y += dy_normalized * overlap / 2

def keyboard(key, x, y):
    global player1_movement, player2_movement, football_field_color, current_color_flag



    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = True
    elif key == b'A' or key == b'a':
        player1_movement['A'] = True
    elif key == b'S' or key == b's':
        player1_movement['S'] = True
    elif key == b'D' or key == b'd':
        player1_movement['D'] = True

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = True
    elif key == b'J' or key == b'j':
        player2_movement['J'] = True
    elif key == b'K' or key == b'k':
        player2_movement['K'] = True
    elif key == b'L' or key == b'l':
        player2_movement['L'] = True
        
        
    # Change football field color based on keyboard input
    
    if key == b'1':
        football_field_color = [0.0, 1.0, 0.0]  # Green
        current_color_flag = 1
    elif key == b'2':
        football_field_color = [0.0, 0.0, 1.0]  # Blue
        current_color_flag = 2
    elif key == b'3':
        football_field_color = [1.0, 0.0, 0.0]  # Red
        current_color_flag = 3
    elif key == b'4':
        football_field_color = [0.529, 0.808, 0.922]  # Light blue (default)
        current_color_flag = 0

    glutPostRedisplay()


def keyboard_release(key, x, y):
    global player1_movement, player2_movement

    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = False
    elif key == b'A' or key == b'a':
        player1_movement['A'] = False
    elif key == b'S' or key == b's':
        player1_movement['S'] = False
    elif key == b'D' or key == b'd':
        player1_movement['D'] = False

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = False
    elif key == b'J' or key == b'j':
        player2_movement['J'] = False
    elif key == b'K' or key == b'k':
        player2_movement['K'] = False
    elif key == b'L' or key == b'l':
        player2_movement['L'] = False

    glutPostRedisplay()

football = Football(ball_x, ball_y, ball_radius, ball_speed)

#__________________________________________________________Ball Movement________________________________________________

def check_collision(player_x, player_y, player_radius, ball):
    distance = ((player_x - ball.x) ** 2 + (player_y - ball.y) ** 2) ** 0.5 #euclidean
    if distance < player_radius + ball.radius and distance > 0:  # Check if distance is not zero
        # Collision detected, update ball direction based on player's position
        dx = ball.x - player_x
        dy = ball.y - player_y
        length = (dx**2 + dy**2)**0.5
        ball.direction = [dx / length, dy / length]
        
def update_timer(value):
    global paused

    if not paused:
        football.move()
        update_ball_position()
        glutPostRedisplay()

    glutTimerFunc(10, update_timer, 0)



def update_ball_position():
    global ball_x, ball_y, SCREEN_WIDTH, SCREEN_HEIGHT, paused,player1_score, player2_score 

    if paused != True:
        football.move()
        check_collision(player1_x, player1_y, player_radius, football)
        check_collision(player2_x, player2_y, player_radius, football)

        # Check if the ball is in the right goal area
        if (football.x + ball_radius > SCREEN_WIDTH - 50) and \
        (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
            print("Player1: Goal!!!")
            player1_score += 1
            print('Player1',player1_score,':',player2_score,'player2')
            reset_ball()

        # Check if the ball is in the left goal area
        elif (football.x - ball_radius < 50) and \
            (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
            print("Player2: Goal!!!")
            player2_score += 1
            print('Player1',player1_score,':',player2_score,'player2')
            reset_ball()
        global player1_lives, player2_lives

    if (football.x + ball_radius > SCREEN_WIDTH - 50) and (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
        print("Player 1 scores!")
        player2_lives -= 1
        reset_ball()

    elif (football.x - ball_radius < 50) and (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
        print("Player 2 scores!")
        player1_lives -= 1
        reset_ball()

    if player1_lives == 0 or player2_lives == 0:
        print("Game Over!")
        reset_game()
        reset_ball()

    if player1_score ==3:
        print('Player 1 wins the game')
        print('Game Over!')
        reset_game() 
        reset_ball()
    elif player2_score ==3:
        print('Player 1 wins the game')
        print('Game Over!')
        reset_game() 
        reset_ball()

#___________________________________Draw heart__________________________________
def draw_heart(x, y, size, color):
    glColor3fv(color)
    glBegin(GL_POINTS)
    for angle in range(0, 360):
        theta = angle * pi / 180
        px = size * (16 * sin(theta)**3)
        py = -size * (13 * cos(theta) - 5 * cos(2*theta) - 2 * cos(3*theta) - cos(4*theta))
        glVertex2f(x + px, y + py)
    glEnd()

player1_lives = 3  # Player 1 starts with 3 hearts
player2_lives = 3  # Player 2 starts with 3 hearts

def display_hearts():
    heart_size = 5  # Adjust heart size as needed
    spacing = 50  # Adjust spacing between hearts

    # Player 1 hearts (left side)
    for i in range(player1_lives):
        draw_heart(100 + i * spacing, SCREEN_HEIGHT - 50, heart_size, (1.0, 0.0, 0.0))  # Red hearts

    # Player 2 hearts (right side)
    for i in range(player2_lives):
        draw_heart(SCREEN_WIDTH - 100 - i * spacing, SCREEN_HEIGHT - 50, heart_size, (0.0, 0.0, 1.0))  # Blue hearts





        
#####################################################################
# resetting

def reset_ball():
    # Reset the ball to the center of the field
    global ball_x, ball_y, ball_direction
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_direction = [0, 0]  # Stop the ball


    
def reset_game():
    global player1_x, player1_y, player2_x, player2_y, ball_x, ball_y, ball_direction, player1_score, player2_score, ball_speed, paused
    player1_x = SCREEN_WIDTH // 3
    player1_y = SCREEN_HEIGHT // 2
    player2_x = 2 * SCREEN_WIDTH // 3
    player2_y = SCREEN_HEIGHT // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    football.x = ball_x
    football.y = ball_y
    ball_direction = [0, 0]  # Stop the ball
    player1_score = 0
    player2_score = 0
    
    paused = True  # To ensure the game is not paused after reset




#___________________________________________DISPLAY________________________________________________________________________________________    

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # White color for lines
    glPointSize(2.0)
    update_player_positions()
    football.move()
    update_ball_position()
    reset_ball()
    draw_football_field()
    draw_player(player1_x, player1_y)  # Draw player 1
    draw_player2(player2_x, player2_y)  # Draw player 2
    glColor3f(1.0, 1.0, 0.0)
    draw_filled_circle(football.x, football.y, ball_radius)
    global catcher_color
    draw_catcher()
    catcher_color = (0.0, 0.0, 0.0)  # Black color
    draw_second_catcher()
    draw_football_field()
    draw_player(player1_x, player1_y)
    draw_player2(player2_x, player2_y)
    draw_filled_circle(football.x, football.y, ball_radius)
    draw_catcher()
    draw_second_catcher()
    display_hearts()
    
    
    draw_retry_button(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    draw_exit(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])
    if not paused:
        draw_pause_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else:
        draw_play_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    glutSwapBuffers()

    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Football")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_release)  
    glutTimerFunc(0, update_timer, 0)
    glClearColor(0.529, 0.808, 0.922, 1.0)
    glutMouseFunc(handle_mouse)

    glutMainLoop()

if __name__ == "__main__":
    main()