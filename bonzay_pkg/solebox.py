import requests
import json
from bs4 import BeautifulSoup as bs
from names import get_first_name, get_last_name
from colorama import Fore, Style, init
import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import threading

from bonzay_pkg.reusable import getTime, saveIntoFile, readFile, isProxyGood, loadProxies, loadUseragents

init(autoreset=True)

# -------------------------------------------------------------------------------- SOLEBOX SPECIFIC FUNCTIONS -------------------------------------------------------------------------------- #

def logMessage(status: str, message: str):
    print(getTime() + f"[{status:<8}] -> {message}")

def scrapeCountryIds(headers: dict):
    """
    Scrapes country IDs from Solebox's website

    Args:
        headers {dict}  - Headers that are sent with the requests to scrape the IDs
    Returns: 
        None
    """
    country_data = {}
    logMessage("STATUS", "Scraping country IDs...")
    s = requests.Session()
    r = s.get(url='https://www.solebox.com/', headers=headers)
    soup = bs(r.text, 'lxml')
    countr_selection = soup.find('select', {'id':'invCountrySelect'})
    country_values = countr_selection.contents
    for val in country_values:
        # scraped info is separate by new lines which we want to skip
        if val == '\n':
            continue
        else:
            country_id = val['value']
            country_name = val.text
            country_data[country_name] = country_id

    saveIntoFile("countrydata.json", country_data)
    logMessage("SUCCESS", "Country IDs scraped!")

def getCountryId(country_name: str):
    """
    Reads file `countrydata.json` and returns a value matched with `country_name`

    Args:
        - country_name {str}    - Name of the country you want to get the ID for

    Returns:
        - country_id {str}      - ID of the country (if found)
        - None                  - if not found
    """
    if os.stat("countrydata.json").st_size == 0:
        scrapeCountryIds({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6',
                # 'cache-control': 'max-age=0',
                # 'sec-fetch-mode': 'navigate',
                # 'sec-fetch-site': 'none',
                'referer' : "https://www.google.com/",
                # 'sec-fetch-user': '?1',
                # 'origin': 'https://www.solebox.com',
                # 'upgrade-insecure-requests': '1',
                # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            })
    country_data = readFile("countrydata.json")
    try:
        country_id = country_data[country_name]
        return country_id
    except:
        logMessage("ERROR", "Error getting country_id, check your country name in userdata.json!")
        return None

def parseStoken(req, print_lock):
    soup = bs(req.text, 'lxml')
    with print_lock:
        logMessage("STATUS", "Parsing stoken...")
    try:
        stoken = soup.find('input', {'name': 'stoken'})['value']
        with print_lock:
            logMessage("SUCCESS", f"Successfully parsed stoken: {stoken}!")
    except:
        with print_lock:
            stoken = None
            logMessage("ERROR", "Unable to get stoken.")
    return stoken

def sendSoleboxWebhook(webhook_url, title, email, passwd):
    hook = DiscordWebhook(url=webhook_url, username="BONZAY Tools", avatar_url="https://avatars1.githubusercontent.com/u/38296319?s=460&v=4")
    color=15957463

    embed = DiscordEmbed(
        title = title,
        color=color,
        url="https://github.com/rtunaboss/SoleboxAccountGenerator",
    )
    embed.set_timestamp()
    embed.set_footer(text="BONZAY Tools",icon_url="https://cdn.discordapp.com/attachments/527830358767566848/622854816120569887/Bonzay.png")
    embed.add_embed_field(name="Username", value=f"{email}")
    embed.add_embed_field(name="Password", value=f"||{passwd}||", inline=False)
    hook.add_embed(embed)
    hook.execute()

# -------------------------------------------------------------------------------- GEN CLASS -------------------------------------------------------------------------------- #

class SoleboxGen():

    def __init__(self):
        # ---------- Headers ---------- #
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6',
            # 'cache-control': 'max-age=0',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'none',
            'referer' : "https://www.google.com/",
            # 'sec-fetch-user': '?1',
            # 'origin': 'https://www.solebox.com',
            # 'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }

        # ---------- Loading user input data ---------- #
        config = readFile("./userdata.json")
        userdata = config["profile"]
        self.settings = config["settings"]

        self.first_name = userdata["first_name"]
        self.last_name = userdata["last_name"]
        self.phone_num = userdata["phone_num"]

        self.catchall = userdata["catchall"]

        if self.catchall.strip() == '':
            catchall = "gmail.com"
        if '@' in self.catchall:
            self.catchall = catchall.replace('@', '')

        self.passwd = userdata["passwd"]

        self.address_first_line = userdata["address_first_line"]
        self.house_number = userdata["house_number"]
        self.address_second_line = userdata["address_second_line"]
        self.zipcode = userdata["zipcode"]
        self.city = userdata["city"]
        self.country_name = userdata["country_name"]
        self.us_state = userdata["us_state"]

        self.webhook_url = userdata["webhook_url"]

        # ---------- Loading data ---------- #
        self.country_id = getCountryId(self.country_name)

    def buildBillingPayload(self, stoken: str):
        if self.useragent_type == "mobile":
            register_payload = {
                'stoken': stoken,
                'lang': 1,
                'actcontrol': 'register',
                'fnc': 'registeruser',
                'cl': 'register',
                'lgn_cook': 0,
                'reloadaddress': '',
                'option': 3,
                'lgn_usr': self.email,
                'lgn_pwd': self.passwd,
                'lgn_pwd2': self.passwd,
                'blnewssubscribed': 0,
                'invadr[oxuser__oxsal]': random.choice(['MR', 'MRS']),
                'invadr[oxuser__oxfname]': self.first_name,
                'invadr[oxuser__oxlname]': self.last_name,
                'invadr[oxuser__oxcompany]': '',
                'invadr[oxuser__oxaddinfo]': self.address_second_line,
                'invadr[oxuser__oxstreet]': self.address_first_line,
                'invadr[oxuser__oxstreetnr]': self.house_number,
                'invadr[oxuser__oxzip]': self.zipcode,
                'invadr[oxuser__oxcity]': self.city,
                'invadr[oxuser__oxustid]': '',
                'invadr[oxuser__oxcountryid]': self.country_id,
                'invadr[oxuser__oxstateid]': self.us_state,
                'invadr[oxuser__oxfon]': self.phone_num,
                'invadr[oxuser__oxfax]': '',
                'invadr[oxuser__oxmobfon]': '',
                'invadr[oxuser__oxprivfon]': '',
                'invadr[oxuser__oxbirthdate][day]': '',
                'invadr[oxuser__oxbirthdate][month]': '',
                'invadr[oxuser__oxbirthdate][year]': '',
                'save': '',
            }
        else:
            register_payload = {
                "stoken": stoken,
                "lang": 1,
                "listtype": "",
                "actcontrol": "account",
                "cl": "user",
                "fnc": "createuser",
                "reloadaddress": "",
                "blshowshipaddress": 1,
                "invadr[oxuser__oxsal]": random.choice(['MR', 'MRS']),
                "invadr[oxuser__oxfname]": self.first_name,
                "invadr[oxuser__oxlname]": self.last_name,
                "invadr[oxuser__oxstreet]": self.address_first_line,
                "invadr[oxuser__oxstreetnr]": self.house_number,
                "invadr[oxuser__oxaddinfo]": self.address_second_line,
                "invadr[oxuser__oxzip]": self.zipcode,
                "invadr[oxuser__oxcity]": self.city,
                "invadr[oxuser__oxcountryid]": self.country_id,
                "invadr[oxuser__oxstateid]": self.us_state,
                "invadr[oxuser__oxbirthdate][day]": "",
                "invadr[oxuser__oxbirthdate][month]": "",
                "invadr[oxuser__oxbirthdate][year]": "",
                "invadr[oxuser__oxfon]": self.phone_num,
                "lgn_usr": self.email,
                "lgn_pwd": self.passwd,
                "lgn_pwd2": self.passwd,
                "userform": "",
            }

        return register_payload

    def buildShippingPayload(self, stoken: str):
        return {
            # 'MIME Type': 'application/x-www-form-urlencoded',
            'stoken': stoken,
            'lang': '1',
            'listtype': '',
            'actcontrol': 'account_user',
            'fnc': 'changeuser_testvalues',
            'cl': 'account_user',
            'CustomError': 'user',
            'blshowshipaddress': '1',
            'invadr[oxuser__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
            'invadr[oxuser__oxfname]': self.first_name,
            'invadr[oxuser__oxlname]': self.last_name,
            'invadr[oxuser__oxstreet]': self.address_first_line,
            'invadr[oxuser__oxstreetnr]': self.house_number,
            'invadr[oxuser__oxaddinfo]': self.address_second_line,
            'invadr[oxuser__oxzip]': self.zipcode,
            'invadr[oxuser__oxcity]': self.city,
            'invadr[oxuser__oxcountryid]': self.country_id,
            'invadr[oxuser__oxstateid]': self.us_state,
            'invadr[oxuser__oxfon]': self.phone_num,
            'changeClass': 'account_user',
            'oxaddressid': '-1',
            'deladr[oxaddress__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
            'deladr[oxaddress__oxfname]': self.first_name,
            'deladr[oxaddress__oxlname]': self.last_name,
            'deladr[oxaddress__oxcompany]': '',
            'deladr[oxaddress__oxstreet]': self.address_first_line,
            'deladr[oxaddress__oxstreetnr]': self.house_number,
            'deladr[oxaddress__oxaddinfo]': self.address_second_line,
            'deladr[oxaddress__oxzip]': self.zipcode,
            'deladr[oxaddress__oxcity]': self.city,
            'deladr[oxaddress__oxcountryid]': self.country_id,
            'deladr[oxaddress__oxstateid]': self.us_state,
            'deladr[oxaddress__oxfon]': self.phone_num,
            'userform' : '',
        }
    
    def jigInfo(self):

        linetwolist =['apt', 'apartment', 'dorm', 'suite', 'unit', 'house', 'unt', 'room', 'floor']
        
        jig_name = self.settings["jig_name"]
        jig_first_line = self.settings["jig_first_line"]
        jig_second_line = self.settings["jig_second_line"]
        jig_phone_number = self.settings["jig_phone_number"]

        if jig_name:
            self.first_name = get_first_name()
            self.last_name = get_last_name()

        if jig_phone_number:
            self.phone_num = f'+1{random.randint(300,999)}{random.randint(300,999)}{random.randint(300,999)}{random.randint(0,9)}'

        if jig_first_line:
            self.address_first_line = f'{2*(chr(random.randint(97,97+25)).upper() + chr(random.randint(97,97+25)).upper())} {self.address_first_line}'

        if self.address_second_line == '' and jig_second_line:
            self.address_second_line = f'{random.choice(linetwolist)} {random.randint(1,20)}{chr(random.randint(97,97+25)).upper()}'

        self.email = f'{get_first_name()}{random.randint(1,9999999)}@{self.catchall}'

    def setup(self):
        self.jigInfo()

        self.useragent_type = random.choice(["mobile", "desktop"])
        all_useragents_list = loadUseragents()
        if self.useragent_type == "desktop":
            # all_useragents_list[0] means desktop useragent list
            self.headers['user-agent'] = random.choice(all_useragents_list[0])
        else:
            # all_useragents_list[1] means mobile useragent list
            self.headers['user-agent'] = random.choice(all_useragents_list[1])

        self.proxy_list = loadProxies("./proxies.txt")

        self.s = requests.Session()
        self.stoken = None

    def testWorkingProxies(self, print_lock):
        """

        Returns:
            True    - if a working proxy was found
            False   - if a working proxy was NOT found
        """
        # ---------- Proxy testing ---------- #
        test_count = 0
        while True:
            self.s.proxies = random.choice(self.proxy_list)
            with print_lock:
                logMessage("STATUS", "Checking proxy...")
            
            # s.get('https://www.solebox.com/en/home/', headers=headers)
            try:
                test = self.s.get(url='https://www.solebox.com/en/open-account/', headers=self.headers, timeout=5)
            except:
                with print_lock:
                    logMessage("ERROR", "Proxy timed out, rotating proxy...")
                continue
            if test.status_code in (302, 200):
                with print_lock:
                    logMessage("STATUS", "Proxy working...")
                return True
            elif "captcha.js" in test.text:
                with print_lock:
                    logMessage("ERROR", "Encountered CloudFare (captcha), rotating proxy...")
            else:
                with print_lock:
                    logMessage("ERROR", "Proxy banned, rotating proxy...")
            
            if test_count > 50:
                with print_lock:
                    logMessage("CRITICAL", "Retry limit exceeded. Load more proxies or generate new ones.")
                break
            test_count += 1
        return False

    def generateAccount(self, print_lock: threading.Lock):
        """
        Returns:
            - True (on success)
            - False (on failure)
        """
        # ---------------------------------------- Setting up ---------------------------------------- #
        self.setup()

        with print_lock:
            logMessage("STATUS", f"Generating account for {self.email}")
        
        # ---------- Proxy testing ---------- #
        proxy_status = testWorkingProxies(print_lock)
        if not proxy_status:
            return False
        
        # ---------- Parsing stoken ---------- #
        self.stoken = parseStoken(test, print_lock)
        if self.stoken is None:
            return False

        # ---------------------------------------- Creating an account ---------------------------------------- #
        with print_lock:
            logMessage("STATUS", f"Trying to create an account for {self.email}, using {self.useragent_type} mode.")
        register_payload = self.buildBillingPayload(self.stoken)

        # ---------- Posting to create an account ---------- #
        register_post = self.s.post(url='https://www.solebox.com/index.php?lang=1&', headers=self.headers, data=register_payload)
        if "Not possible to register" in register_post.text:
            with print_lock:
                logMessage("ERROR", f"Unable to create an account. Solebox returned:\n\'Not possible to register {self.email}. Maybe you have already registered?\'")
            return False
        if "captcha.js" in register_post.text:
            with print_lock:
                logMessage("ERROR", "Unable to generate account - encountered Cloudfare. (captcha)")
            return False
        if register_post.status_code in (302, 200):
            with print_lock:
                logMessage("SUCCESS", "Successfully created an account.")
        else:
            with print_lock:
                logMessage("ERROR", f"ERROR {register_post.status_code} occurred: Unable to create an account.")
            return False
        return True

        # ---------------------------------------- Updating an account ---------------------------------------- #
        
    def login(self, print_lock: threading.Lock):
        """

        Returns:
            True    - if successfully logged in
            False   - if logging in wasn't successful
            None    - if logging in failed
        """
        with print_lock:
            logMessage("STATUS", f"Trying to log in as {self.email}.")
        login_url = "https://www.solebox.com/index.php?lang=1&"
        login_payload = {
            "stoken": self.stoken,
            "lang": 1,
            "listtype": "",
            "actcontrol": "account",
            "fnc": "login_noredirect",
            "cl": "account",
            "lgn_usr": self.email,
            "lgn_pwd": self.passwd,
        }
        try:
            p = self.s.get(url=login_url, headers=self.headers, data=login_payload)
        except:
            with print_lock:
                logMessage("STATUS", f"Failed to log in as {self.email}.")
            return
        if p.status_code in (302, 200) and "YOUR SOLEBOX DASHBOARD" in p.text:
            with print_lock:
                logMessage("STATUS", f"Logged in successfully as {self.email}.")
                return True
        elif "Wrong e-mail address or password!" in p.text:
            with print_lock:
                logMessage("STATUS", f"Failed to log in as {self.email}.")
                return False
        else:
            with print_lock:
                logMessage("STATUS", f"Failed to log in as {self.email}. Status code {p.status_code}")
                return None

    def updateShippingAddress(self, print_lock: threading.Lock, new_account: bool):
        # ---------------------------------------- This part executes only if the account isn't new ---------------------------------------- #
        if not new_account:

            # ---------- Setup ---------- #

            self.setup()
            # ---------- Proxy testing ---------- #
            proxy_status = testWorkingProxies(print_lock)
            if not proxy_status:
                return False
            
            # ---------- Parsing stoken ---------- #
            self.stoken = parseStoken(test, print_lock)
            if self.stoken is None:
                return False
            
            # ---------- Logging in ---------- #
            self.login(print_lock)

        # ---------------------------------------- Updating the shipping address ---------------------------------------- #
        with print_lock:
            logMessage("STATUS", f"Updating shipping address for {self.email}")
        
        if self.stoken is None:
            r = self.s.get('https://www.solebox.com/en/open-account/', headers=self.headers, timeout=5)
            parseStoken(r, print_lock)
        update_shipping_payload = self.buildShippingPayload(self.stoken)

        update_shipping_post = self.s.post(url='https://www.solebox.com/index.php?lang=1&', headers=self.headers, data=update_shipping_payload)
        if "captcha.js" in update_shipping_post.text:
            with print_lock:
                logMessage("ERROR", "Unable to edit shipping details - encountered Cloudfare. (captcha)")
            return False
        if update_shipping_post.status_code in (302,200):
            with print_lock:
                logMessage("SUCCESS", "Successfully updated accounts shipping details.")
            saveIntoFile("./accounts/solebox-valid.txt", f"{self.email}:{self.passwd}\n")
            if self.webhook_url.strip() != '':
                if new_account:
                    message = "Account successfully created!"
                else:
                    message = "Shipping details updated successfully created!"
                sendSoleboxWebhook(self.webhook_url, message, self.email, self.passwd)

        else:
            with print_lock:
                logMessage("ERROR", f"Error {update_shipping_post.status_code} occurred: Unable to edit shipping details.")
            if new_account:
                saveIntoFile("./accounts/solebox-no-shipping.txt", f"{self.email}:{self.passwd}\n")

    def checkAccount(self, print_lock: threading.Lock):
        with print_lock:
            logMessage("STATUS", f"Checking account {self.email}...")

        # ---------- Setup ---------- #
        self.setup()

        # ---------- Proxy testing ---------- #
        proxy_status = self.testWorkingProxies(print_lock)
        if not proxy_status:
            return False

        # ---------- Logging in ---------- #
        login_status = self.login(print_lock)
        if login_status:
            with print_lock:
                logMessage("SUCCESS", f"Account {self.email} is working.")
            return True
        elif login_status == None:
            with print_lock:
                logMessage("ERROR", f"Checking failed for account {self.email}.")
        else:
            with print_lock:
                logMessage("ERROR", f"Account {self.email} is NOT working.")
            return False
    
    def checkShippingAddress(self, print_lock: threading.Lock):
        pass