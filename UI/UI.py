from PyQt5 import QtCore, QtGui, QtWidgets
from detect_car_and_objetcts.main import drawing_obstacles
from ComESP.main import WorkerBLE
import cv2
from picamera2 import Picamera2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1420, 900)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.resize(QtCore.QSize(1400, 900))
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(10, 10, 1400, 880)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Atualiza a cada 30 milissegundos
        
        self.cap = Picamera2()
        self.cap.start()
        # self.cap = cv2.VideoCapture(0)

        self.wd_menu = QtWidgets.QWidget(self.centralwidget)
        self.wd_menu.setMinimumSize(QtCore.QSize(210, 120))
        self.wd_menu.setMaximumSize(QtCore.QSize(210, 120))
        self.wd_menu.setStyleSheet("background-color: #CCCCCC")
        self.wd_menu.setObjectName("wd_menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.addWidget(self.wd_menu, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wd_menu)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bt_Calcular = QtWidgets.QPushButton(self.wd_menu)
        self.bt_Calcular.setMinimumSize(QtCore.QSize(167, 50))
        self.bt_Calcular.setMaximumSize(QtCore.QSize(213, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.bt_Calcular.setFont(font)
        self.bt_Calcular.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_Calcular.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_Calcular.setAutoFillBackground(False)
        self.bt_Calcular.setStyleSheet("QPushButton{\n"
"border: none;\n"
"color: #FFF\n"
"}\n"
"QPushButton:hover {\n"
"background: #BBBBBB\n"
" }"
"QPushButton:pressed {"
"background: #3B5998;"
"}")
        self.bt_Calcular.setFlat(True)
        self.bt_Calcular.setObjectName("bt_Calcular")
        self.verticalLayout.addWidget(self.bt_Calcular)
        self.bt_Iniciar = QtWidgets.QPushButton(self.wd_menu)
        self.bt_Iniciar.setMinimumSize(QtCore.QSize(167, 50))
        self.bt_Iniciar.setMaximumSize(QtCore.QSize(213, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.bt_Iniciar.setFont(font)
        self.bt_Iniciar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_Iniciar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_Iniciar.setAutoFillBackground(False)
        self.bt_Iniciar.setStyleSheet("QPushButton{\n"
"border: none;\n"
"color: #FFF\n"
"}\n"
"QPushButton:hover {\n"
"background: #BBBBBB\n"
" }"
"QPushButton:pressed {"
"background: #3B5998;"
"}")
        self.bt_Iniciar.setFlat(True)
        self.bt_Iniciar.setObjectName("bt_Iniciar")
        self.verticalLayout.addWidget(self.bt_Iniciar)
        MainWindow.setCentralWidget(self.centralwidget)
#BOTÕES CONTROLE-----------------------------------------------------
        buttonStartBLE = QtWidgets.QPushButton("Start BLE")
        buttonStartBLE.pressed.connect(self.startBLE)
        self.verticalLayout.addWidget(buttonStartBLE)
        
        buttonForward = QtWidgets.QPushButton("Forward")
        buttonForward.pressed.connect(self.Forward)
        self.verticalLayout.addWidget(buttonForward)
        
        buttonBackward = QtWidgets.QPushButton("Backward")
        buttonBackward.pressed.connect(self.Backward)
        self.verticalLayout.addWidget(buttonBackward)
        
        buttonRight = QtWidgets.QPushButton("Right")
        buttonRight.pressed.connect(self.Right)
        self.verticalLayout.addWidget(buttonRight)
        
        buttonLeft = QtWidgets.QPushButton("Left")
        buttonLeft.pressed.connect(self.Left)
        self.verticalLayout.addWidget(buttonLeft)

                
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robô com Visão Computacional"))
        self.bt_Calcular.setText(_translate("MainWindow", "Calcular"))
        self.bt_Iniciar.setText(_translate("MainWindow", "Iniciar"))


    # def update_frame(self):
    #     ret, frame = self.cap.read()
    #     if ret:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         h, w, ch = frame.shape
    #         bytesPerLine = ch * w
    #         frame = drawing_obstacles(frame)
    #         convertToQtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
    #         p = convertToQtFormat.scaled(1600, 900, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
    #         self.label.setPixmap(QtGui.QPixmap.fromImage(p))
    
    def update_frame(self):
        frame = self.cap.capture_array()
               
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        frame = drawing_obstacles(frame)
        convertToQtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        p = convertToQtFormat.scaled(1600, 900, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(QtGui.QPixmap.fromImage(p))
        
    threadpool = QtCore.QThreadPool()
        
    def startBLE(self):
        self.workerBLE = WorkerBLE()
        self.threadpool.start(self.workerBLE)
            
    def Forward (self):
        strToSend = "F"
        self.workerBLE.toSendBLE(strToSend)
        
    def Backward (self):
        strToSend = "B"
        self.workerBLE.toSendBLE(strToSend)
    
    def Right (self):
        strToSend = "R"
        self.workerBLE.toSendBLE(strToSend)
    
    def Left (self):
        strToSend = "L"
        self.workerBLE.toSendBLE(strToSend)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
