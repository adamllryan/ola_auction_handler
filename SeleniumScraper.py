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
    reload_called: Event
    callback: Event

    def __init__(self, auctions: list[str], debug: bool):
        Thread.__init__(self)

        self.logged_auctions = auctions
        self.auctions = []
        self.debug = debug
        self.running = False
        self.progress = []
        self.total_items = []
        self.reload_called = Event()
        self.callback = Event()
        # self.create_driver()

    def create_driver(self):

        options = FirefoxOptions()

        if not self.debug:
            options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=options)




    def find_auctions(self):

        # Get url

        options = FirefoxOptions()

        if not self.debug:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

        driver.get("https://www.onlineliquidationauction.com/")

        # Grab all auction elements

        auction_elements = try_load_elements(driver, URLS.subpath('', URLS.auctions))

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

    def find_items(self):

        threads = []
        id = 0
        for auction in self.auctions:
            self.progress.append(0)
            self.total_items.append(0)
            thread = Thread(target=self.get_auction_items, args=(auction,id))
            thread.start()
            threads.append(thread)
            self.logged_auctions.add(auction.name)
            id += 1
        for thread in threads:
            thread.join()


    def get_auction_items(self, auction: Auction, id: int):
        
        options = FirefoxOptions()

        if not self.debug:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

        # Get url

        driver.get(auction.url)

        # Set page up and scroll until elements are found

        time.sleep(5)
        names = []

        # need to set to active items only, first load use try_load

        select = try_load_element(driver, URLS.select)
        select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).click()

        # Get number of total items to search for, first load call try_load

        count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))

        if count > 0:

            self.total_items[id] = count
            
            # Get body element so we can scroll

            try_load_element(driver, URLS.first_item)
            body = try_load_element(driver, URLS.body)

            # set repeat counter, so we exit if an item is missed but never accounted for

            repeat_counter = REPEAT_INITIAL_VALUE

            while len(names) < count and repeat_counter > 0:

                self.progress[id] = len(names)
                

                # Find current active items

                live_items = driver.find_elements(By.XPATH, '//*[@id="all-items"]/div')
                live_items.pop()

                for i in live_items:

                    # Get item name text

                    end_text = try_load_element(driver, URLS.date)
                    
                    try:
                        end_text = end_text.text
                    except:
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

        driver.close()

    def get_item_details(self, item: WebDriver, names: list):
        
        try:
            name = item.find_element(By.XPATH, URLS.subpath(URLS.items, URLS.name))
        except:
            return None

        name = name.text

        # If we have not already added this item to our item list

        if name not in names:

            # Set listing url

            url = try_load_element(item, URLS.subpath(URLS.items, URLS.listing_url))

            try:
                url = url.get_attribute("href")
            except:
                return None

            # Set src image urls

            img_url = []
            img_elements = try_load_elements(item, URLS.subpath(URLS.items, URLS.img_elements))

            for element in img_elements:
                img_url.append(try_load_element(element, URLS.subpath(URLS.img_elements,
                                                                      URLS.img_src)).get_attribute('owl-data-src'))

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
            else:
                return None
            
            # Set last price

            last_price = try_load_element(item, URLS.subpath(URLS.items, URLS.last_price))
            try:
                last_price = float(last_price.text.replace('[$', '').replace(']', ''))
            except:
                return None

            condition = ''
            retail_price = 0
            price_condition_text = try_load_element(item, URLS.subpath(URLS.items, URLS.price_condition))
            
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
            
            # Add names to found list

            listing = Item(name, url, img_url, end_time, last_price, retail_price, condition)

            return listing
        return None

    def clean_auctions(self):

        for auction in self.auctions:
            current = datetime.now()
            auction.items = list(filter(lambda x: current > x.end_time, auction.items))
        self.auctions = list(filter(lambda x: len(x.items)>0, self.auctions))
        print(f"Leaving {len(self.auctions)} auctions")

    # def import_(self, items):
        
        

    def export_(self):
        items = []
        for auction in self.auctions:
            for x in auction.items:
                items.append([auction.name, x.name, x.url, x.img_url[0], x.last_price, x.retail_price, x.condition, x.end_time])
        self.auctions.clear()
        return items
        

    def run(self):
        while True:
            flag = self.reload_called.wait(3600)
            if flag:
                print("Refresh Called")
            else:
                print("Auto-refresh triggered")
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
            time.sleep(60)
            self.reload_called.clear()

    
    def close_driver(self):
        if self.driver is not None:
            self.driver.close()
    
    def get_progress(self):
        sum1 = sum(self.progress)
        sum2 = sum(self.total_items)
        if sum2 == 0:
            return 0
        else:
            return f"{sum1}/{sum2} - {float(sum1)/sum2}%"

# s = SeleniumScraper([], True)
# s.start()
# s.reload_called.set()
# while True:
#     input("press enter to check progress.")
#     print(s.get_progress())

