# #####******Task 01******
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# raindrops = []  
# rain_tilt = 0.0  
# background_color = (0.529, 0.808, 0.922, 1.0)  # Initial background color (sky blue)
# window_color = (0.8, 0.898, 1.0)  # Initial window color (light blue)

# def display():
#     glClearColor(*background_color)  
#     glClear(GL_COLOR_BUFFER_BIT)  

#     glColor3f(0.0, 0.0, 0.0)  # Set the outline color to black

#     line_thickness = 20 
#     glLineWidth(line_thickness)  

#     # Draw the outline of a hollow triangle (roof)
#     glColor3f(0.376, 0.376, 0.376)  
#     glBegin(GL_TRIANGLES)  
#     glVertex2f(0, 0.8)  
#     glVertex2f(-0.4, 0.3)
#     glVertex2f(0.4, 0.3)  
#     glEnd()  # End drawing the triangle

#     # Draw the body of the house as ash grey
#     glColor3f(0.75, 0.75, 0.75)
#     glBegin(GL_POLYGON)  
#     glVertex2f(-0.35, 0.3)
#     glVertex2f(-0.35, -0.4)
#     glVertex2f(0.35, -0.4)
#     glVertex2f(0.35, 0.3)
#     glEnd()  # End drawing the polygon

#     glColor3f(0.545, 0.271, 0.075)  # Set the door color to brown

#     # Draw the door
#     glBegin(GL_POLYGON)
#     glVertex2f(-0.25, -0.05)
#     glVertex2f(-0.25, -0.4)
#     glVertex2f(-0.1, -0.4)
#     glVertex2f(-0.1, -0.05)
#     glEnd()

#     glColor3f(*window_color)  # Set the window color

#     # Draw the window
#     glBegin(GL_POLYGON)
#     glVertex2f(0.1, 0.1)
#     glVertex2f(0.3, 0.1)
#     glVertex2f(0.3, -0.1)
#     glVertex2f(0.1, -0.1)
#     glEnd()

#     draw_rain()  

#     glutSwapBuffers() 

# def draw_rain():
#     glLineWidth(2.0)  
#     glColor3f(0.0, 0.5, 1.0)  

#     glBegin(GL_LINES)  # Start drawing lines
#     for x, y in raindrops:
#         glVertex2f(x, y)
#         glVertex2f(x + rain_tilt, y - 0.05)  
#     glEnd()

# def update_rain(value):
#     global raindrops
#     new_raindrops = []
#     for x, y in raindrops:
#         y -= 0.02  # Move the raindrop downward
#         x += rain_tilt  
#         if y < -1:  
#             y = random.uniform(0.8, 1.0)
#             x = random.uniform(-1, 1)
#         new_raindrops.append((x, y))
#     raindrops = new_raindrops

#     glutPostRedisplay()  # Request a redisplay to show updated positions
#     glutTimerFunc(25, update_rain, 0)  # Call this function again after 25ms

# def mouse_click(button, state, x, y):
#     global rain_tilt
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         rain_tilt = -0.02  # Tilt rain left when left-clicked
#     elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         rain_tilt = 0.02  # Tilt rain right when right-clicked

# def keyboard(key, x, y):
#     global background_color, window_color
#     if key == b'n':
#         background_color = (0.0, 0.0, 0.2, 1.0)  # Night mode
#         window_color = (1.0, 1.0, 0.0)  # Yellow windows
#     elif key == b'd':
#         background_color = (0.529, 0.808, 0.922, 1.0)  # Day mode
#         window_color = (0.8, 0.898, 1.0)  # Light blue windows
#     glutPostRedisplay()

# def main():
#     glutInit(sys.argv)
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#     glutInitWindowSize(1200, 800)
#     glutCreateWindow(b'Task1')
#     glutDisplayFunc(display)
#     glutMouseFunc(mouse_click)
#     glutKeyboardFunc(keyboard)

#     # Initialize raindrop positions
#     for _ in range(200):
#         x = random.uniform(-1, 1)
#         y = random.uniform(-0.2, 1)
#         raindrops.append((x, y))

#     glutTimerFunc(25, update_rain, 0)  # Start rain animation
#     glutMainLoop()

# if __name__ == "__main__":
#     main()


#*******End Of task 01********


#******** Task 02*************
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
POINT_RADIUS = 0.03
MIN_SPEED, MAX_SPEED = 0.02, 0.1
SPEED_INCREMENT = 0.01
BLINK_INTERVAL = 500  # Blink interval in milliseconds

# Initialize variables
points = []
frozen = False

class Point:
    def __init__(self, x, y, color, speed):
        self.x, self.y = x, y
        self.color = color
        self.speed = speed
        self.velocity = [random.choice([-1, 1]) * speed, random.choice([-1, 1]) * speed]
        self.blinking = False
        self.blink_state = True  # True means visible, False means invisible
        self.original_color = color

    def toggle_blinking(self):
        self.blinking = not self.blinking

    def update_blinking(self):
        if self.blinking:
            self.blink_state = not self.blink_state
            self.color = self.original_color if self.blink_state else (0.0, 0.0, 0.0)

def draw_point(x, y, color):
    glColor3f(*color)
    num_segments = 100
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        xi = x + POINT_RADIUS * math.cos(theta)
        yi = y + POINT_RADIUS * math.sin(theta)
        glVertex2f(xi, yi)
    glEnd()

def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen

    for point in points:
        draw_point(point.x, point.y, point.color)

    glutSwapBuffers()

def mouse_click(button, state, x, y):
    global points
    if not frozen and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Convert screen coordinates to OpenGL coordinates
        x, y = x / WINDOW_WIDTH * 2 - 1, 1 - y / WINDOW_HEIGHT * 2
        color = (random.random(), random.random(), random.random())
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        points.append(Point(x, y, color, speed))
    elif not frozen and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.toggle_blinking()
    glutPostRedisplay()

def toggle_freeze():
    global frozen
    frozen = not frozen

def keyboard(key, x, y):
    global frozen
    if key == b' ':  # Spacebar to toggle freeze
        toggle_freeze()

def special_keys(key, x, y):
    if not frozen:
        if key == GLUT_KEY_DOWN:
            for point in points:
                point.speed = max(point.speed - SPEED_INCREMENT, MIN_SPEED)
        elif key == GLUT_KEY_UP:
            for point in points:
                point.speed = min(point.speed + SPEED_INCREMENT, MAX_SPEED)

def idle():
    if not frozen:
        for point in points:
            # Bounce from boundaries
            if point.x + POINT_RADIUS >= 1.0 or point.x - POINT_RADIUS <= -1.0:
                point.velocity[0] *= -1
            if point.y + POINT_RADIUS >= 1.0 or point.y - POINT_RADIUS <= -1.0:
                point.velocity[1] *= -1

            # Update position
            point.x += point.velocity[0] * point.speed
            point.y += point.velocity[1] * point.speed

    glutPostRedisplay()

def blink_timer(value):
    if not frozen:
        for point in points:
            point.update_blinking()
    glutTimerFunc(BLINK_INTERVAL, blink_timer, 0)  # Repeat timer

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b'The Amazing Box')

    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)  # Use for standard keys like spacebar
    glutSpecialFunc(special_keys)  # Use for arrow keys
    glutIdleFunc(idle)

    glOrtho(-1, 1, -1, 1, -1, 1)  # Set up orthographic projection

    # Start the blink timer
    glutTimerFunc(BLINK_INTERVAL, blink_timer, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()


# ###******** End of task 02*****