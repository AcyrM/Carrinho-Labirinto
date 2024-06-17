import cv2
import numpy as np
import sys


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


def tracking_car_detect_obj(frame_vid):
    fgmask = background_object.apply(frame_vid)
    _, fgmask = cv2.threshold(fgmask, 10, 255, cv2.THRESH_BINARY)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel2, iterations=5)

    contours_car, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    car_dim = [0, 0, 0, 0]

    # frame_copy = frame_vid.copy()
    for cnt_car in contours_car:
        # Desenha retangulo quando detecta carrinho
        if (cv2.contourArea(cnt_car) > 5500) and (cv2.contourArea(cnt_car) < 8000):
            # Dimensões dos carrinho
            x_car, y_car, width_car, height_car = cv2.boundingRect(cnt_car)
            # Lista a dimensão do carrinho
            car_dim = [x_car, y_car, width_car, height_car]

    # print(obj_dim)
    return car_dim

    # cv2.imshow("fim", frame_copy)
    # cv2.imshow("fgmask", fgmask)
    # cv2.imshow("img", frame_car)

def drawing_obstacles(frame):
    # Detecta os objetos e retorna os contornos
    obj_contours = detect_obstacles(frame.copy())

    frame_copy = frame.copy()
    # Desenha retangulo para cada um dos obstaculos detectados
    for obj in obj_contours:
        if not ((obj[0] >= car_contours[0]) and (obj[0] <= (car_contours[0] + car_contours[2])) and
                (obj[1] >= car_contours[1]) and (obj[1] <= (car_contours[1] + car_contours[3]))):
            cv2.rectangle(frame_copy, (obj[0], obj[1]), (obj[0] + obj[2], obj[1] + obj[3]), (255, 0, 255), 2)

    # Desenha retangulo para o carrinho detectado
    cv2.rectangle(frame_copy, (car_contours[0], car_contours[1]),
                    (car_contours[0] + car_contours[2], car_contours[1] + car_contours[3]), (0, 0, 255), 2)
    
    return frame_copy


if __name__ == '__main__':
    cap = cv2.VideoCapture("C:/Users/ph01g/PycharmProjects/detect_car_and_objetcts/videos/red_car.mp4")

    # background_object = cv2.createBackgroundSubtractorMOG2(history=2)
    background_object = cv2.bgsegm.createBackgroundSubtractorMOG()
    kernel = np.ones([3, 3], np.uint8)
    kernel2 = None

    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if not ret:
            print(f"Erro coletando frame do video")
            sys.exit()
        # Detecta o carrinho e retorna os contornos
        car_contours = tracking_car_detect_obj(frame.copy())


        frame_copy = drawing_obstacles(frame.copy())

        # print(car_contours)



        cv2.imshow("fim", frame_copy)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
