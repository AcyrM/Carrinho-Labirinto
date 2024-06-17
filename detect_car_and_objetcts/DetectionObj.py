import cv2
import numpy as np

cap = cv2.VideoCapture("C:/Users/pedro.gros/Documents/Detection-Object/cars.mp4")

# backgroundObject = cv2.createBackgroundSubtractorMOG2(history=1)
backgroundObject = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = np.ones([3,3], np.uint8)
kernel2 = None

def DetectionObj(frame):
   fgmask = backgroundObject.apply(frame)
   _, fgmask = cv2.threshold(fgmask, 10, 255, cv2.THRESH_BINARY)
   fgmask = cv2.erode(fgmask, kernel, iterations=1)
   fgmask = cv2.dilate(fgmask, kernel2, iterations=5)

   countours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   frameCopy = frame.copy()

   for cnt in countours:
      if cv2.contourArea(cnt) > 5500 and cv2.contourArea(cnt) < 8000:
         x, y, width, height = cv2.boundingRect(cnt)

         cv2.rectangle(frameCopy, (x,y), (x+width, y +height), (0,0,255), 2)

   return frameCopy


if __name__ == "__main__":
   while True:
      ret, frame = cap.read()
      if not ret:
         break
      
      frameCopy = DetectionObj(frame)

      cv2.imshow("fim", frameCopy)
      # cv2.imshow("fgmask", fgmask)
      # cv2.imshow("img", frame)
      if cv2.waitKey(1) == ord('q'):
         break

   cap.release()
   cv2.destroyAllWindows()