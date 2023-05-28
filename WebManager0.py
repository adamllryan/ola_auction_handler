import time

from attr import dataclass
from selenium.webdriver import Keys

import ManagerBase
from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass
class Listing:
    name: str
    url: str
    img_url: list[str]


class WebManager0(ManagerBase.ManagerBase):

    def __init__(self):
        self.manager_name = "WebManager0"
        super().__init__()
        self.auctions = []
        self.listings = []
        self.driver = webdriver.Firefox()

    def dispose(self):
        super().dispose()
        self.driver.close()

    def get_auctions(self):
        super().get_auctions()
        self.driver.get("https://www.onlineliquidationauction.com/")
        # row blog margin-bottom-40 //*[@id="main-content-top"]/div/div[1]/div[1]
        auction_elements = self.driver.find_elements(By.XPATH, './html/body/div[2]/div[5]/div/div[1]/div')
        print("\nFound {num} auctions: ".format(num=len(auction_elements)))
        for i in auction_elements:
            listing: Listing = Listing("", "", [])
            listing.name = i.find_element(By.XPATH, "./div[2]/h2/a").text
            print(listing.name)
            bad_url = 'https://www.onlineliquidationauction.com/auctions/detail/bw'
            good_url = 'https://bid.onlineliquidationauction.com/bid/'
            listing.url = i.find_element(By.XPATH, "./div[2]/h2/a").get_attribute("href").replace(bad_url, good_url)
            print(listing.url)
            listing.img_url = [i.find_element(By.XPATH, "./div[1]/div/div/div/div/div/a/img").get_attribute('src')]
            print(listing.img_url)
            self.auctions.append(listing)
        print()

    def filter_auctions(self, auctions_to_remove: list[str]):
        super().filter_auctions(auctions_to_remove)
        new = []
        for i in self.auctions:
            for j in auctions_to_remove:
                print("Checking for '{loc}' in ({auction})".format(loc=j, auction=i.name))
                if j not in i.name:
                    new.append(i)
                else:
                    print("\033[91mRemoving {name} from list\033[0m".format(name=i.name))
        self.auctions = new
        print(len(self.auctions))

    def get_items_raw(self):
        super().get_items_raw()
        # TODO: add boolean value check to click on Your Items when sign in is implemented
        for auction in self.auctions:
            auction_driver = webdriver.Firefox()
            auction_driver.get(auction.url)
            # TODO: replace with webdriver wait
            time.sleep(5)
            count = int(
                auction_driver.find_element(By.XPATH, '//*[@id="many-items"]/div[3]/select/option').text.replace(
                    "Select Category... (", "").replace(" items total)", ""))
            body = auction_driver.find_element(By.XPATH, '//*[@id="all-items"]')
            names = []
            auction_driver.execute_script("document.body.style.zoom='50%'")
            while len(names) < count:
                print(len(names))
                live_items = auction_driver.find_elements(By.TAG_NAME, 'item-result')
                for i in live_items:
                    name = i.find_element(By.XPATH, "./div/div/div/div/div/a").text
                    if name not in names:
                        listing: Listing = Listing("", "", [])
                        listing.name = name
                        print(listing.name)
                        listing.url = i.find_element(By.XPATH, "./div/div/div/div/div/a").get_attribute("href")
                        print(listing.url)
                        img_elements = i.find_elements(By.XPATH, "./div/div[2]/div/owl-carousel/div/div/div/div")
                        for element in img_elements:
                            listing.img_url.append(element.get_attribute('src'))
                        self.listings.append(listing)
                        names.append(name)
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(.2)
                print("There are {count} total listings. ".format(count=len(self.listings)))
            print("{count} items found. ".format(count=len(names)))
            auction_driver.close()
            break

    def filter_items(self):
        super().filter_items()

    def refresh_items(self):
        super().refresh_items()
