import requests
import json
from bs4 import BeautifulSoup as bs
from names import get_first_name, get_last_name
from colorama import Fore, Style, init
import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import threading
import time
import cloudscraper

try:
    from bonzay_pkg.reusable import getTime, saveIntoFile, appendIntoFile, readFile, isProxyGood, loadProxies, loadUseragents
except:
    from reusable import getTime, saveIntoFile, appendIntoFile, readFile, isProxyGood, loadProxies, loadUseragents

init(autoreset=True)

# -------------------------------------------------------------------------------- SOLEBOX SPECIFIC FUNCTIONS -------------------------------------------------------------------------------- #

def logMessage(status: str, message: str):
    status=f"[{status}]"
    if "success" in status.lower():
        print(Fore.GREEN + f"{getTime():<25}" + f"{status.upper():<10} -> {message}")
    elif "error" in status.lower():
        print(Fore.RED + f"{getTime():<25}" + f"{status.upper():<10} -> {message}")
    else:
        print(f"{getTime():<25}" + f"{status.upper():<10} -> {message}")

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

    def __init__(self, proxy_list):

        # ---------- General ---------- #
        self.proxy_list = proxy_list

        useragents = loadUseragents()
        # ---------- Generation Type ---------- #
        self.useragent_type = random.choice(["mobile", "desktop"])
        if self.useragent_type == "mobile":
            mobile = True
            ua = random.choice(useragents[1])
        else:
            mobile=False
            ua = random.choice(useragents[0])
        # ---------- Headers ---------- #
        SOLEBOX_URLS = [
            "https://www.solebox.com/en/Apparel/",
            "https://www.solebox.com/",
            "https://www.solebox.com/en/New/",
            "https://www.solebox.com/en/Soon/",
            "https://www.solebox.com/en/Footwear/",
            "https://www.solebox.com/en/Accessories/",
            "https://www.solebox.com/index.php?lang=1&cl=brands",
            "https://www.solebox.com/en/Sale/",
            "https://www.solebox.com/blog/",
            "https://www.solebox.com/en/cart/",
        ]

        # ---------- Creating a session ---------- #
        self.s = cloudscraper.create_scraper(browser={'browser': 'chrome', 'mobile': mobile})
        self.s.headers.update({
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": ua,
            "sec-fetch-user": "?1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "referer": random.choice(SOLEBOX_URLS),
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
        })
        self.stoken = None

        # ---------- Loading user input data ---------- #
        config = readFile("./userdata.json")
        userdata = config["profile"]
        self.settings = config["settings"]

        self.first_name = userdata["first_name"]
        self.last_name = userdata["last_name"]
        self.phone_num = userdata["phone_num"]

        self.catchall = userdata["catchall"]

        if self.catchall.strip() == '':
            self.catchall = "gmail.com"
        if '@' in self.catchall:
            self.catchall = self.catchall.replace('@', '')

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
        if self.country_id == None:
            quit()

        # ---------- Jigging info ---------- #
        self.jigInfo()

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
                "invadr[oxuser__oxbirthdate][day]": random.randint(1,27),
                "invadr[oxuser__oxbirthdate][month]": random.randint(1,12),
                "invadr[oxuser__oxbirthdate][year]": random.randint(1950,2000),
                'save': '',
            }
        else:
            register_payload = {
                "stoken": stoken,
                # "lang": random.choice([0,1]),
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
                "invadr[oxuser__oxbirthdate][day]": random.randint(1,27),
                "invadr[oxuser__oxbirthdate][month]": random.randint(1,12),
                "invadr[oxuser__oxbirthdate][year]": random.randint(1950,2000),
                "invadr[oxuser__oxfon]": self.phone_num,
                "lgn_usr": self.email,
                "lgn_pwd": self.passwd,
                "lgn_pwd2": self.passwd,
                "userform": "",
            }

        return register_payload

    def buildShippingPayload(self, stoken: str):
        title = random.choice(["MR", "MRS"])

        if self.useragent_type == "mobile":
            return {
                "stoken": stoken,
                "lang": 1,
                "listtype": "",
                "actcontrol": "account_user",
                "fnc": "changeuser_testvalues",
                "cl": "account_user",
                "CustomError": "user",
                "blshowshipaddress": 1,
                "invadr[oxuser__oxsal]": title,
                "invadr[oxuser__oxfname]": self.first_name,
                "invadr[oxuser__oxlname]": self.last_name,
                "invadr[oxuser__oxstreet]": self.address_first_line,
                "invadr[oxuser__oxstreetnr]": self.house_number,
                "invadr[oxuser__oxaddinfo]": self.address_second_line,
                "invadr[oxuser__oxzip]": self.zipcode,
                "invadr[oxuser__oxcity]": self.city,
                "invadr[oxuser__oxcountryid]": self.country_id,
                "invadr[oxuser__oxstateid]": self.us_state,
                "invadr[oxuser__oxbirthdate][day]": random.randint(1,27),
                "invadr[oxuser__oxbirthdate][month]": random.randint(1,12),
                "invadr[oxuser__oxbirthdate][year]": random.randint(1950,2000),
                "invadr[oxuser__oxfon]": self.phone_num,
                "changeClass": "account_user",
                "oxaddressid": -1,
                "deladr[oxaddress__oxsal]": title,
                "deladr[oxaddress__oxfname]": self.first_name,
                "deladr[oxaddress__oxlname]": self.last_name,
                "deladr[oxaddress__oxcompany]": "",
                "deladr[oxaddress__oxstreet]": self.address_first_line + ' ' + self.house_number,
                "deladr[oxaddress__oxstreetnr]": self.address_second_line,
                "deladr[oxaddress__oxzip]": self.zipcode,
                "deladr[oxaddress__oxcity]": self.city,
                "deladr[oxaddress__oxcountryid]": self.country_id,
                "deladr[oxaddress__oxstateid]": self.us_state,
                "deladr[oxaddress__oxfon]": self.phone_num,
            }
        else:
            return {
                "stoken": stoken,
                "lang": 1,
                "listtype": "",
                "actcontrol": "account_user",
                "fnc": "changeuser_testvalues",
                "cl": "account_user",
                "CustomError": "user",
                "blshowshipaddress": 1,
                "invadr[oxuser__oxsal]": title,
                "invadr[oxuser__oxfname]": self.first_name,
                "invadr[oxuser__oxlname]": self.last_name,
                "invadr[oxuser__oxstreet]": self.address_first_line,
                "invadr[oxuser__oxstreetnr]": self.house_number,
                "invadr[oxuser__oxaddinfo]": self.address_second_line,
                "invadr[oxuser__oxzip]": self.zipcode,
                "invadr[oxuser__oxcity]": self.city,
                "invadr[oxuser__oxcountryid]": self.country_id,
                "invadr[oxuser__oxstateid]": self.us_state,
                "invadr[oxuser__oxbirthdate][day]": random.randint(1,27),
                "invadr[oxuser__oxbirthdate][month]": random.randint(1,12),
                "invadr[oxuser__oxbirthdate][year]": random.randint(1950,2000),
                "invadr[oxuser__oxfon]": self.phone_num,
                "changeClass": "account_user",
                "oxaddressid": -1,
                "deladr[oxaddress__oxsal]": title,
                "deladr[oxaddress__oxfname]": self.first_name,
                "deladr[oxaddress__oxlname]": self.last_name,
                "deladr[oxaddress__oxcompany]": "",
                "deladr[oxaddress__oxstreet]": self.address_first_line,
                "deladr[oxaddress__oxstreetnr]": self.house_number,
                "deladr[oxaddress__oxaddinfo]": self.address_second_line,
                "deladr[oxaddress__oxzip]": self.zipcode,
                "deladr[oxaddress__oxcity]": self.city,
                "deladr[oxaddress__oxcountryid]": self.country_id,
                "deladr[oxaddress__oxstateid]": self.us_state,
                "deladr[oxaddress__oxfon]": self.phone_num,
                "userform" : "",
            }

    def jigInfo(self):

        linetwolist =['apt', 'apartment', 'dorm', 'suite', 'unit', 'house', 'unt', 'room', 'floor']
        
        jig_first_name = self.settings["jig_first_name"]
        jig_last_name = self.settings["jig_last_name"]

        jig_first_line = self.settings["jig_first_line"]
        jig_second_line = self.settings["jig_second_line"]
        jig_phone_number = self.settings["jig_phone_number"]

        if jig_first_name:
            self.first_name = get_first_name()
        if jig_last_name:
            self.last_name = get_last_name()

        if jig_phone_number:
            self.phone_num = f'+1{random.randint(300,999)}{random.randint(300,999)}{random.randint(300,999)}{random.randint(0,9)}'

        if jig_first_line:
            self.address_first_line = f'{2*(chr(random.randint(97,97+25)).upper() + chr(random.randint(97,97+25)).upper())} {self.address_first_line}'

        if self.address_second_line == '' and jig_second_line:
            self.address_second_line = f'{random.choice(linetwolist)} {random.randint(1,20)}{chr(random.randint(97,97+25)).upper()}'

        self.email = f'{get_first_name()}{random.randint(1,9999999)}@{self.catchall}'

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
            
            self.s.get("https://www.solebox.com/en/home/")
            try:
                if self.useragent_type == "mobile":
                    test = self.s.get(url="https://www.solebox.com/en/open-account/")
                else:
                    test = self.s.get(url="https://www.solebox.com/en/my-account/")
            except:
                with print_lock:
                    logMessage("ERROR", "Proxy timed out, rotating proxy...")
                continue
            if test.status_code in (302, 200):
                with print_lock:
                    logMessage("STATUS", "Proxy working...")
                self.stoken = parseStoken(test, print_lock)
                return True
            elif test.url == "https://www.solebox.com/offline.html":
                with print_lock:
                    logMessage("ERROR", "Website is down...")
            elif "captcha.js" in test.text:
                with print_lock:
                    logMessage("ERROR", "Encountered CloudFare (captcha), rotating proxy...")
            else:
                with print_lock:
                    logMessage("ERROR", "Proxy banned, rotating proxy...")
            time.sleep(random.randint(1,3))
            if test_count >= (len(self.proxy_list) - 10):
                with print_lock:
                    logMessage("CRITICAL", "Retry limit exceeded. Load more proxies or generate new ones.")
                return False
            test_count += 1
        return False

    def generateAccount(self, print_lock: threading.Lock):
        """
        Returns:
            - True (on success)
            - False (on failure)
        """
        
        # ---------- Proxy testing ---------- #
        proxy_status = self.testWorkingProxies(print_lock)
        if not proxy_status:
            return False
        
        with print_lock:
            logMessage("STATUS", f"Generating account for {self.email}")

        # ---------- Parsing stoken (if it's not obtained from proxy testing) ---------- #
        if self.stoken is None:
            try:
                if self.useragent_type == "mobile":
                    r = self.s.get(url="https://www.solebox.com/en/open-account/")
                else:
                    r = self.s.get(url="https://www.solebox.com/en/my-account/")
                parseStoken(r, print_lock)
            except:
                with print_lock:
                    logMessage("ERROR", "Unable to edit shipping details. Try again later or use different proxies.")
                return False

        # ---------------------------------------- Creating an account ---------------------------------------- #
        with print_lock:
            logMessage("STATUS", f"Trying to create an account for {self.email}, using {self.useragent_type} mode.")
        register_payload = self.buildBillingPayload(self.stoken)
        time.sleep(random.randint(5,10))
        # ---------- Posting to create an account ---------- #

        register_post = self.s.post(url='https://www.solebox.com/index.php?lang=1&', data=register_payload)
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
                logMessage("SUCCESS", f"Successfully created an account for {self.email}")
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

        # ---------- If there's no stoken, that means that we haven't tested proxies for the website yet, so we have to test ---------- #
        if self.stoken == None:
            # ---------- Proxy testing ---------- #
            proxy_status = self.testWorkingProxies(print_lock)
            if not proxy_status:
                return False
        
        if self.useragent_type == "mobile":
            login_payload = {
                "stoken": self.stoken,
                "lang": 1,
                "listtype": "",
                "actcontrol": "account",
                "fnc": "login_noredirect",
                "cl": "account",
                "tpl": '',
                "oxloadid": '',
                "lgn_usr": "self.email",
                "lgn_pwd": "self.passwd",
                "lgn_cook": 1,
            }
        else:
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
            p = self.s.post(url=login_url, data=login_payload)
        except:
            with print_lock:
                logMessage("ERROR", f"Failed to log in as {self.email}.")
            return False
        if p.status_code in (302, 200) and "Your solebox Dashboard".lower() in p.text.lower():
            with print_lock:
                logMessage("SUCCESS", f"Logged in successfully as {self.email}.")
                return True
        elif "Wrong e-mail address or password!" in p.text:
            with print_lock:
                logMessage("ERROR", f"Failed to log in as {self.email}.")
                return False
        else:
            with print_lock:
                logMessage("ERROR", f"Failed to log in as {self.email}. Status code {p.status_code}")
                return None

    def updateShippingAddress(self, print_lock: threading.Lock, new_account: bool, email: str = None, passwd: str = None):
        # ---------------------------------------- This part executes only if the account isn't new ---------------------------------------- #
        if not new_account:
            # ---------- Setup ---------- #
            if email != None:
                self.email = email
            if passwd != None:
                self.passwd = passwd

            # ---------- Proxy testing ---------- #
            proxy_status = self.testWorkingProxies(print_lock)
            if not proxy_status:
                return False
            
            # ---------- Logging in ---------- #
            login_status = self.login(print_lock)
            if login_status == False:
                return False

        # ---------------------------------------- Updating the shipping address ---------------------------------------- #
        with print_lock:
            logMessage("STATUS", f"Updating shipping address for {self.email}...")
        
        # ---------- Parsing stoken (if it's not obtained from proxy testing) ---------- #
        if self.stoken is None:
            try:
                r = self.s.get('https://www.solebox.com/en/open-account/')
                parseStoken(r, print_lock)
            except:
                with print_lock:
                    logMessage("ERROR", "Unable to edit shipping details. Try again later or use different proxies.")
                return False
        
        # headers_cpy["referer"] = random.choice(["https://www.solebox.com/en/my-address/", "https://www.solebox.com/meine-adressen/"])
        # headers_cpy["referer"] = "https://www.solebox.com/en/my-address/"

        update_shipping_payload = self.buildShippingPayload(self.stoken)
        time.sleep(random.randint(5,10))
        update_shipping_post = self.s.post(url='https://www.solebox.com/index.php?lang=1&', data=update_shipping_payload)
        # update_shipping_post = self.s.post(url='https://www.solebox.com/index.php?lang=1&', headers=headers_cpy, data=update_shipping_payload)

        if "captcha.js" in update_shipping_post.text:
            with print_lock:
                logMessage("ERROR", "Unable to edit shipping details - encountered Cloudfare. (captcha)")
            return False
        if update_shipping_post.status_code in (302,200):
            with print_lock:
                logMessage("SUCCESS", f"Successfully updated account's shipping details for {self.email}.")
            appendIntoFile("./accounts/solebox-valid.txt", f"{self.email}:{self.passwd}\n")
            if self.webhook_url.strip() != '':
                if new_account:
                    message = "Account successfully created!"
                else:
                    message = "Shipping details updated successfully!"
                sendSoleboxWebhook(self.webhook_url, message, self.email, self.passwd)

        else:
            with print_lock:
                logMessage("ERROR", f"Error {update_shipping_post.status_code} occurred: Unable to edit shipping details.")
            if new_account:
                appendIntoFile("./accounts/solebox-no-shipping.txt", f"{self.email}:{self.passwd}\n")

    def checkAccount(self, print_lock: threading.Lock, email, passwd):
        # ---------- Setup ---------- #
        self.email = email
        self.passwd = passwd

        with print_lock:
            logMessage("STATUS", f"Checking account {self.email}...")

        # ---------- Proxy testing ---------- #
        proxy_status = self.testWorkingProxies(print_lock)
        if not proxy_status:
            return False

        # ---------- Parsing stoken (if it's not obtained from proxy testing) ---------- #
        if self.stoken is None:
            try:
                r = self.s.get('https://www.solebox.com/en/open-account/')
                parseStoken(r, print_lock)
            except:
                with print_lock:
                    logMessage("ERROR", "Unable to edit shipping details. Try again later or use different proxies.")
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
    
    def checkShippingAddress(self, print_lock: threading.Lock, email: str = None, passwd: str = None):
        """

        Returns:
            - True  - if there is a shippping address
            - False - if there isn't a shipping address
            - None  - on error
        """
        # ---------- Setup ---------- #
        if email != None:
            self.email = email
        if passwd != None:
            self.passwd = passwd
        address_url = "https://www.solebox.com/en/my-address/"

        with print_lock:
            logMessage("STATUS", f"Checking if account {self.email} has a shipping address...")
        
        # ---------- Logging in ---------- #
        # We don't need to proxy test bcs we test the proxy while logging in
        login_status = self.login(print_lock)
        if login_status == False:
            return None
        
        # ---------- Going to the shipping page ---------- #
        try:
            r = self.s.get(url=address_url)
        except:
            return False
        if r.status_code in (302,200):
            soup = bs(r.text, "lxml")
            address_selection = soup.find("select", {"id":"addressId", "name": "oxaddressid"})
            options = address_selection.find_all("option", {"value": True})
            # ---------- Checking if an account has a shipping address ---------- #
            if len(options) == 1:
                logMessage("STATUS", f"Account {self.email} does NOT have a shipping address.")
                return False
            else:
                logMessage("SUCCESS", f"Account {self.email} DOES have a shipping address.")
                return True
        return False
      
if __name__ == "__main__":
    print_lock = threading.Lock()
    PROXY_LIST = loadProxies("./proxies.txt")
    if not PROXY_LIST:
        logMessage("ERROR", "You did not load proxies. Put your proxies into the proxies.txt file before running.")
        exit()
    gen = SoleboxGen(PROXY_LIST)
    create_status = gen.generateAccount(print_lock)
    if create_status:
        gen.updateShippingAddress(print_lock, new_account=True)