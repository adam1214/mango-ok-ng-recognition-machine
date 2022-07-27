import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_MainWindow
from model import AutoRun, ManRun, Camera, ReadModbus
import serial
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):    
    def __init__(self, parent=None):
        """ 初始化
            - 物件配置
            - 相關屬性配置
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.statusBar = self.statusBar()
        # 設定 Frame Rate 的參數
        self.frame_num1 = 0
        self.frame_num2 = 0
        self.frame_num3 = 0
        self.frame_num4 = 0
        self.frame_rate1 = 0.0
        self.frame_rate2 = 0.0
        self.frame_rate3 = 0.0
        self.frame_rate4 = 0.0
        self.t_total1 = 1.0
        self.t_total2 = 1.0
        self.t_total3 = 1.0
        self.t_total4 = 1.0
        # 設定相機功能
        self.ProcessCam1 = Camera(bright=124, multicam=2) # cam1 = port3
        self.ProcessCam2 = Camera(bright=48, multicam=1) # cam2 = port2
        self.ProcessCam3 = Camera(bright=80, multicam=3) # cam3 = port4
        self.ProcessCam4 = Camera(bright=60, multicam=0) # cam4 = port1
        cam_status = [self.ProcessCam1.connect, self.ProcessCam2.connect, self.ProcessCam3.connect, self.ProcessCam4.connect]
        # print('cam1: ', self.ProcessCam1.connect, ', and cam2: ', self.ProcessCam2.connect, ', and cam3: ', self.ProcessCam3.connect, ', and cam4: ', self.ProcessCam4.connect)
        if self.ProcessCam1.connect and self.ProcessCam2.connect and self.ProcessCam3.connect and self.ProcessCam4.connect:
            self.ProcessCam1.rawdata.connect(self.getRaw1)  
            self.ProcessCam1.open()
            self.ProcessCam1.start()
            self.ProcessCam2.rawdata.connect(self.getRaw2) 
            self.ProcessCam2.open()
            self.ProcessCam2.start()
            self.ProcessCam3.rawdata.connect(self.getRaw3) 
            self.ProcessCam3.open()
            self.ProcessCam3.start()
            self.ProcessCam4.rawdata.connect(self.getRaw4) 
            self.ProcessCam4.open()
            self.ProcessCam4.start()
            self.camBtn_auto.setEnabled(True)
            self.camBtn_manual.setEnabled(True)
            self.camBtn_save.setEnabled(True)
        else:
            error_message = ''
            index = 0
            for i in cam_status:
                if not i:
                    error_message += '相機 {ind} 未連線\n'.format(ind = index + 1)
                index += 1
            QtWidgets.QMessageBox.warning(None, 'Check', error_message)
            sys.exit()
        
        #設定Modbus初始化
        self.slaveid = 2
        try:
            self.master = modbus_rtu.RtuMaster(serial.Serial(port='com7', baudrate=19200, bytesize=8, parity='O', stopbits=1, xonxoff=0)) # connection with modbus
            self.master.set_timeout(1.0)
            self.master.set_verbose(True)
            # print('main thread in self.master: ', self.master)
            self.ReadModbusProcess = ReadModbus(slave_id=self.slaveid, modbus_handler=self.master, message=self.debugBar) #read modbus 50-65 slave ready status 
            self.ReadModbusProcess.plcstatus.connect(self.getStatus)
            self.ReadModbusProcess.open()
            self.ReadModbusProcess.start()
        except:
            QtWidgets.QMessageBox.warning(None, 'Check', '請檢察PLC通訊連線')
            sys.exit()

        # button function
        self.camBtn_auto.clicked.connect(self.autoMode)
        self.camBtn_manual.clicked.connect(self.manMode)
        self.camBtn_save.clicked.connect(self.saveImg)

    def getStatus(self, status):
        self.readystatus = status
        print('main readystatus: ', self.readystatus)
        if self.readystatus[10]:  # M60 on
            self.camBtn_manual.setEnabled(False)
            self.camBtn_save.setEnabled(False)
            try:
                if self.auto_mode:
                    pass
            except:
                self.auto_mode = AutoRun(slave_id=self.slaveid, modbus_handler=self.master, cam1=self.ProcessCam1, \
                                        cam2=self.ProcessCam2, cam3=self.ProcessCam3, cam4=self.ProcessCam4)
                self.auto_mode.open()
                self.auto_mode.start()
        else:  # M60 on
            self.camBtn_manual.setEnabled(True)
            self.camBtn_save.setEnabled(True)
            try:
                if not self.auto_mode:
                    self.auto_mode.stop()
            except:
                pass
            
    def getRaw1(self, data):  # data 為接收到的影像
        self.showData1(data)  # 將影像傳入至 showData()

    def getRaw2(self, data):
        self.showData2(data)

    def getRaw3(self, data):
        self.showData3(data)

    def getRaw4(self, data):
        self.showData4(data)
    
    def autoMode(self):
        self.camBtn_manual.setEnabled(False)
        self.camBtn_save.setEnabled(False)
        print('readystatus: ', self.readystatus)
        # if not self.readystatus[13]:  # M64 off
        if self.readystatus[11] and not self.readystatus[10]: # M61 on
            self.master.execute(self.slaveid, cst.WRITE_SINGLE_COIL, 60, output_value=1)
            self.auto_mode = AutoRun(slave_id=self.slaveid, modbus_handler=self.master, cam1=self.ProcessCam1, \
                                     cam2=self.ProcessCam2, cam3=self.ProcessCam3, cam4=self.ProcessCam4)
            self.auto_mode.open()
            self.auto_mode.start()
            self.camBtn_manual.setEnabled(False)
            self.camBtn_save.setEnabled(False)
        elif self.readystatus[10]:  # M60 on
            self.master.execute(self.slaveid, cst.WRITE_SINGLE_COIL, 60, output_value=0)
            self.camBtn_manual.setEnabled(True)
            self.camBtn_save.setEnabled(True)
            try:
                self.auto_mode.stop()
            except:
                pass
        else:
            self.camBtn_manual.setEnabled(True)
            self.camBtn_save.setEnabled(True)

    def manMode(self):
        self.camBtn_auto.setEnabled(False)
        self.camBtn_manual.setEnabled(False)
        self.camBtn_save.setEnabled(False)
        print('readystatus', self.readystatus)

        if self.readystatus[15]:
            self.master.execute(self.slaveid, cst.WRITE_SINGLE_COIL, 62, output_value=1)
            self.man_mode = ManRun(slave_id=self.slaveid, modbus_handler=self.master, autobtn=self.camBtn_auto,manbtn=self.camBtn_manual, savebtn=self.camBtn_save)
            self.man_mode.open()
            self.man_mode.start()
        else:
            self.camBtn_auto.setEnabled(True)
            self.camBtn_manual.setEnabled(True)
            self.camBtn_save.setEnabled(True)
            QtWidgets.QMessageBox.information(None, 'Check', '手動未預備')

    def saveImg(self):
        """ 啟動攝影機的影像讀取 """
        if self.ProcessCam1.connect:
            self.ProcessCam1.save(camera_index='cam1')
        if self.ProcessCam2.connect:
            self.ProcessCam2.save(camera_index='cam2')
        if self.ProcessCam3.connect:
            self.ProcessCam3.save(camera_index='cam3')
        if self.ProcessCam4.connect:
            self.ProcessCam4.save(camera_index='cam4')
        self.master.execute(self.slaveid, cst.WRITE_SINGLE_COIL, 65, output_value=1)

    def showData1(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (RGB格式)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        # viewData 的顯示設定
        self.viewData1.setScaledContents(True)  # 尺度可變
        ### 將 Qimage 物件設置到 viewData 上
        self.viewData1.setPixmap(QtGui.QPixmap.fromImage(qimg))
        ### 顯示大小設定
        roi_rate = 0.3
        # print(self.Nx, self.Ny, self.frameGeometry().width(), self.frameGeometry().height())
        if self.frameGeometry().width() < 1200 or self.frameGeometry().height() < 900:
            roi_rate = 0.4
        else: 
            roi_rate = 0.6
        # print('roi_rate: ', roi_rate)
        self.viewForm1.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewForm1.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData1.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData1.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        # Frame Rate 計算並顯示到狀態欄上
        if self.frame_num1 == 0:
            self.time_start = time.time()
        if self.frame_num1 >= 0:
            self.frame_num1 += 1
            self.t_total1 = time.time() - self.time_start
            if self.frame_num1 % 100 == 0:
                self.framePerSecond()

    def showData2(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (RGB格式)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        # viewData 的顯示設定
        self.viewData2.setScaledContents(True)  # 尺度可變
        ### 將 Qimage 物件設置到 viewData 上
        self.viewData2.setPixmap(QtGui.QPixmap.fromImage(qimg))
        ### 顯示大小設定
        roi_rate = 0.3
        # print(self.Nx, self.Ny, self.frameGeometry().width(), self.frameGeometry().height())
        if self.frameGeometry().width() < 1200 or self.frameGeometry().height() < 900:
            roi_rate = 0.4
        else: 
            roi_rate = 0.6
        # print('roi_rate: ', roi_rate)
        self.viewForm2.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewForm2.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData2.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData2.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        # Frame Rate 計算並顯示到狀態欄上
        if self.frame_num2 == 0:
            self.time_start = time.time()
        if self.frame_num2 >= 0:
            self.frame_num2 += 1
            self.t_total2 = time.time() - self.time_start
            if self.frame_num2 % 100 == 0:
                self.framePerSecond()

    def showData3(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (RGB格式)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        # viewData 的顯示設定
        self.viewData3.setScaledContents(True)  # 尺度可變
        ### 將 Qimage 物件設置到 viewData 上
        self.viewData3.setPixmap(QtGui.QPixmap.fromImage(qimg))
        ### 顯示大小設定
        roi_rate = 0.3
        # print(self.Nx, self.Ny, self.frameGeometry().width(), self.frameGeometry().height())
        if self.frameGeometry().width() < 1200 or self.frameGeometry().height() < 900:
            roi_rate = 0.4
        else: 
            roi_rate = 0.6
        # print('roi_rate: ', roi_rate)
        self.viewForm3.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewForm3.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData3.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData3.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        # Frame Rate 計算並顯示到狀態欄上
        if self.frame_num3 == 0:
            self.time_start = time.time()
        if self.frame_num3 >= 0:
            self.frame_num3 += 1
            self.t_total3 = time.time() - self.time_start
            if self.frame_num3 % 100 == 0:
                self.framePerSecond()

    def showData4(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (RGB格式)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        # viewData 的顯示設定
        self.viewData4.setScaledContents(True)  # 尺度可變
        ### 將 Qimage 物件設置到 viewData 上
        self.viewData4.setPixmap(QtGui.QPixmap.fromImage(qimg))
        ### 顯示大小設定
        roi_rate = 0.3
        # print(self.Nx, self.Ny, self.frameGeometry().width(), self.frameGeometry().height())
        if self.frameGeometry().width() < 1200 or self.frameGeometry().height() < 900:
            roi_rate = 0.4
        else: 
            roi_rate = 0.6
        # print('roi_rate: ', roi_rate)
        self.viewForm4.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewForm4.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData4.setMinimumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        self.viewData4.setMaximumSize(self.Nx*roi_rate, self.Ny*roi_rate)
        # Frame Rate 計算並顯示到狀態欄上
        if self.frame_num4 == 0:
            self.time_start = time.time()
        if self.frame_num4 >= 0:
            self.frame_num4 += 1
            self.t_total4 = time.time() - self.time_start
            if self.frame_num4 % 100 == 0:
                self.framePerSecond()

    def framePerSecond(self):
        if self.frame_num1 % 100 == 0:
            self.frame_rate1 = float(self.frame_num1) / self.t_total1
        if self.frame_num2 % 100 == 0:
            self.frame_rate2 = float(self.frame_num2) / self.t_total2
        if self.frame_num2 % 100 == 0:
            self.frame_rate3 = float(self.frame_num3) / self.t_total3
        if self.frame_num2 % 100 == 0:
            self.frame_rate4 = float(self.frame_num4) / self.t_total4
        # self.debugBar('Camera 1: {fps1:0.3f} frames/sec, Camera 2: {fps2:0.3f} frames/sec, Camera 3: {fps3:0.3f} frames/sec, \
        #                 Camera 4: {fps4:0.3f} frames/sec '.format(fps1=self.frame_rate1, fps2=self.frame_rate2, fps3=self.frame_rate3, fps4=self.frame_rate4))  # 顯示到狀態欄

    def closeEvent(self, event):
        """ 視窗應用程式關閉事件 """
        reply = QtWidgets.QMessageBox.question(self, '訊息',"確定離開?", \
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.ProcessCam1.running:
                self.ProcessCam1.stop()   
                self.ProcessCam1.close()      
                self.ProcessCam1.terminate() 
            if self.ProcessCam2.running:
                self.ProcessCam2.stop()
                self.ProcessCam2.close()
                self.ProcessCam2.terminate()
            if self.ProcessCam3.running:
                self.ProcessCam3.stop()
                self.ProcessCam3.close()
                self.ProcessCam3.terminate()
            if self.ProcessCam4.running:
                self.ProcessCam4.stop()
                self.ProcessCam4.close()
                self.ProcessCam4.terminate()
            try:
                self.ReadModbusProcess.stop()
                self.ReadModbusProcess.terminate()
            except:
                pass
            try:
                self.auto_mode.stop()
                self.auto_mode.terminate()
            except:
                pass
            try:
                self.man_mode.stop()
                self.man_mode.terminate()
            except:
                pass
            time.sleep(0.1)
            QtWidgets.QApplication.closeAllWindows()
        else:
            event.ignore()

    def debugBar(self, msg):
        """ 狀態欄功能顯示 """
        self.statusBar.showMessage(str(msg), 5000)  # 在狀態列顯示字串資訊
