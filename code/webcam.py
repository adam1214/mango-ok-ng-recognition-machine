import sys
from PyQt5 import QtWidgets
from modelview import MainWindow
# from Ui_main import Ui_MainWindow

import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'


if __name__=='__main__':
    # 這個蠻複雜的，簡單講建立一個應用程式都需要它
    # 然後將 sys.argv 這個參數引入進去之後
    # 就能執行最後一行的 sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    #建立視窗程式的物件
    win = MainWindow()
    # 顯示視窗
    win.show()
    # 離開程式
    sys.exit(app.exec_())