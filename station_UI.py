import TestSupport
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *
from PyQt5.QtQml import *
from PyQt5.QtGui import *
from ui.images.images import *
from MapData import *
import sys,os
from win32api import GetSystemMetrics
from Utils import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("TEST")
        self.menuBar = QMenuBar(self)
        self.menuBar.setStyleSheet("background-color: white;")
        self.menuBar.setObjectName("menuBar")

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.mainToolBar = QToolBar(self)
        self.mainToolBar.setWindowTitle("菜单栏")
        self.addToolBar(self.mainToolBar)
        self.createMainWindowMenu(menuBarList)

        # 创建centralWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet("background-color: black;")
        self.setCentralWidget(self.centralWidget)
        qmlRegisterType(Utils,"an.qt.Utils", 1, 0, "Utils");
        view = QQuickView();
        view.rootContext().setContextProperty("ate_mianWindow", self);
        view.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'ui/main.qml')))

        viewWidget = QWidget.createWindowContainer(view,self.centralWidget)
        layout_view = QVBoxLayout(self.centralWidget)
        layout_view.addWidget(viewWidget)

    @pyqtSlot(Utils)
    def mapReady(self,util):
        self.utils = util
        self.utils.qmlInitReady()

    # 遍历创建菜单栏
    def createMainWindowMenu(self, menuList):
        for k in menuList:
            self.menu = QMenu(self.menuBar)
            self.menu.setStyleSheet(
                "QMenu{background-color:white;color:black;}QMenu::item:selected{background-color:#CCDAE7;}")
            self.menu.setObjectName(k)
            self.setMenuBar(self.menuBar)
            self.menu.setTitle(k)
            for h in range(len(menuList[k])):
                self.action = QAction(self.menu)
                self.action.setObjectName(str(menuList[k][h]))
                self.menu.addAction(self.action)
                self.action.setText(str(menuList[k][h]))
                self.action.triggered.connect(self.windowMenuClick)
            self.menuBar.addAction(self.menu.menuAction())

    #菜单栏槽函数
    def windowMenuClick(self):
        sender_parent = self.sender().parent().objectName()
        sender = self.sender().objectName()
        print(sender_parent,sender)

def init_station_map_ga():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.setMinimumSize(GetSystemMetrics(0)/2, GetSystemMetrics(1)/2)
    ui.showMaximized();
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    init_station_map_ga()