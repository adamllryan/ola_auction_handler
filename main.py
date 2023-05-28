import os

import DesktopUI0
import ManagerBase
import WebManager0
import UIBase
import time


def main():
    # use MVC design pattern
    model: ManagerBase = WebManager0.WebManager0()
    view: UIBase = DesktopUI0.DesktopUI0()

    model.get_auctions()
    model.filter_auctions(["Brookpark Rd", "N Royalton"])

    if os.path.isfile('listings'):
        model.load_from_file()
    else:
        model.get_items_raw()

    time.sleep(5)

    model.dispose()
    view.dispose()


main()
