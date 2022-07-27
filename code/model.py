from PyQt5 import QtCore
import cv2
import numpy as np
import time
import os

import modbus_tk.defines as cst

from glob  import glob
from recognition import recognize
from PIL import Image
import pdb
import torch
import asyncio

class Camera(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 Camera 類別
    rawdata = QtCore.pyqtSignal(np.ndarray)  # 建立傳遞信號，需設定傳遞型態為 np.ndarray

    def __init__(self, bright, parent=None, multicam=0):
        """ 初始化
            - 執行 QtCore.QThread 的初始化
            - 建立 cv2 的 VideoCapture 物件
            - 設定屬性來確認狀態
              - self.connect：連接狀態
              - self.running：讀取狀態
        """
        # 將父類初始化
        super().__init__(parent)
        # 建立 cv2 的攝影機物件
        self.multicam = multicam
        # self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam = cv2.VideoCapture(self.multicam, cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        # 判斷攝影機是否正常連接
        if self.cam is None or not self.cam.isOpened():
            self.connect = False
            self.running = False
        else:
            self.connect = True
            self.running = False

    def run(self):
        # 當正常連接攝影機才能進入迴圈
        while self.running and self.connect:
            ret, img = self.cam.read()    # 讀取影像
            if ret:
                img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                self.rawdata.emit(img_rgb)    # 發送影像
            else:    # 例外處理
                print("Warning!!!")
                print(self.cam.read())
                self.cam = cv2.VideoCapture(self.multicam)
                self.connect = False
            time.sleep(0.01)
    
    def save(self,camera_index):
        images = 'images'
        directory_path = os.path.join('.', images, camera_index)
        is_exist = os.path.exists(directory_path)
        if not is_exist:
            os.makedirs(directory_path)
        tim = time.localtime()
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S", tim)
        time_png = str(current_time) + '.png'
        print('save png name: ', os.path.join('.', images, camera_index, time_png))
        if self.running and self.connect:
            ret, img = self.cam.read()
            if ret:
                img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                cv2.imwrite(str(os.path.join('.', images, camera_index, time_png)), img)
                self.rawdata.emit(img_rgb)    # 發送影像
                return os.path.join('.', images, camera_index, time_png)
            else:    # 例外處理
                print("Warning: Image is not Captured")
                self.cam = cv2.VideoCapture(self.multicam)
                return ''
                pass

    def open(self):
        """ 開啟攝影機影像讀取功能 """
        if self.connect:
            self.running = True    # 啟動讀取狀態

    def stop(self):
        """ 暫停攝影機影像讀取功能 """
        if self.connect:
            self.running = False    # 關閉讀取狀態

    def close(self):
        """ 關閉攝影機功能 """
        if self.connect:
            self.running = False    # 關閉讀取狀態
            time.sleep(1)
            self.cam.release()      # 釋放攝影機

class ReadModbus(QtCore.QThread):
    plcstatus = QtCore.pyqtSignal(list)

    def __init__(self, slave_id,modbus_handler, message, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.handler = modbus_handler
        self.slave = slave_id
        self.running = False
        self.message = message

    def run(self):
        while self.running:
            try:
                read = self.handler.execute(self.slave, cst.READ_COILS, 50, 16)  # 取像1站:50 2站:51,取像完成1站:52 2站:53, 
                tmp2 = self.handler.execute(self.slave, cst.READ_INPUT_REGISTERS, 0, 2)
                self.plcstatus.emit(list(read))
                msg = '警報內容: '
                if tmp2[0] == 0:
                    msg += '無警報,    '
                elif tmp2[0] == 1:
                    msg += '出料卡料,    '
                elif tmp2[0] == 2:
                    msg += '分料氣缸錯誤,    '
                elif tmp2[0] == 3:
                    msg += '第一站未偵測到芒果,    '
                elif tmp2[0] == 4:
                    msg += '第二站未偵測到芒果,    '
                elif tmp2[0] == 5:
                    msg += '安全門未關,    '
                msg += '機台狀態: '
                if tmp2[1] == 1:
                    msg += '請復歸'
                elif tmp2[1] == 2:
                    msg += '復歸中'
                elif tmp2[1] == 3:
                    msg += '待命中'
                elif tmp2[1] == 4:
                    msg += '啟動中'
                elif tmp2[1] == 5:
                    msg += '暫停中'
                elif tmp2[1] == 6:
                    msg += '急停中'
                elif tmp2[1] == 10:
                    msg += '警報中'
                print(msg)
                self.message(msg)
                time.sleep(0.5)
            except Exception as exc:
                print('ReadModbus Error: ', exc)

    def open(self):
        if self.handler:
            self.running = True

    def stop(self):
        self.running = False

class AutoRun(QtCore.QThread):
    def __init__(self, slave_id, modbus_handler,cam1 ,cam2, cam3, cam4, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.handler = modbus_handler
        self.slave = slave_id
        self.cam1 = cam1
        self.cam2 = cam2
        self.cam3 = cam3
        self.cam4 = cam4
        self.running = False
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
    def multi_batch_inference(self, img_path_1, img_path_2):
        r = recognize.Recognize_multi(
                model_path='recognition/model_pack_v3_1619986187.pth', device=self.device,
                async_run=False, 
                verbose=True)
        imgs_file_path_list = [img_path_1, img_path_2]
        imgs_list = []
        for imgs_file_path in imgs_file_path_list:
            if '.png' in imgs_file_path: # four channels to three channels
                input_img = Image.open(imgs_file_path)
                input_img_arr = np.array(input_img)
                input_img_arr = input_img_arr[:, :, :3]
                input_img = Image.fromarray(input_img_arr)
            else:
                input_img = Image.open(imgs_file_path)
            imgs_list.append(input_img)
            
        result_nums_list = r(imgs_list[:])[0]
        
        print(imgs_file_path_list)
        print(result_nums_list)
        
        if 2 in result_nums_list:
            return 'NG'
        else:
            return 'OK'

    def run(self):
        while self.running:
            try:
                read = self.handler.execute(self.slave, cst.READ_COILS, 50, 16)  # 取像1站:50 2站:51,取像完成1站:52 2站:53
                print('Auto Thread in Running: ', read)
                if read[0] and read[10]:
                    self.handler.execute(self.slave, cst.WRITE_SINGLE_COIL, 50, output_value=0)
                    img_path1 = self.cam1.save(camera_index='cam1')
                    img_path2 = self.cam2.save(camera_index='cam2')
                    self.handler.execute(self.slave, cst.WRITE_SINGLE_COIL, 52, output_value=1)
                    
                    OK_or_NG = self.multi_batch_inference(img_path1, img_path2) # do model inference
                    if OK_or_NG == 'OK':
                        # 寫1在81 reg
                        self.handler.execute(self.slave, cst.WRITE_SINGLE_REGISTER, starting_address=81, output_value=1)
                    else:
                        # 寫2在81 reg
                        self.handler.execute(self.slave, cst.WRITE_SINGLE_REGISTER, starting_address=81, output_value=2)
                    
                if read[1] and read[10]:
                    self.handler.execute(self.slave, cst.WRITE_SINGLE_COIL, 51, output_value=0)
                    img_path3 = self.cam3.save(camera_index='cam3')
                    img_path4 = self.cam4.save(camera_index='cam4')
                    self.handler.execute(self.slave, cst.WRITE_SINGLE_COIL, 53, output_value=1)
                    
                    if OK_or_NG == 'OK':
                        OK_or_NG = self.multi_batch_inference(img_path3, img_path4) # do model inference
                        if OK_or_NG == 'OK':
                            # 寫1在82 reg
                            self.handler.execute(self.slave, cst.WRITE_SINGLE_REGISTER, starting_address=82, output_value=1)
                        else:
                            # 寫2在82 reg
                            self.handler.execute(self.slave, cst.WRITE_SINGLE_REGISTER, starting_address=82, output_value=2)
                    else:
                        # 寫2在82 reg
                        self.handler.execute(self.slave, cst.WRITE_SINGLE_REGISTER, starting_address=82, output_value=2)
                else:
                    pass
                
                time.sleep(1)
            except Exception as exc:
                print('AutoRun Error: ', exc)

    def open(self):
        if self.handler:
            self.running = True

    def stop(self):
        self.running = False

class ManRun(QtCore.QThread):

    def __init__(self, slave_id,modbus_handler, autobtn, manbtn, savebtn, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.handler = modbus_handler
        self.slave = slave_id
        self.autobtn = autobtn
        self.manbtn = manbtn
        self.savebtn = savebtn
        self.running = False

    def run(self):
        while self.running:
            try:
                finish = self.handler.execute(self.slave, cst.READ_COILS, 64, 1)
                if finish:
                    self.autobtn.setEnabled(True)
                    self.manbtn.setEnabled(True)
                    self.savebtn.setEnabled(True)
                    finish = self.handler.execute(self.slave, cst.WRITE_SINGLE_COIL, 64, output_value=0)
                time.sleep(0.1)
            except Exception as exc:
                print('ManRun Error: ', exc)

    def open(self):
        if self.handler:
            self.running = True

    def stop(self):
        self.running = False