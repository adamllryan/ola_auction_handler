import os

import DesktopUI0
import ManagerBase
import SeleniumManager0
import UIBase
import time


def main():

    # use MVC design pattern

    model: ManagerBase = SeleniumManager0.SeleniumManager0(False)
    view: UIBase = DesktopUI0.DesktopUI0()

    # Test determine if we should load new data

    reload = False
    if os.path.isfile('listings.csv') and not reload:
        model.load_from_file()
    else:
        model.get_auctions()
        model.filter_auctions(["Brookpark Rd", "N Royalton"])
        model.get_items_raw(False)
        if model is SeleniumManager0:
            model.close_driver()

    # Data filtering

    model.filter_items(['kid', 'men', 'women', 'shelf', 'artwork', 'scratch', 'cat', 'shoe', 'shelv', 'gaming chair', 'desk', 'table', 'costume', 'baby'])
    time.sleep(5)

    # Cleanup

    model.dispose()
    view.dispose()


main()
