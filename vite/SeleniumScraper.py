from datetime import datetime
import sys
import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from attr import dataclass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread, Event

REPEAT_INITIAL_VALUE = 10
TIMEOUT = 15

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
    src: str
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
        element = WebDriverWait(driver, TIMEOUT).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    finally:

        return element if element is not None else None


def try_load_elements(driver: WebDriver, xpath: str):

    # Load element with timeout set to x seconds

    elements = []
    try:
        WebDriverWait(driver, TIMEOUT).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        elements = driver.find_elements(By.XPATH, xpath)

    finally:

        return elements


class SeleniumScraper(Thread):

    callback = { # Event to trigger refresh and event to trigger export callback
        'page_refresh_trigger': Event(),
        'page_refresh_callback': Event()
    }

    debug = { # Debug events for all responses
        'verbose': False,
        'demo': False,
        'show_display': False
    }

    status = { # All vars related to status of class
        'state': ['Idle - Waiting'],
        'items_found': [],
        'total_items': [],
        'is_running': False,
    }

    auction_data = { # Storage of auction data
        'auctions_in_database': [],
        'auctions_to_process': []
    }

    def __init__(self, auctions: list[str], debug: dict):

        Thread.__init__(self) # Init threading
        self.callback['page_refresh_trigger'] = Event()
        self.callback['page_refresh_callback'] = Event()
        self.auction_data['auctions_in_database'] = auctions
        self.debug = debug

    def create_driver(self):

        self.status['state'].append('Creating Driver')

        options = FirefoxOptions()
        if not self.debug['show_display']:
            options.add_argument("--headless")

        self.status['state'].pop()

        return webdriver.Firefox(options=options)


    def find_auctions(self):

        self.status['state'].append('Finding Auctions')

        driver = self.create_driver()
        driver.get("https://www.onlineliquidationauction.com/")

        auction_elements = try_load_elements(driver, URLS.subpath('', URLS.auctions)) # initial load with Wait

        self.status['state'].append('Getting Auction Data')

        for i in auction_elements:

            # Grab name

            name = i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_name)).text

            # Get url and swap domain with bidding page url, keep ID

            bad_url = 'https://www.onlineliquidationauction.com/auctions/detail/bw'
            good_url = 'https://bid.onlineliquidationauction.com/bid/'
            url = i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_name)).get_attribute("href") \
                .replace(bad_url, good_url)

            # Get image src url and save, not really needed

            img_url = i.find_element(By.XPATH, URLS.subpath(URLS.auctions, URLS.auction_img)).get_attribute('src')

            # Add to auctions list

            if not name in self.auction_data['auctions_in_database']:
                print(name, 'not in', self.auction_data['auctions_in_database'], file=sys.stderr)
                self.auction_data['auctions_to_process'].append(Auction(name, url, img_url, []))

        self.close_driver(driver)

        self.status['state'].pop()
        self.status['state'].pop()

    def find_items(self):

        self.status['state'].append('Creating Item Search Threads and Waiting for Completion')

        threads = []
        id = 0
        for auction in self.auction_data['auctions_to_process']:
            self.status['items_found'].append(0) # Append a 0 for every auction so we can measure progress
            self.status['total_items'].append(0)
            thread = Thread(target=self.get_auction_items, args=(auction,id)) # New thread per auction
            thread.start()
            threads.append(thread) # Make sure threads are tracked
            self.auction_data['auctions_in_database'].append(auction.name) # So we don't rescrape
            id += 1
            if self.debug['demo']:
                break

        for thread in threads:
            thread.join() # Wait for all threads to complete

        self.status['state'].pop()

    def parse_description(self, data: str):
        retail: float # Description is stored as one string
        condition: str
        words = data.replace("Retail Price: ", "").split(" ")
        if 'Unknown' not in words[0] and words[0] != '': # Price is not unknown & not empty
            retail = float(words[0].replace(',', '').replace('$', ''))
        else:
            retail = -1
        condition = ' '.join(words[1::])
        return retail, condition

    def all_items_loaded(self, driver, total_items, id): # Check if all loaded and do status updates
        current_size = int(driver.execute_script('return bwAppState.auction.all_items.items.length'))
        self.status['items_found'][id] = current_size
        
        if self.debug['verbose']:
            print(f'Auction {id}: ({sum(self.status["items_found"])}/{sum(self.status["total_items"])}) found.')

        return total_items <= current_size

    def get_auction_items(self, auction: Auction, id: int):

        # NOTE: This used to be much larger because it would scroll and scrape auction items in sets of 5-10, 
        # has since been replaced with a set of JS lines that force all items to load at once, and then grabs the 
        # auction application state with all the items in it. 

        driver = self.create_driver()
        
        # Get url
        driver.get(auction.url)

        # Originally the element to change to active items, now good for grabbing total items to scrape
        select = try_load_element(driver, URLS.select)

        # Line no longer works because js refresh call requires search option to be default
        # select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).click()

        # Get number of total items to search for, first load call try_load

        count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))
        self.status['total_items'][id] = count
        retries = 60 # 60s of retry
        if count >= 50: # All items are already loaded if <=50
            # JS line that will force next refresh to load 1500 more items (largest auction so far has been 1100)
            driver.execute_script('bwAppState.auction.all_items.api_args.per_page=1500;')
            
            # Force refresh
            driver.execute_script('bwAppState.auction.all_items.fetch_more_items();')
            # Check once a second to see if items have been found, timeout in case items have been removed and numbers are incorrect
            while not self.all_items_loaded(driver, count, id) and retries > 0:
                count = int(select.find_element(By.XPATH, URLS.subpath(URLS.select, URLS.active_item)).
                    text.replace("All > Active (", "").replace(")", ""))
                self.status['total_items'][id] = count
                retries-=1
                
                time.sleep(1)
        # Line that will get all data
        data = driver.execute_script('return Array.from(bwAppState.auction.all_items.items).map(item => [item.name, item.id, item.images.map(img => img.original_url), item.actual_end_time, item.maxbid.amount, item.simple_description, item.auction_id])')
        # Write data to Auction object
        for item in data:
            name = item[0]
            url = 'https://bid.onlineliquidationauction.com/bid/'+ str(item[6]) + '?section=auction&item=' + str(item[1])
            img = ';'.join(item[2])
            # print(item[2])
            end = datetime.strptime(item[3], "%Y-%m-%dT%H:%M:%S.000Z")
            max = item[4]
            retail, condition = self.parse_description(item[5])
            item = Item(name, url, img, end, max, retail, condition)
            auction.items.append(item)
        
        self.close_driver(driver)
        
    # Obsolete, we now clear the whole auction list after write to db and clean in other file
    def clean_auctions(self): 
        
        self.status['state'].append('Cleaning Auctions')

        for auction in self.auction_data['auctions_to_process']:
            current = datetime.now()
            auction.items = list(filter(lambda x: current > x.end_time, auction.items))
        self.auction_data['auctions_to_process'] = list(filter(lambda x: len(x.items)>0, self.auction_data['auctions_to_process']))

        self.status['state'].pop()

    # Export data
    def export_(self):

        self.status['state'].append('Exporting Data')

        items = []
        for auction in self.auction_data['auctions_to_process']:
            for x in auction.items:
                items.append([auction.name, x.name, x.url, x.img_url, x.last_price, x.retail_price, x.condition, x.end_time])
        self.auction_data['auctions_to_process'].clear()

        self.status['state'].pop()

        return items
    
    # Cleanup driver
    def close_driver(self, driver):
        if driver is not None:
            driver.close()
    

    def get_progress(self):
        sum1 = sum(self.status['items_found'])
        sum2 = sum(self.status['total_items'])
        if sum2==0:
            return {'state': self.status['state'], 'progress': 0, 'vals': [sum1, sum2], 'logged': self.auction_data['auctions_in_database']}
        else:
            return {'state': self.status['state'], 'progress': float(sum1)/sum2, 'vals': [sum1, sum2],  'logged': self.auction_data['auctions_in_database']}
        
    def run(self):
        while True:
            # Wait for 1 hour before auto refresh
            flag = self.callback['page_refresh_trigger'].wait(3600)
            if flag:
                print("Refresh Called")
            else:
                print("Auto-refresh triggered")
            
            # Remove idle state

            self.status['state'].pop()

            # Run sequence

            print('running __find_auctions__')
            self.find_auctions()
            print('running __find_items__')
            self.find_items()

            # Set callback flag for flask server
            self.callback['page_refresh_callback'].set()

            self.status['state'].append('Idle - Cooldown')
            # time.sleep(300) # Force cooldown 5 min so we don't overburden server
            self.callback['page_refresh_trigger'].clear()
            self.status['state'][0] = ('Idle - Waiting')    
    

if __name__ == '__main__':
    debug = {
        'verbose': True,
        'demo': False,
        'show_display': True
    }
    s = SeleniumScraper([], debug)
    s.start()
    s.callback['page_refresh_trigger'].set()
    while True:
        input("press enter to check progress.")
        print(s.get_progress())

