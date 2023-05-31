from PySide6.QtCore import QTimer

import DesktopUI
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QLabel, QWidget
import sys
import time


class MainWindow(QMainWindow):
    class MainWindow(QMainWindow):

        def __init__(self):
            super(MainWindow, self).__init__()

            self.counter = 0

            layout = QVBoxLayout()

            self.l = QLabel("Start")
            b = QPushButton("DANGER!")
            b.pressed.connect(self.oh_no)

            layout.addWidget(self.l)
            layout.addWidget(b)

            w = QWidget()
            w.setLayout(layout)

            self.setCentralWidget(w)

            self.show()

            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.recurring_timer)
            self.timer.start()

        def oh_no(self):
            time.sleep(5)

        def recurring_timer(self):
            self.counter += 1
            self.l.setText("Counter: %d" % self.counter)


class DesktopUI1(DesktopUI.DesktopUI):

    def __init__(self):
        print("init DesktopUI1")
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.app.exec_()

    def dispose(self):
        print("dispose DesktopUI1")
        self.window.close
        pass

    def add_item(self, data: str):
        print("add item" + self)
        pass

    def remove_item(self, data: str):
        pass
