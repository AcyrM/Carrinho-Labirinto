import pygame as pg
import cv2
import numpy as np
import sys
from random import random
from collections import deque


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


def detect_obstacles(frame_obj):
    # Lista com a dimensão dos objetos detectados
    obj_dim = []

    gray_obj = cv2.cvtColor(frame_obj, cv2.COLOR_BGR2GRAY)
    blur_obj = cv2.GaussianBlur(gray_obj, (3, 3), cv2.BORDER_DEFAULT)
    canny_obj = cv2.Canny(blur_obj, 125, 175)
    # cv2.imshow('canny_obj', canny_obj)
                                                 # cv2.RETR_LIST
                                                 # cv2.RETR_TREE     # cv2.CHAIN_APPROX_NONE
                                                 # cv2.RETR_EXTERNAL # cv2.CHAIN_APPROX_SIMPLE
    contours_obj, _ = cv2.findContours(canny_obj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(f"{len(contours_obj)} contour(s) found!")

    # frame_obj_copy = frame_obj.copy()

    for cnt_obj in contours_obj:
        if (cv2.contourArea(cnt_obj) > 40) and (cv2.contourArea(cnt_obj) < 5000):
            # Dimensões dos obstaculos
            x_obj, y_obj, width_obj, height_obj = cv2.boundingRect(cnt_obj)
            # Adiciona a lista a dimensão do objeto detectado
            obj_dim.append([x_obj, y_obj, width_obj, height_obj])

            # cv2.rectangle(frame_obj_copy, (x_obj, y_obj), (x_obj + width_obj, y_obj + height_obj), (255, 0, 255), 2)

    # cv2.imshow("frame_obj_copy", frame_obj_copy)
    return obj_dim


# "imagem da camera" -> como estou usando um video -> passar path do video
cap = cv2.VideoCapture("C:/Users/ph01g/PycharmProjects/detect_car_and_objetcts/videos/red_car.mp4")
# 1° frame do video
ret, frame = cap.read()
frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
if not ret:
    print(f"Erro coletando frame do video")
    sys.exit()

# tamanho do labirinto
cols, rows, _ = frame.shape
cols = int(cols/6)
rows = int(rows/6 )
TILE = 5

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

# Detecta os objetos e retorna os contornos do primeiro frame
obj_contours = detect_obstacles(frame.copy())

# Cria um labirinto do tamanho da imagem
grid = np.zeros((rows, cols), dtype=np.int8)

# Fechando o labirinto
# Bordas laterais do labirinto
for k in range(rows):
    grid[k][0] = 1
    grid[k][cols-1] = 1
# Bordas superior e inferior do labirinto
for k in range(cols):
    grid[0][k] = 1
    grid[rows-1][k] = 1

# Para cada objeto encontrado preenche ele como uma parede
for obj in obj_contours:
    for i in range(int(obj[0]/6), int((obj[0]+obj[2])/6)):
        for j in range(int(obj[1]/6), int((obj[1]+obj[3])/6)):
            grid[i][j] = 1

# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (10, 10)
goal = start
queue = deque([start])
visited = {start: None}

while True:
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    # draw BFS work
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

    # bfs, get path to mouse click
    mouse_pos = get_click_mouse_pos()
    if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
        queue, visited = bfs(start, mouse_pos, graph)
        goal = mouse_pos

    # draw path
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]
        print(path_segment)
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)
