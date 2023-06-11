from Controllers.Controller0 import Commands, Controller0
from Views import DesktopUI


class DesktopUI0(DesktopUI.DesktopUI):

    def __init__(self):
        super().__init__("DesktopCLI")

    def add_item(self, data: str):
        super().add_item(data)

    def remove_item(self, data: str):
        super().add_item(data)




