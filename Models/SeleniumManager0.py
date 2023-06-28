import os
import pickle
from datetime import datetime, timedelta
import time
import webbrowser
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from attr import dataclass
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.by import By

timeout = 5
REPEAT_INITIAL_VALUE = 10


@dataclass
class Item:
    name: str
    url: str
    img_url: list[str]
    end_time: datetime
    last_price: float
    retail_price: float
    condition: str


@dataclass
class Auction:
    name: str
    url: str
    src: list[str]
    items: list[Item]


class URLS:
    # auction

    site: str = "https://www.onlineliquidationauction.com/"
    auctions: str = '/html/body/div[2]/div[5]/div/div[1]/div'
    auction_name: str = '/html/body/div[2]/div[5]/div/div[1]/div[1]/div[2]/h2/a'
    auction_url: str = '/html/body/div[2]/div[5]/div/div[1]/div[1]/div[2]/h2/a'
    auction_img: str = '/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div/div[1]/div/div[1]/div/a/img'

    # item

    select: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[3]/select'
    active_item: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[3]/select/optgroup[2]/option[2]'
    count: str = '//*[@id="many-items"]/div[3]/select/optgroup[2]/option[2]'
    first_item: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[1]/div/div/div/a'
    body: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div'
    items: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div'
    name: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[1]/div/div/div/a'
    listing_url: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[1]/div/div/div/a'
    img_elements: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[2]/div[1]/owl-carousel/div[1]/div/div[1]'
    img_src: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[2]/div[1]/owl-carousel/div[1]/div/div[1]/div/img'
    date: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[3]/div/item-status/div/div[1]/div[1]/b/span'
    last_price: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[3]/div/item-status/div/div[1]/div[2]/b'
    price_condition: str = '/html/body/div[3]/div[3]/div/div/div[2]/div[4]/div/div[2]/item-result/div/div[2]/div[2]/div'

    def subpath(src: str, dest: str):
        rel_path = dest.replace(src, '')
        if rel_path[0] == '[':
            rel_path = rel_path[rel_path.index(']')+1:]
        return '.' + rel_path


def try_load_element(driver: WebDriver, xpath: str):

    # Load element with timeout set to x seconds

    element = None

    try:
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    finally:

        return element if element is not None else None


def try_load_elements(driver: WebDriver, xpath: str):

    # Load element with timeout set to x seconds

    elements = []
    try:
        WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        elements = driver.find_elements(By.XPATH, xpath)

    finally:

        return elements


class SeleniumScraper:

    auctions: list[Auction]
    new_auctions: list[Auction]
    filter_items: list[Item]
    driver: webdriver.firefox.webdriver.WebDriver
    auction_filters: list[str]
    item_filters: list[str]
    loud: bool
    debug: bool

    def __init__(self, auctions: list[str], filters: list[str], open_in_browser, debug):

        # Init variables

        self.auctions = []
        self.new_auctions = []
        self.auction_filters = auctions
        self.item_filters = filters
        self.loud = open_in_browser
        self.debug = debug
        self.filter_items = []

    def create_driver(self):

        options = FirefoxOptions()

        if not self.debug:
            options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=options)

    def find_auctions(self):

        # Get url

        if not hasattr(self, 'driver'):
            self.create_driver()

        self.driver.get("https://www.onlineliquidationauction.com/")

        # Grab all auction elements

        auction_elements = try_load_elements(self.driver, URLS.subpath('', URLS.auctions))
        # print("\nFound {num} auctions: ".format(num=len(auction_elements)))

        # Get data into Listing class from each auction

        for i in auction_elements:

            # Grab name
            name = i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_name)).text

            # Get url and swap domain with bidding page url, keep ID

            bad_url = 'https://www.onlineliquidationauction.com/auctions/detail/bw'
            good_url = 'https://bid.onlineliquidationauction.com/bid/'

            url = i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_name)).get_attribute("href") \
                .replace(bad_url, good_url)

            # Get image src url and save, not really needed

            img_url = [i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_img)).get_attribute('src')]

            # Add to auctions list

            pass_auction_filter = False
            for keyword in self.auction_filters:
                if keyword in name:
                    pass_auction_filter = True
            if pass_auction_filter:
                is_new_auction = True
                for auction in self.auctions:
                    if auction.name is name:
                        is_new_auction = False
                if is_new_auction:
                    self.new_auctions.append(Auction(name, url, img_url, []))

    def find_items(self, auctions: list[Auction]):

        # For each auction

        for auction in auctions:

            self.get_auction_items(auction)

    def get_auction_items(self, auction: Auction):

        # Get url

        self.driver.get(auction.url)

        # Set page up and scroll until elements are found

        time.sleep(5)
        names = []

        # TODO: fix this, execute_script does not work

        # self.driver.set_context("chrome")
        #
        # for i in range(1, 10):
        #     self.driver.send_keys(Keys.CONTROL, '-')
        #     self.driver.
        # self.driver.set_context('content')
        # self.driver.execute_script("document.body.style.zoom='50%'")

        # need to set to active items only, first load use try_load

        select = try_load_element(self.driver, URLS.select)
        select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).click()

        # Get number of total items to search for, first load call try_load

        count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))

        if count > 0:

            # Get body element so we can scroll

            try_load_element(self.driver, URLS.first_item)
            body = try_load_element(self.driver, URLS.body)

            # print("There are {count} items.".format(count=count))

            # set repeat counter, so we exit if an item is missed but never accounted for

            repeat_counter = REPEAT_INITIAL_VALUE

            while len(names) < count and repeat_counter > 0:

                # Find current active items

                live_items = self.driver.find_elements(By.XPATH, '//*[@id="all-items"]/div')
                live_items.pop()
                for i in live_items:

                    # Get item name text
                    end_text = try_load_element(self.driver, URLS.date)
                    if end_text is not None:
                        try:
                            end_text = end_text.text
                        except:
                            continue
                    else:
                        continue
                    for phrase in ['Extending', 'Closing', 'SOLD']:
                        if phrase in end_text:
                            continue

                    item = self.get_item_details(i, names)

                    if item is not None:
                        repeat_counter = REPEAT_INITIAL_VALUE
                        auction.items.append(item)
                        names.append(item.name)

                # Send page down and delay for a bit

                try:
                    body.send_keys(Keys.PAGE_DOWN)
                except:
                    break

                repeat_counter -= 1

                time.sleep(.3)
                # print("Found {l_count}/{t_count} listings. ".format(l_count=len(names), t_count=count))

        # print("{count} items found. ".format(count=len(names)))

    def get_item_details(self, item: WebDriver, names: []):

        try:
            name = item.find_element(By.XPATH, URLS.subpath(URLS.items, URLS.name))
        except:
            return None

        name = name.text

        # If we have not already added this item to our item list

        if name not in names:

            # TODO: fill out pricing and end date
            # Set name

            # name = name
            print(name)

            # Set listing url

            url = try_load_element(item, URLS.subpath(URLS.items, URLS.listing_url))
            if url is not None:
                try:
                    url = url.get_attribute("href")
                except:
                    return None
            else:
                return None
            # print(url)

            # Set src image urls

            img_url = []
            img_elements = try_load_elements(item, URLS.subpath(URLS.items, URLS.img_elements))
            for element in img_elements:
                img_url.append(try_load_element(element, URLS.subpath(URLS.img_elements,
                                                                      URLS.img_src)).get_attribute('owl-data-src'))
                # print(img_url[-1])

            # Set date by splitting formatted date into elements it could be; a unit with 0 left is hidden.

            end_time = None
            date_text = try_load_element(item, URLS.subpath(URLS.items, URLS.date))
            if date_text is not None:
                date_text = date_text.text.split(' ')

                if 'Ends' in date_text:
                    date_text.remove('Ends')
                    time_left = datetime.now()
                    for segment in date_text:
                        if 'd' in segment:
                            time_left += timedelta(days=int(segment.replace('d', '')))
                        elif 'h' in segment:
                            time_left += timedelta(hours=datetime.strptime(segment, '%Hh').hour)
                        elif 'm' in segment:
                            time_left += timedelta(minutes=datetime.strptime(segment, '%Mm').minute)
                        elif 's' in segment:
                            time_left += timedelta(seconds=datetime.strptime(segment, '%Ss').second)
                    end_time = time_left
                else:
                    end_time = datetime.now()
                # print("End Date is {date}".format(date=end_time))
            else:
                return None
            # Set last price

            last_price = try_load_element(item, URLS.subpath(URLS.items, URLS.last_price))
            if last_price is not None:
                try:
                    last_price = float(last_price.text.replace('[$', '').replace(']', ''))
                except:
                    return None
            else:
                return None
            # print("Last price is {price}".format(price=last_price))

            # Set retail price and condition text

            # TODO: FINISH THIS

            condition = ''
            retail_price = 0
            price_condition_text = try_load_element(item, URLS.subpath(URLS.items, URLS.price_condition))
            if price_condition_text is not None:
                try:
                    price_condition_text = price_condition_text.text
                except:
                    return None

                words = price_condition_text.replace("Retail Price: ", "").split(" ")
                if 'Unknown' not in words[0] and words[0] != '':
                    retail_price = float(words[0].replace(',', '').replace('$', ''))
                else:
                    retail_price = -1
                condition = ' '.join(words[1::])
                # print("Retail price is {price}".format(price=retail_price))
                # print("Condition is {condition}".format(condition=condition))
            else:
                return None
            # Add names to found list

            listing = Item(name, url, img_url, end_time, last_price, retail_price, condition)

            for i in self.item_filters:
                if i.lower() in name.lower():
                    self.filter_items.append(listing)
                    return listing
            return listing
        return None

    def clean_auctions(self):
        for auction in self.auctions:
            current = datetime.now()
            for item in auction.items:
                if current > item.end_time:
                    auction.items -= item
            if auction.items.count == 0:
                self.auctions -= auction

    def notify(self):
        for i in self.filter_items:
            if self.loud:
                webbrowser.open(i.url)
            print("{name} - {url}".format(name=i.name, url=i.url))

    def import_(self):
        if os.path.isfile("data"):
            with open('data', 'rb') as f:
                self.auctions = pickle.load(f)

    def export_(self):
        with open('data', 'wb') as f:
            pickle.dump(self.auctions, f)

    def close_driver(self):
        if self.driver is not None:
            self.driver.close()


auction_filters = input("Add auction locations, separated by ';' (eg. 'Brookpark;Stow'): ").split(';')
item_filters = input("Add items to look for, same format ('item;item;item'): ").split(';')
show_browser = input("Show browser? (yes): ") == 'yes'
loud = input("Open matches in browser? (yes): ") == 'yes'
scraper = SeleniumScraper(auction_filters, item_filters, loud, show_browser)
scraper.create_driver()
scraper.import_()
while True:
    # print("Finding Auctions...")
    scraper.find_auctions()
    # print("Cleaning Up old Auctions...")
    scraper.clean_auctions()
    # print("Collecting auction items...")
    scraper.find_items(scraper.new_auctions)
    scraper.export_()
    scraper.notify()
    # print("Sleeping...")
    time.sleep(3600)
