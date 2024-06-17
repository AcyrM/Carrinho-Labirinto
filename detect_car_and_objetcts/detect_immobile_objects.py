import cv2

cap = cv2.VideoCapture("C:/Users/ph01g/PycharmProjects/detect_car_and_objetcts/videos/black_car.mp4")

ret, frame = cap.read()

# Caso não ocorra problemas durante a captura do frame
if ret:
    # cv2.imshow("img", frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)

    blur = cv2.GaussianBlur(gray, (3, 3), cv2.BORDER_DEFAULT)
    # cv2.imshow('blur', blur)

    canny = cv2.Canny(blur, 125, 175)
    # cv2.imshow('canny', canny)
                                                    # cv2.RETR_LIST
                                                    # cv2.RETR_TREE     # cv2.CHAIN_APPROX_NONE
                                                    # cv2.RETR_EXTERNAL # cv2.CHAIN_APPROX_SIMPLE
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(f"{len(contours)} contour(s) found!")

    frameCopy = frame.copy()

    for cnt in contours:
        if (cv2.contourArea(cnt) > 40) and (cv2.contourArea(cnt) < 4000):
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(frameCopy, (x, y), (x + width, y + height), (255, 0, 255), 2)

    cv2.imshow("frameCopy", frameCopy)

cv2.waitKey(0)
