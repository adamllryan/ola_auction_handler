import os
from datetime import datetime, timedelta
import pickle
import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from attr import dataclass
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread, Event

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


class SeleniumScraper(Thread):

    logged_auctions: list[str]
    auctions: list[Auction]
    driver: webdriver.firefox.webdriver.WebDriver
    debug: bool
    running: bool
    progress: list[int]
    total_items: list[int]
    reload_called: Event # Use this to call reload
    callback: Event # Use this to call back after load
    state: list

    def __init__(self, auctions: list[str], debug: bool):
        Thread.__init__(self)

        self.logged_auctions = auctions # Set vars to initial values
        self.auctions = []
        self.debug = debug
        self.running = False
        self.state = ['Idle - Waiting']
        self.progress = []
        self.total_items = []
        self.reload_called = Event()
        self.callback = Event()

    def create_driver(self):
        self.state.append('Creating Driver')
        options = FirefoxOptions()

        if not self.debug:
            options.add_argument("--headless")

        self.state.pop()

        return webdriver.Firefox(options=options)




    def find_auctions(self):

        self.state.append('Finding Auctions')

        # Get url

        driver = self.create_driver()

        driver.get("https://www.onlineliquidationauction.com/")

        # Grab all auction elements

        auction_elements = try_load_elements(driver, URLS.subpath('', URLS.auctions))

        # Get data into Listing class from each auction

        self.state.append('Getting Auction Data')

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

            pass_auction_filter = True
            for keyword in self.logged_auctions:
                if keyword in name:
                    pass_auction_filter = False
            if pass_auction_filter:
                is_new_auction = True
                for auction in self.auctions:
                    if auction.name == name:

                        is_new_auction = False
                if is_new_auction:
                    self.auctions.append(Auction(name, url, img_url, []))

        driver.close()

        self.state.pop()
        self.state.pop()

    def find_items(self):

        self.state.append('Creating Item Search Threads and Waiting for Completion')

        threads = []
        id = 0
        for auction in self.auctions:
            self.progress.append(0)
            self.total_items.append(0)
            thread = Thread(target=self.get_auction_items, args=(auction,id))
            thread.start()
            threads.append(thread)
            self.logged_auctions.append(auction.name)
            id += 1

        for thread in threads:
            thread.join()

        self.state.pop()

    def parse_description(self, data: str):
        retail: float
        condition: str
        words = data.replace("Retail Price: ", "").split(" ")
        if 'Unknown' not in words[0] and words[0] != '':
            retail = float(words[0].replace(',', '').replace('$', ''))
        else:
            retail = -1
        condition = ' '.join(words[1::])
        return retail, condition

    def all_items_loaded(self, driver, count, id):
        current_size = int(driver.execute_script('return bwAppState.auction.all_items.items.length'))
        self.progress[id] = current_size
        # print(f"Found {current_size}/{count} items. ")
        return count <= current_size

    def get_auction_items(self, auction: Auction, id: int):

        # Get url

        driver = self.create_driver()

        driver.get(auction.url)

        # Set page up and scroll until elements are found

        time.sleep(5)
        names = []

        # need to set to active items only, first load use try_load

        select = try_load_element(driver, URLS.select)
        # select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).click()

        # Get number of total items to search for, first load call try_load

        count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))
        self.total_items[id] = count
        if count >= 50:
            driver.execute_script('bwAppState.auction.all_items.api_args.per_page=1500;')
            retries = 30
            time.sleep(5)
            while not self.all_items_loaded(driver, count, id) and retries > 0:
                count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))
                self.total_items[id] = count
                driver.execute_script('bwAppState.auction.all_items.fetch_more_items();')
                retries-=1
                time.sleep(1)
        
        data = driver.execute_script('return Array.from(bwAppState.auction.all_items.items).map(item => [item.name, item.id, item.company.logo_url, item.actual_end_time, item.maxbid.amount, item.simple_description])')
        for item in data:
            name = item[0]
            url = 'https://bid.onlineliquidationauction.com/bid/' + str(item[1])
            img = item[2]
            end = datetime.strptime(item[3], "%Y-%m-%dT%H:%M:%S.000Z")
            max = item[4]
            retail, condition = self.parse_description(item[5])
            item = Item(name, url, img, end, max, retail, condition)
            auction.items.append(item)
        driver.close()

    def clean_auctions(self):
        
        self.state.append('Cleaning Auctions')

        for auction in self.auctions:
            current = datetime.now()
            auction.items = list(filter(lambda x: current > x.end_time, auction.items))
        self.auctions = list(filter(lambda x: len(x.items)>0, self.auctions))

        self.state.pop()

    def export_(self):

        self.state.append('Exporting Data')

        items = []
        for auction in self.auctions:
            for x in auction.items:
                items.append([auction.name, x.name, x.url, x.img_url[0], x.last_price, x.retail_price, x.condition, x.end_time])
        self.auctions.clear()

        self.state.pop()

        return items
        

    def run(self):
        while True:
            flag = self.reload_called.wait(3600)
            if flag:
                print("Refresh Called")
            else:
                print("Auto-refresh triggered")
            self.state.pop()
            print('running __find_auctions__')
            
            # for i in range(1,100):
            #     auction = Auction(f"auction{i}", "", [""], [])
            #     for j in range(1,100):
            #         item = Item(f"item{j}", "url", ["src"], datetime.now(), 0, 0, "New")
            #         auction.items.append(item)
            #     # print(len(auction.items))
            #     self.auctions.append(auction)

            # self.callback.set()
            # self.reload_called.clear()
            # continue
           
           
           
            # self.auctions.clear()
            self.find_auctions()
            print('running __find_items__')
            self.find_items()
            # print('running __clean_auctions__')
            # self.clean_auctions()
            #1 min cooldown for refresh
            self.callback.set()
            self.state.append('Idle - Cooldown')
            time.sleep(60)
            self.reload_called.clear()
            self.state[0] = ('Idle - Waiting')

    
    def close_driver(self):
        if self.driver is not None:
            self.driver.close()
    
    def get_progress(self):
        sum1 = sum(self.progress)
        sum2 = sum(self.total_items)
        if sum2 == 0:
            return f"{self.state}"
        else:
            return f"{self.state} \n{sum1}/{sum2} - {float(sum1)/sum2}%"

# s = SeleniumScraper([], True)
# s.start()
# s.reload_called.set()
# while True:
#     input("press enter to check progress.")
#     print(s.get_progress())

