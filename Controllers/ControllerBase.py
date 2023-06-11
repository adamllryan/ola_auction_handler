from enum import Enum

from Models.ManagerBase import ManagerBase
from Views.UIBase import UIBase


class ControllerBase:

    controller_name: str
    model: ManagerBase
    view: UIBase

    def __init__(self, name: str, model: ManagerBase, view: UIBase):

        self.controller_name = name
        self.model = model
        self.view = view

        print("Init Controller -> ({name})".format(name=self.controller_name))

    def dispose(self):
        print("Disposing Controller -> ({name})".format(name=self.controller_name))

        if self.model is not None:
            self.model.dispose()
        del self.model
        if self.view is not None:
            self.model.dispose()
        del self.view
        pass

    def input(self, command: Enum, data):
        print("Handling input in Controller -> ({name})".format(name=self.controller_name))
        pass

    def run(self):
        print("Running ({})".format(self.controller_name))
        pass

