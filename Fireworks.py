from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import numpy as np
import time
import random

# Initial position of the rectangle
initial_position = np.array([[0], [0], [1]])


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


# Midpoint line BEGIN
def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
        if dx >= 0 and dy < 0: return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5
        if dx >= 0 and dy < 0: return 6


def convert_to_zone_zero(x, y, zone):
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


def convert_to_original(x, y, zone):
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


def drawline(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone_zero(x1, y1, zone)
    x2, y2 = convert_to_zone_zero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d_init = 2 * dy - dx
    x = x1
    y = y1
    while x < x2:
        x_back, y_back = convert_to_original(x, y, zone)
        draw_points(x_back, y_back)
        x += 1
        if d_init > 0:
            d_init += 2 * (dy - dx)
            y += 1
        else:
            d_init += 2 * dy


# Midpoint Circle

def MidpointCircle(r, cx, cy):
    for r in range(r, 0, -1):
        d = 1 - r
        x = 0
        y = r
        while x <= y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * x - 2 * y + 5
                y -= 1
            x += 1

            draw_points(x + cx, y + cy)
            draw_points(y + cx, x + cy)
            draw_points(y + cx, -x + cy)
            draw_points(x + cx, -y + cy)
            draw_points(-x + cx, -y + cy)
            draw_points(-y + cx, -x + cy)
            draw_points(-y + cx, x + cy)
            draw_points(-x + cx, y + cy)


# Firework Code
def firework(r, x, y):
    # axis lines

    random_r = random.uniform(0.0, 1.0)
    random_g = random.uniform(0.0, 1.0)
    random_b = random.uniform(0.0, 1.0)
    glColor3f(random_r, random_g, random_b)

    drawline(x, y, x + (5 * r), y)
    drawline(x, y, x - (5 * r), y)
    drawline(x, y, x, y + (5 * r))
    drawline(x, y, x, y - (5 * r))

    # axis small lines

    random_r = random.uniform(0.0, 1.0)
    random_g = random.uniform(0.0, 1.0)
    random_b = random.uniform(0.0, 1.0)
    glColor3f(random_r, random_g, random_b)

    drawline(x + (5.5 * r), y, x + (7 * r), y)
    drawline(x - (5.5 * r), y, x - (7 * r), y)
    drawline(x, y + (5.5 * r), x, y + (7 * r))
    drawline(x, y - (5.5 * r), x, y - (7 * r))

    # diagonal lines

    a = (5 * r) * math.cos(math.pi / 4)
    b = (5 * r) * math.sin(math.pi / 4)

    random_r = random.uniform(0.0, 1.0)
    random_g = random.uniform(0.0, 1.0)
    random_b = random.uniform(0.0, 1.0)
    glColor3f(random_r, random_g, random_b)

    drawline(x, y, x + a, y + b)
    drawline(x, y, x - a, y + b)
    drawline(x, y, x - a, y - b)
    drawline(x, y, x + a, y - b)

    # diagonal small lines

    random_r = random.uniform(0.0, 1.0)
    random_g = random.uniform(0.0, 1.0)
    random_b = random.uniform(0.0, 1.0)
    glColor3f(random_r, random_g, random_b)

    a = (5.5 * r) * math.cos(math.pi / 4)
    b = (5.5 * r) * math.sin(math.pi / 4)
    c = (7 * r) * math.cos(math.pi / 4)
    d = (7 * r) * math.sin(math.pi / 4)
    drawline(x + a, y + b, x + c, y + d)
    drawline(x - a, y + b, x - c, y + d)
    drawline(x - a, y - b, x - c, y - d)
    drawline(x + a, y - b, x + c, y - d)

    # center circle

    random_r = random.uniform(0.0, 1.0)
    random_g = random.uniform(0.0, 1.0)
    random_b = random.uniform(0.0, 1.0)
    glColor3f(random_r, random_g, random_b)

    MidpointCircle(r, x, y)


# Firework animation and display
def showFirework(r, x, y):
    global count
    global firework_radius
    if count <= r:
        r = count
        firework(r, x, y)  # center circle
        firework(r // 2, x + 150, y + 100)  # upper right circle
        firework(r // 2, x - 50, y + 150)  # upper circle
        count += 1
    else:
        r = firework_radius
        firework(r, x, y)  # upper circle
        firework(r // 2, x + 150, y + 100)  # upper  right circle
        firework(r // 2, x - 50, y + 150)  # upper circle


def iterate():
    glViewport(0, 0, 1500, 900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1500, 0.0, 900, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def transform(scaling_factor):
    global initial_position  # We need to modify the global variable

    # Update the position by changing the y-coordinate
    initial_position[1][0] += 1.00  # Move upward by 1 unit in each iteration

    # Calculate the scaling factor based on the y-coordinate
    scaling_factor = max(0.0, 1.0 - initial_position[1][0] / 400.0)  # Adjust the division factor as needed

    t = np.array([[1, 0, initial_position[0][0]],
                  [0, 1, initial_position[1][0]],
                  [0, 0, 1]])

    s = np.array([[scaling_factor, 0, 0],
                  [0, scaling_factor, 0],
                  [0, 0, 1]])

    ts = np.matmul(t, s)

    for i in range(-15, 16, 1):
        for j in range(20, -51, -1):
            v1 = np.array([[i],
                           [j],
                           [1]])

            v11 = np.matmul(ts, v1)

            if scaling_factor > 0.0:  # Only draw if scaling factor is positive
                glColor3f(0, 0, 1)
                glPointSize(3)
                glBegin(GL_POINTS)
                glVertex2f(v11[0][0] + 750, v11[1][0] + 50)
                glEnd()

    # rocket head
    d = 0
    for n in range(20, 55, 1):
        for m in range(-16 + d, 17 - d):
            v2 = np.array([[m], [n], [1]])

            v22 = np.matmul(ts, v2)
            if scaling_factor > 0.0:  # Only draw if scaling factor is positive
                glColor3f(1, 0, 0)
                glPointSize(3)
                glBegin(GL_POINTS)
                glVertex2f(v22[0][0] + 750, v22[1][0] + 50)
                glEnd()

        d += 1

    # rocket flame
    for p in range(-52, -80, -1):
        v3 = np.array([[0], [p], [1]])
        v4 = np.array([[-4], [p], [1]])
        v5 = np.array([[4], [p], [1]])
        v6 = np.array([[-8], [p], [1]])
        v7 = np.array([[8], [p], [1]])

        v33 = np.matmul(ts, v3)
        v44 = np.matmul(ts, v4)
        v55 = np.matmul(ts, v5)
        v66 = np.matmul(ts, v6)
        v77 = np.matmul(ts, v7)

        if scaling_factor > 0.0:  # Only draw if scaling factor is positive
            glColor3f(1, 1, 0)
            glPointSize(2)
            glBegin(GL_POINTS)
            glVertex2f(v33[0][0] + 750, v33[1][0] + 50)
            if p > -70:
                glVertex2f(v44[0][0] + 750, v44[1][0] + 50)
                glVertex2f(v55[0][0] + 750, v55[1][0] + 50)
                if p > -60:
                    glVertex2f(v66[0][0] + 750, v66[1][0] + 50)
                    glVertex2f(v77[0][0] + 750, v77[1][0] + 50)

            glEnd()


def showScreen():
    global current_step
    global level
    global firework_radius
    if current_step <= 450:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate()
        transform(1.0)
        glutSwapBuffers()
        glutPostRedisplay()
        time.sleep(0.005)
        current_step += 1

    else:
        time.sleep(0.1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate()
        center = np.array([[750, 0],  # original center , eita change korish
                           [0, 450]])
        if level == "1":
            v1 = center
            showFirework(firework_radius, v1[0][0], v1[1][1])
        elif level == "2":
            v1 = center
            showFirework(firework_radius, v1[0][0], v1[1][1])
            translation_vector = np.array([[350, 0],
                                           [0, 150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
            v1 = center
            translation_vector = np.array([[-350, 0],
                                           [0, -150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
        elif level == "3":
            v1 = center
            showFirework(firework_radius, v1[0][0], v1[1][1])
            translation_vector = np.array([[350, 0],
                                           [0, 150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
            v1 = center
            translation_vector = np.array([[-350, 0],
                                           [0, -150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
            v1 = center
            translation_vector = np.array([[-350, 0],
                                           [0, 150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
            v1 = center
            translation_vector = np.array([[350, 0],
                                           [0, -150]])
            v1 = np.add(translation_vector, v1)
            showFirework(firework_radius, v1[0][0], v1[1][1])
        glutPostRedisplay()
        glutSwapBuffers()


firework_radius = 15
count = 1
print(" 1 : Small Celebration")
print(" 2 : Medium Celebration")
print(" 3 : Max Celebration")

level = input("Kindly give the Level of celebration: ")

current_step = 0
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1500, 900)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)

glutMainLoop()