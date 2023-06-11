import os

from Views import DesktopUI0, UIBase
from Models import SeleniumManager0, ManagerBase
from Controllers import Controller0, ControllerBase
import time


def main():

    # use MVC design pattern
    view: UIBase = DesktopUI0.DesktopUI0()
    model: ManagerBase = SeleniumManager0.SeleniumManager0(False)
    controller: ControllerBase = Controller0.Controller0(model, view)
    controller.run()

    del controller


main()

