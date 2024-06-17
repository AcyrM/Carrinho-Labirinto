import cv2
import sys
import numpy as np
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import matplotlib.pyplot as plt


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


def showPNG(g):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(g, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()


def toHTML(g, start, end, cell_size=10):
    row_max = g.shape[0]
    col_max = g.shape[1]

    html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"' + \
           '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' + \
           '<html xmlns="http://www.w3.org/1999/xhtml"><head>' + \
           '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />' + \
           '<style type="text/css" media="screen">' + \
           '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
           str(cell_size * row_max) + 'px;border: 3px solid grey;}' + \
           'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
           'div.maze_row div.bl{background-color: black;}' + \
           'div.maze_row div.wh{background-color: white;}' + \
           'div.maze_row div.rd{background-color: red;}' + \
           'div.maze_row div.gr{background-color: green;}' + \
           'div.maze_row div{float: left;}' + \
           'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
           '</style></head><body>' + \
           '<div id="maze">'

    for row in range(row_max):
        html += '<div class="maze_row">'
        for col in range(col_max):
            if (row, col) == start:
                html += '<div class="gr"></div>'
            elif (row, col) == end:
                html += '<div class="rd"></div>'
            elif grid[row][col]:
                html += '<div class="bl"></div>'
            else:
                html += '<div class="wh"></div>'
        html += '</div>'
    html += '</div></body></html>'

    return html


if __name__ == '__main__':
    cap = cv2.VideoCapture("C:/Users/ph01g/PycharmProjects/detect_car_and_objetcts/videos/red_car.mp4")
    # 1° frame do video
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if not ret:
        print(f"Erro coletando frame do video")
        sys.exit()

    # Detecta os objetos e retorna os contornos do primeiro frame
    obj_contours = detect_obstacles(frame.copy())

    # tamanho do labirinto
    maze_height, maze_width, _ = frame.shape
    # Cria um labirinto do tamanho da imagem
    grid = np.zeros((maze_height, maze_width), dtype=np.int8)

    # Fechando o labirinto
    # Bordas laterais do labirinto
    for k in range(maze_height):
        grid[k][0] = 1
        grid[k][maze_width-1] = 1
    # Bordas superior e inferior do labirinto
    for s in range(maze_width):
        grid[0][s] = 1
        grid[maze_height-1][s] = 1

    # Para cada objeto encontrado preenche ele como uma parede
    for obj in obj_contours:
        for i in range(obj[0], obj[0]+obj[2]):
            for j in range(obj[1], obj[1]+obj[3]):
                grid[j][i] = 1

    maze = Maze()
    maze.grid = grid
    maze.start = (1, 1)
    maze.end = (maze_height-99, maze_width-2)
    showPNG(grid)
    # m = toHTML(grid, maze.start, maze.end)
    # f = open('teste.html', 'w')
    # f.write(m)
    # f.close()

    # maze.solver = BacktrackingSolver()
    # maze.generate_entrances()
    # maze.solve()

    # cv2.waitKey(0)
