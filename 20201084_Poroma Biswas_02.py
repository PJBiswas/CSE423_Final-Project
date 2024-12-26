import random
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global Variables
window_width, window_height = 800, 600
shooter_x, shooter_y = 400, 50
shooter_width, shooter_height = 60, 20
shooter_speed = 10
projectiles = []
falling_circles = []
score = 0
miss_count = 0
misfire_count = 0
game_over = False
paused = False
last_time = time.time()

# Button Positions and Dimensions
buttons = {
    "restart": {"x": 50, "y": 550, "width": 50, "height": 30},
    "play_pause": {"x": 125, "y": 550, "width": 50, "height": 30},
    "exit": {"x": 200, "y": 550, "width": 50, "height": 30},
}

# Circle Drawing Function
def draw_circle(x_center, y_center, radius):
    glBegin(GL_LINE_LOOP)
    num_segments = 100
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex2f(x_center + x, y_center + y)
    glEnd()

# Rocket-shaped Shooter Drawing Function
def draw_shooter(x, y, width, height):
    rocket_body_width = width * 0.6
    rocket_body_height = height * 1.5

    glBegin(GL_POLYGON)  # Rocket body
    glVertex2f(x + width * 0.2, y)  # Bottom left
    glVertex2f(x + width * 0.2, y + rocket_body_height)  # Top left
    glVertex2f(x + width * 0.8, y + rocket_body_height)  # Top right
    glVertex2f(x + width * 0.8, y)  # Bottom right
    glEnd()

    glBegin(GL_TRIANGLES)  # Rocket nose
    glVertex2f(x + width * 0.2, y + rocket_body_height)
    glVertex2f(x + width * 0.8, y + rocket_body_height)
    glVertex2f(x + width * 0.5, y + rocket_body_height + height * 0.5)  # Tip of the nose
    glEnd()

    glBegin(GL_TRIANGLES)  # Left fin
    glVertex2f(x, y)
    glVertex2f(x + width * 0.2, y)
    glVertex2f(x + width * 0.2, y + height * 0.5)
    glEnd()

    glBegin(GL_TRIANGLES)  # Right fin
    glVertex2f(x + width * 0.8, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width * 0.8, y + height * 0.5)
    glEnd()

# Projectile Class
class Projectile:
    def __init__(self, x, y, radius=5):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        draw_circle(self.x, self.y, self.radius)

# Circle Class
class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        draw_circle(self.x, self.y, self.radius)

# Special Circle Class
class SpecialCircle(Circle):
    def __init__(self, x, y, radius, expansion_rate=40):
        super().__init__(x, y, radius)
        self.base_radius = radius
        self.expansion_rate = expansion_rate
        self.growth = True

    def update_radius(self, delta_time):
        if self.growth:
            self.radius += self.expansion_rate * delta_time
            if self.radius >= self.base_radius * 1.5:
                self.growth = False
        else:
            self.radius -= self.expansion_rate * delta_time
            if self.radius <= self.base_radius * 0.5:
                self.growth = True

# Collision Detection
def has_collided(circle, projectile):
    dx = circle.x - projectile.x
    dy = circle.y - projectile.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance < circle.radius + projectile.radius

# Draw Buttons
def draw_button(x, y, width, height, color, label):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    draw_text(label, x + width // 4, y + height // 4)

# Draw Text
def draw_text(text, x, y):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Check if a falling circle touches the shooter
def circle_touches_shooter(circle):
    return (
        circle.y - circle.radius <= shooter_y + shooter_height and
        circle.x + circle.radius >= shooter_x and
        circle.x - circle.radius <= shooter_x + shooter_width
    )

# Spawn a falling circle at a random horizontal position
def spawn_circle():
    x = random.randint(50, window_width - 50)
    y = window_height - 50
    if random.random() < 0.2:  # 20% chance to spawn a special circle
        radius = random.randint(20, 30)
        falling_circles.append(SpecialCircle(x, y, radius))
    else:
        radius = random.randint(20, 30)
        falling_circles.append(Circle(x, y, radius))

# Reset the game state
def reset_game():
    global score, miss_count, misfire_count, game_over, falling_circles, projectiles
    score = 0
    miss_count = 0
    misfire_count = 0
    game_over = False
    falling_circles.clear()
    projectiles.clear()
    print("Game restarted!")

# Display callback
def display():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)

    if not game_over:
        glColor3f(0, 1, 0)  # Green for the shooter
        draw_shooter(shooter_x, shooter_y, shooter_width, shooter_height)

        glColor3f(1, 1, 0)  # Yellow for projectiles
        for projectile in projectiles:
            projectile.draw()

        for circle in falling_circles:
            if isinstance(circle, SpecialCircle):
                glColor3f(0, 1, 1)  # Cyan for special circles
            else:
                glColor3f(1, 0, 0)  # Red for regular circles
            circle.draw()
    else:
        draw_text("Game Over!", window_width // 2 - 50, window_height // 2)

    # Draw buttons
    draw_button(
        x=buttons["restart"]["x"],
        y=buttons["restart"]["y"],
        width=buttons["restart"]["width"],
        height=buttons["restart"]["height"],
        color=(0, 1, 1),  # Cyan
        label="<--"
    )
    draw_button(
        x=buttons["play_pause"]["x"],
        y=buttons["play_pause"]["y"],
        width=buttons["play_pause"]["width"],
        height=buttons["play_pause"]["height"],
        color=(1, 0.5, 0),  # Amber
        label="||" if not paused else "\u25b6"
    )
    draw_button(
        x=buttons["exit"]["x"],
        y=buttons["exit"]["y"],
        width=buttons["exit"]["width"],
        height=buttons["exit"]["height"],
        color=(1, 0, 0),  # Red
        label="X"
    )

    glutSwapBuffers()

# Update callback
def update(value):
    global falling_circles, projectiles, score, miss_count, misfire_count, game_over, paused

    if game_over or paused:
        glutTimerFunc(16, update, 0)
        return

    global last_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    for circle in falling_circles[:]:
        circle.y -= 70 * delta_time
        if isinstance(circle, SpecialCircle):
            circle.update_radius(delta_time)

        if circle.y + circle.radius < 0:
            miss_count += 1
            falling_circles.remove(circle)
            if miss_count >= 3:
                game_over = True

        elif circle_touches_shooter(circle):
            game_over = True

    for projectile in projectiles[:]:
        projectile.y += 100 * delta_time
        if projectile.y - projectile.radius > window_height:
            projectiles.remove(projectile)
            misfire_count += 1
            if misfire_count >= 3:
                game_over = True

    for circle in falling_circles[:]:
        for projectile in projectiles[:]:
            if has_collided(circle, projectile):
                if isinstance(circle, SpecialCircle):
                    score += 5
                else:
                    score += 1
                print(f"Score: {score}")
                falling_circles.remove(circle)
                projectiles.remove(projectile)

    if len(falling_circles) < 5:
        spawn_circle()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Mouse callback
def mouse(button, state, x, y):
    global paused, game_over

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = window_height - y

        if (
            buttons["restart"]["x"] <= x <= buttons["restart"]["x"] + buttons["restart"]["width"]
            and buttons["restart"]["y"] <= y <= buttons["restart"]["y"] + buttons["restart"]["height"]
        ):
            reset_game()
        elif (
            buttons["play_pause"]["x"] <= x <= buttons["play_pause"]["x"] + buttons["play_pause"]["width"]
            and buttons["play_pause"]["y"] <= y <= buttons["play_pause"]["y"] + buttons["play_pause"]["height"]
        ):
            paused = not paused
        elif (
            buttons["exit"]["x"] <= x <= buttons["exit"]["x"] + buttons["exit"]["width"]
            and buttons["exit"]["y"] <= y <= buttons["exit"]["y"] + buttons["exit"]["height"]
        ):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

# Keyboard callback
def keyboard(key, x, y):
    global shooter_x, paused, game_over

    if key == b'a' and shooter_x > 0:
        shooter_x -= shooter_speed
    elif key == b'd' and shooter_x < window_width - shooter_width:
        shooter_x += shooter_speed
    elif key == b' ' and not game_over:
        projectiles.append(Projectile(shooter_x + shooter_width // 2, shooter_y + shooter_height))
    elif key == b'p':
        paused = not paused
    elif key == b'r':
        reset_game()
    elif key == b'q':
        print(f"Goodbye! Final Score: {score}")
        glutLeaveMainLoop()

# Reshape callback
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Main function
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Shoot The Circles!")
glClearColor(0, 0, 0, 1)

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutTimerFunc(16, update, 0)

for _ in range(5):
    spawn_circle()

glutMainLoop()
