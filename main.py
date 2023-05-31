import os

from Views import DesktopUI0, UIBase
from Models import SeleniumManager0, ManagerBase
import time


def main():

    # use MVC design pattern

    model: ManagerBase = SeleniumManager0.SeleniumManager0(False)
    view: UIBase = DesktopUI0.DesktopUI0()

    # Test determine if we should load new data

    reload = False
    if os.path.isfile('listings.csv') and not reload:
        f = open('listings.csv', "r")
        model.load_from_file(f)
        f.close()
    else:
        print(type(model))
        if isinstance(model, SeleniumManager0.SeleniumManager0):
            model.create_driver()
        model.get_auctions()
        model.filter_auctions(["Brookpark Rd", "N Royalton"])
        model.get_items_raw(False)
        if isinstance(model, SeleniumManager0.SeleniumManager0):
            model.close_driver()

    # Data filtering

    model.filter_items(['kid', 'men', 'women', 'shelf', 'artwork', 'scratch', 'cat', 'shoe', 'shelv', 'gaming chair', 'desk', 'table', 'costume', 'baby'])
    time.sleep(5)

    # Cleanup

    model.dispose()
    view.dispose()


main()
