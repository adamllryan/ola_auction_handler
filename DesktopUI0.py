import DesktopUI
import sys
import time


class DesktopUI0(DesktopUI.DesktopUI):

    def __init__(self):
        self.ui_name = "DesktopUI0 - CLI"
        super().__init__()

    def dispose(self):
        super().dispose()

    def add_item(self, data: str):
        super().add_item(data)

    def remove_item(self, data: str):
        super().add_item(data)

