#### made by: rtuna#4321 | @rTunaboss
#### Working on Python 3.8.0

print(r'''
 ____    ____   _   _  ______       __     __ _        
|  _ \  / __ \ | \ | ||___  /    /\ \ \   / /(_)       
| |_) || |  | ||  \| |   / /    /  \ \ \_/ /  _   ___  
|  _ < | |  | || . ` |  / /    / /\ \ \   /  | | / _ \ 
| |_) || |__| || |\  | / /__  / ____ \ | | _ | || (_) |
|____/  \____/ |_| \_|/_____|/_/    \_\|_|(_)|_| \___/ 
''')
print(" • made by: rtuna#4321 | @rTunaboss")
print(" • for personal use only")
print('-------------------------------------\n')
####################          Settings [Feel free to modify this]          ####################

how_many = None
# how_many = 1
while not how_many:
    try:
        how_many = int(input("How many accounts would you like to create?\n"))
    except ValueError:
        print("This is not an integer. Try again...")
jigFirstAndLast = False #or True
jigFirst = False #or True
jigPhone = True #or False
jigFirstLineAddress = True #or False
jigSecondLineAddress = True #or False
#TODO Also make sure you fill in everything in the userdata.json file.

#-------------------------------- DO NOT MODIFY THE CODE BELOW UNLESS YOU KNOW WHAT YOU'RE DOING --------------------------------#

####################          Importing necessary libraries          ####################
import requests
from bs4 import BeautifulSoup as bs
from names import get_first_name, get_last_name
import random
import time
import datetime
import threading
import cfscrape
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)
####################          Defining non-account specific functions          ####################
def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    threadname = threading.currentThread().getName()
    threadname = str(threadname).replace('Thread', 'Task')
    now = '[' + str(now) + ']' + ' ' + '[' + str(threadname) + ']'
    return now

def loadProxyUserPass(filename):
    global proxyList
    with open(filename + '.txt') as f:
        file_content = f.read()
    file_rows = file_content.split('\n')
    for i in range(0, len(file_rows)):
        if ':' in file_rows[i]:
            tmp = file_rows[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)

def loadProxyIpAuth(filename):
    with open(filename + '.txt') as f:
        file_content = f.read()

    tmp = file_content.split('\n')
    for n in range(0, len(tmp)):
        if ':' in tmp[n]:
            temp = tmp[n]
            proxies = {'http': 'http://' + temp,  'https': 'http://' + temp}
            proxyList.append(proxies)

def saveEmail(email, passwd):
    with open('valid_emails.txt', 'a') as f:
        f.write(f'{email}:{passwd}\n')

def saveNoShipEmail(email, passwd):
    with open('no_ship_addy_emails.txt', 'a') as f:
        f.write(f'{email}:{passwd}\n')

def getStoken(s):
    try:
        print(gettime() + ' [STATUS] -> Trying to scrape stoken...')
        index_url = 'https://www.solebox.com/en/my-account/'
        index_r = s.get(url=index_url, headers=headers)
        if index_r.status_code == 200:
            soup = bs(index_r.text, 'lxml')
            stoken = soup.find('input', {'name': 'stoken'})['value']
            print(Fore.GREEN + Style.BRIGHT + gettime() + f' [SUCCESS] -> Successfully scraped stoken: {stoken} !')
            return stoken
        else:
            print(Fore.RED + gettime() + ' [ERROR] -> Bad request. Satus code %d, try to change proxies if this error persists.' % index_r.status_code)
            return
    except:
        print(Fore.RED + gettime() + ' [ERROR] -> Unable to get stoken.')

def scrapeCountryIds():
    country_data = {}
    print(gettime() + ' [STATUS] -> Scraping country IDs...')
    s = cfscrape.create_scraper()
    r = s.get(url='https://www.solebox.com/en/my-account/', headers=headers)
    soup = bs(r.text, 'lxml')
    countrySelection = soup.find('select', {'id':'invCountrySelect'})
    countryValues = countrySelection.contents
    for val in countryValues:
        # scraped info is separate by new lines which we want to skip
        if val == '\n':
            continue
        else:
            country_id = val['value']
            country_name = val.text
            country_data[country_name] = country_id

    with open('countrydata.json', 'w') as f:
        json.dump(country_data, f)
    print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Country IDs scraped!')

def getCountryId(country_name):
    with open('countrydata.json', 'r') as f:
        country_data = json.loads(f.read())
    try:
        country_id = country_data[country_name]
        return country_id
    except:
        print(Fore.RED + gettime() + ' [ERROR] -> Error getting country_id, check your country name in userdata.json!')


####################          Loading data and initializing other later used variables          ####################
with open('userdata.json', 'r') as f:
    userData = json.loads(f.read())

firstName = userData['firstName']
lastName = userData['lastName']
phoneNum = userData['phoneNum']
catchall = userData['catchall']
passwd = userData['passwd']
addyFirstLine = userData['addyFirstLine']
houseNum = userData['houseNum']
addySecondLine = userData['addySecondLine']
zipcode = userData['zipcode']
city = userData['city']
country_name = userData['country_name']
country_id = getCountryId(country_name)

headers = {
    'authority': 'www.solebox.com',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'referer': 'https://www.solebox.com/en/my-account/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type':'application/x-www-form-urlencoded',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }

linetwolist = ['apt', 'apartment', 'dorm', 'suite', 'unit', 'house', 'unt', 'room', 'floor']


####################          Main function          ####################
def generateAccount():
    ##########     Initializing a session & getting stoken     ##########
    print(gettime() + ' [STATUS] -> Account generation has started...')
    s = cfscrape.create_scraper()
    # s = requests.Session()
    if proxyList:
        s.proxies = random.choice(proxyList)
    s.get('https://www.solebox.com/', headers=headers)
    time.sleep(1)
    stoken = getStoken(s)
    if stoken is None:
        return
    time.sleep(0.5)
    s.get(url='https://www.solebox.com/en/my-account/', headers=headers)

    ##########     Jigging info     ##########
    global firstName, lastName, phoneNum, addyFirstLine, addySecondLine
    if jigFirstAndLast:
        firstName = get_first_name()
        lastName = get_last_name()
    elif jigFirst:
        firstName = get_first_name()
    if jigPhone:
        phoneNum = f'+420{random.randint(300,999)}{random.randint(300,999)}{random.randint(300,999)}'
    if jigFirstLineAddress:
        addyFirstLine = f'{2*(chr(random.randint(97,97+25)).upper() + chr(random.randint(97,97+25)).upper())} {addyFirstLine}'
    if jigSecondLineAddress:
        addySecondLine = f'{random.choice(linetwolist)} {random.randint(1,20)}{chr(random.randint(97,97+25)).upper()}'
    email = f'{get_first_name()}{random.randint(1,9999999)}@{catchall}'
    time.sleep(0.5)
    print(gettime() + ' [STATUS] -> Trying to create an account...')
    ##########     Configuring payload for registering and POSTing it to create an account     ##########
    register_payload = {
            'stoken': stoken,
            'lang': '1',
            'listtype': '',
            'actcontrol': 'account',
            'cl': 'user',
            'fnc': 'createuser',
            'reloadaddress': '',
            'blshowshipaddress': '1',
            'invadr[oxuser__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
            'invadr[oxuser__oxfname]': firstName,
            'invadr[oxuser__oxlname]': lastName,
            'invadr[oxuser__oxstreet]': addyFirstLine,
            'invadr[oxuser__oxstreetnr]': houseNum,
            'invadr[oxuser__oxaddinfo]': addySecondLine,
            'invadr[oxuser__oxzip]': zipcode,
            'invadr[oxuser__oxcity]': city,
            'invadr[oxuser__oxcountryid]': country_id,
            'invadr[oxuser__oxstateid]': '',
            # 'invadr[oxuser__oxbirthdate][day]': random.randint(0, 31),
            'invadr[oxuser__oxbirthdate][day]': '',
            # 'invadr[oxuser__oxbirthdate][month]': random.randint(0, 12),
            'invadr[oxuser__oxbirthdate][month]': '',
            # 'invadr[oxuser__oxbirthdate][year]': random.randint(1950, 2003),
            'invadr[oxuser__oxbirthdate][year]': '',
            'invadr[oxuser__oxfon]': phoneNum,
            'lgn_usr': email,
            'lgn_pwd': passwd,
            'lgn_pwd2': passwd,
            'userform': ''
        }

    register_post = s.post(url='https://www.solebox.com/index.php?lang=1&', headers=headers, data=register_payload, allow_redirects=True)
    if register_post.status_code in (302, 200):
        print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Successfully created an account.')
    else:
        print(Fore.RED + gettime() + ' [ERROR] -> ERROR occured: Unable to create an account.')
        return
    time.sleep(0.5)
    print(gettime() + ' [STATUS] -> Trying to update accounts shipping details.')    
    ##########     Updating shipping address     ##########
    s.get(url='https://www.solebox.com/en/my-address/', headers=headers)
    update_shipping_payload = {
        'stoken': stoken,
        'lang': '1',
        'listtype': '',
        'actcontrol': 'account_user',
        'fnc': 'changeuser_testvalues',
        'cl': 'account_user',
        'CustomError': 'user',
        'blshowshipaddress': '1',
        'invadr[oxuser__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
        'invadr[oxuser__oxfname]': firstName,
        'invadr[oxuser__oxlname]': lastName,
        'invadr[oxuser__oxstreet]': addyFirstLine,
        'invadr[oxuser__oxstreetnr]': houseNum,
        'invadr[oxuser__oxaddinfo]': addySecondLine,
        'invadr[oxuser__oxzip]': zipcode,
        'invadr[oxuser__oxcity]': city,
        'invadr[oxuser__oxcountryid]': country_id,
        'invadr[oxuser__oxstateid]': '',
        'changeClass': 'account_user',
        'oxaddressid': '-1',
        'deladr[oxaddress__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
        'deladr[oxaddress__oxfname]': firstName,
        'deladr[oxaddress__oxlname]': lastName,
        'deladr[oxaddress__oxcompany]': '',
        'deladr[oxaddress__oxstreet]': addyFirstLine,
        'deladr[oxaddress__oxstreetnr]': houseNum,
        'deladr[oxaddress__oxaddinfo]': addySecondLine,
        'deladr[oxaddress__oxzip]': zipcode,
        'deladr[oxaddress__oxcity]': city,
        'deladr[oxaddress__oxcountryid]': country_id,
        'deladr[oxaddress__oxstateid]': '',
        'deladr[oxaddress__oxfon]': phoneNum,
    }
    time.sleep(0.5)
    update_shipping_post = s.post(url='https://www.solebox.com/index.php?lang=1&', headers=headers, data=update_shipping_payload)
    if update_shipping_post.status_code in (302,200):
        print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Successfully updated accounts shipping details.')
        saveEmail(email, passwd)
    else:
        print(Fore.RED + gettime() + ' [ERROR] -> ERROR occured: Unable to edit shipping details.')
        saveNoShipEmail(email, passwd)


####################          Loading proxies          ####################
proxyList = []
try:
    loadProxyUserPass('proxies')
except:
    loadProxyIpAuth('proxies')

print(Style.BRIGHT + Fore.CYAN + 'SOLEBOX ACCOUNT GENERATOR + SHIPPING ADDRESS UPDATER')
totalproxies = len(proxyList)
if int(totalproxies) == 0:
    print('No proxies loaded.')
else:
    print('Loaded ' + Style.BRIGHT + f'{totalproxies}' + Style.NORMAL + ' proxies!')

####################          Generating accounts          ####################


##########     Checking if countryids are scraped     ##########
if os.stat('countrydata.json').st_size == 0:
    scrapeCountryIds()
##########     Generating the number of accounts specified     ##########

# generateAccount()
print('[STATUS] -> Account generation has started...')
if not proxyList:
    if how_many < 3:
        for acc in range(how_many):
            generateAccount()
    else:
        print(Fore.YELLOW + gettime() + ' [WARNING] -> You are trying to create more than 3 accounts with no proxies! Add some proxies and try again.')
# generateAccount()
else:
    threads = []
    for acc in range(how_many):
        t = threading.Thread(target=generateAccount)
        threads.append(t)
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()
        
