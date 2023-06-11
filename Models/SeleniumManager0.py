import os
from collections.abc import Iterable
from datetime import datetime, timedelta
import time

import selenium.webdriver.firefox.webdriver
from attr import dataclass
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
from Models import ManagerBase
from selenium import webdriver
from selenium.webdriver.common.by import By

timeout = 10


@dataclass
class Listing:
    name: str
    url: str
    img_url: list[str]
    end_time: datetime
    last_price: float
    retail_price: float
    condition: str


def try_load_element(driver: selenium.webdriver.firefox.webdriver.WebDriver, xpath: str):

    # Load element with timeout set to x seconds

    element = None
    try:
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
    finally:
        return element if element is not None else None


def try_load_elements(driver: selenium.webdriver.firefox.webdriver.WebDriver, xpath: str):

    # Load element with timeout set to x seconds

    elements = []
    try:
        WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        elements = driver.find_elements(By.XPATH, xpath)
    finally:
        return elements


class SeleniumManager0(ManagerBase.ManagerBase):

    auctions: list[Listing]
    listings: list[Listing]
    filtered_listings: list[Listing]
    my_listings: list[Listing]
    driver: webdriver.firefox.webdriver.WebDriver
    debug: bool
    auction_filters: list[str]
    item_filters: list[str]

    def __init__(self, is_debug: bool):

        # Init ancestor

        super().__init__("WebManager0")

        # Init variables

        self.auctions = []
        self.listings = []
        self.filtered_listings = []
        self.my_listings = []
        self.debug = is_debug
        self.auction_filters = []
        self.item_filters = []

    def create_driver(self):
        print("Creating driver :)")
        self.driver = webdriver.Firefox()

    def get_auctions(self):

        # Base class console output/inheritance

        super().get_auctions()

        # Get url
        if not hasattr(self, 'driver'):
            self.create_driver()

        self.driver.get("https://www.onlineliquidationauction.com/")

        # Grab all auction elements

        auction_elements = try_load_elements(self.driver, './html/body/div[2]/div[5]/div/div[1]/div')
        print("\nFound {num} auctions: ".format(num=len(auction_elements)))

        # Get data into Listing class from each auction

        for i in auction_elements:

            # Grab name

            name = i.find_element(By.XPATH, "./div[2]/h2/a").text
            print(name)

            # Get url and swap domain with bidding page url, keep ID

            bad_url = 'https://www.onlineliquidationauction.com/auctions/detail/bw'
            good_url = 'https://bid.onlineliquidationauction.com/bid/'
            url = i.find_element(By.XPATH, "./div[2]/h2/a").get_attribute("href").replace(bad_url, good_url)
            print(url)

            # Get image src url and save, not really needed

            img_url = [i.find_element(By.XPATH, "./div[1]/div/div/div/div/div/a/img").get_attribute('src')]
            print(img_url)

            # Add to auctions list

            self.auctions.append(Listing(name, url, img_url, None, None, None, None))

        # Cleanup

        print()

    def filter_auctions(self):

        # Base class console output/inheritance

        super().filter_auctions()

        # Iterate through every auction and check for filter terms in name

        remove = []
        for i in self.auctions:
            for j in self.auction_filters:
                if j in i.name:
                    print("\033[91mRemoving {name} from list\033[0m".format(name=i.name))
                    remove.append(i)

        # Remove every item chosen to be removed

        for i in remove:
            if i in self.auctions:
                self.auctions.remove(i)

        print("Keeping {num} auctions. ".format(num=len(self.auctions)))

    def get_items_raw(self, is_my_items: bool):

        # base class console output/inheritance

        super().get_items_raw(is_my_items)

        # For each auction, does not care if filtered or not

        for auction in self.auctions:

            # Get url

            self.driver.get(auction.url)

            # Set page up and scroll until elements are found

            time.sleep(5)
            names = []

            # TODO: fix this, execute_script does not work

            # self.driver.execute_script("document.body.style.zoom='50%'")

            # need to set to active items only, first load use try_load

            select = try_load_element(self.driver, '/html/body/div[3]/div[3]/div/div/div[2]/div[3]/select')
            select.find_element(By.XPATH, './optgroup[2]/option[2]').click()

            # Get number of total items to search for, first load call try_load

            count = int(try_load_element(self.driver, '//*[@id="many-items"]/div[3]/select/optgroup[2]/option[2]').
                        text.replace("All > Active (", "").replace(")", ""))

            if count > 0:

                # Get body element so we can scroll

                try_load_element(self.driver, '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div['
                                                 '2]/item-result/div/div[1]/div/div/div/a')
                body = try_load_element(self.driver, '//*[@id="all-items"]')


                print("There are {count} items.".format(count=count))
                while len(names) < count:

                    # Find current active items

                    live_items = self.driver.find_elements(By.TAG_NAME, 'item-result')

                    for i in live_items:

                        # Get item name text

                        name = try_load_element(i, "./div/div/div/div/div/a").text

                        # If we have not already added this item to our item list

                        if name not in names:

                            # TODO: fill out pricing and end date
                            # Set name

                            # name = name
                            print(name)

                            # Set listing url

                            url = try_load_element(i, "./div/div/div/div/div/a").get_attribute("href")
                            print(url)

                            # Set src image urls

                            img_url = []
                            img_elements = try_load_elements(i, "./div/div[2]/div/owl-carousel/div/div/div/div")
                            for element in img_elements:
                                img_url.append(element.get_attribute('src'))

                            # Set date by splitting formatted date into elements it could be; a unit with 0 left is hidden.

                            date_text = try_load_element(i, './div/div[3]/div/item-status/div/div[1]/div[1]/b/span').text. \
                                split(' ')
                            if 'Ends' in date_text:
                                date_text.remove('Ends')
                                time_left = datetime.now()
                                for segment in date_text:
                                    if 'd' in segment:
                                        time_left += timedelta(days=datetime.strptime(segment, '%dd').day)
                                    elif 'h' in segment:
                                        time_left += timedelta(hours=datetime.strptime(segment, '%Hh').hour)
                                    elif 'm' in segment:
                                        time_left += timedelta(minutes=datetime.strptime(segment, '%Mm').minute)
                                    elif 's' in segment:
                                        time_left += timedelta(seconds=datetime.strptime(segment, '%Ss').second)
                                end_time = time_left
                            else:
                                end_time = datetime.now()
                            print("End Date is {date}".format(date=end_time))

                            # Set last price

                            last_price = float(try_load_element(i, './div/div[3]/div/item-status/div/div[1]/div[2]/b').
                                               text.replace('[$', '').replace(']', ''))
                            print("Last price is {price}".format(price=last_price))

                            # Set retail price and condition text

                            # TODO: FINISH THIS

                            price_condition_text = try_load_element(i, './div/div[2]/div[2]/div').text
                            words = price_condition_text.replace("Retail Price: ", "").split(" ")
                            if 'Unknown' not in words[0]:
                                retail_price = float(words[0].replace(',', '').replace('$', ''))
                            else:
                                retail_price = None
                            condition = ' '.join(words[1::])
                            print("Retail price is {price}".format(price=retail_price))
                            print("Condition is {condition}".format(condition=condition))

                            # Add names to found list

                            self.listings.append(Listing(name, url, img_url, end_time, last_price, retail_price, condition))
                            names.append(name)

                    # Send page down and delay for a bit

                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(.3)
                    print("Found {l_count}/{t_count} listings. ".format(l_count=len(names), t_count=count))
            break

            print("{count} items found. ".format(count=len(names)))

        # Save data to file, so we don't need to reload

        f = open('listings.csv', 'w')
        w = csv.writer(f)
        for row in self.listings:
            w.writerow([row.name, row.url, "*".join(row.img_url), row.end_time.strftime("%m/%d/%Y, %H:%M:%S"),
                        str(row.last_price), str(row.retail_price), row.condition])

    def read_listings(self, f: Iterable[str]):

        # Base class console output/inheritance

        super().read_listings(f)

        if os.path.isfile('listings.csv'):
            f = open('listings.csv', 'r')
            r = csv.reader(f, delimiter=',')
            for row in r:
                self.listings.append(Listing(row[0], row[1], row[2].split("*"),
                                             datetime.strptime(row[3], "%m/%d/%Y, %H:%M:%S"),
                                             float(row[4]), float(row[5]), row[6]))
            f.close()
    def read_my_listings(self, f: Iterable[str]):

        # Base class console output/inheritance

        super().read_my_listings(f)
        if os.path.isfile('mylistings.csv'):
            f = open('mylistings.csv', 'r')
            r = csv.reader(f, delimiter=',')
            for row in r:
                self.listings.append(Listing(row[0], row[1], row[2].split("*"),
                                             datetime.strptime(row[3], "%m/%d/%Y, %H:%M:%S"),
                                             float(row[4]), float(row[5]), row[6]))
            f.close()

    def filter_items(self):

        # Base class console output/inheritance

        super().filter_items()

        # Find each listing that matches a keyword

        remove = []
        for i in self.listings:
            for j in self.item_filters:
                if j.lower() in i.name.lower():
                    print("\033[91mRemoving {name} from list\033[0m".format(name=i.name))
                    remove.append(i)

        # Remove items that match keywords

        self.filtered_listings = self.listings.copy()
        for i in remove:
            if i in self.filtered_listings:
                self.filtered_listings.remove(i)
        print("Keeping {num} listings. ".format(num=len(self.listings)))

    def refresh(self):

        # Base class console output/inheritance

        super().refresh()

        self.get_auctions()
        self.filter_auctions()
        self.get_items_raw(False)
        self.filter_items()



    def refresh_my(self):

        # Base class console output/inheritance

        super().refresh_my()





    def close_driver(self):
        if self.driver is not None:
            self.driver.close()
