#### made by: rtuna#4321 | @rTunaboss
#### Working on Python 3.8.0

####################          Importing necessary libraries          ####################

try:
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
    from discord_webhook import DiscordWebhook, DiscordEmbed

except:
    print('[FATAL ERROR] -> "Some dependencies are not installed."')
    print('!!! Make sure you read and do EVERYTHING in the "Before running" section of the README.md file on Github !!!')
    print('• Available from:\thttps://github.com/rtunaboss/SoleboxAccountGenerator')
    input()
    quit()

init(autoreset=True)

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
print('-------------------------------------')
print(Fore.YELLOW + '!!! IF YOU GET A LOT OF CLOUDFARE ERRORS, MAKE SURE YOU ARE ON THE LATEST VERSION !!!' )
print('https://github.com/rtunaboss/SoleboxAccountGenerator')
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

#-------------------------------- DO NOT MODIFY THE CODE BELOW UNLESS YOU KNOW WHAT YOU'RE DOING --------------------------------#

class logger:
    print_lock = threading.Lock()
####################          Defining non-account specific functions          ####################
def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    threadname = threading.currentThread().getName()
    threadname = str(threadname).replace('Thread', 'Task')
    now = '[' + str(now) + ']' + ' ' + '[' + str(threadname) + ']'
    return now

def send_webhook(webhook_url, email, passwd):
    hook = DiscordWebhook(url=webhook_url, username="rTuna's Solebox Gen", avatar_url='https://avatars1.githubusercontent.com/u/38296319?s=460&v=4')
    color=15957463

    embed = DiscordEmbed(
        title = 'Account successfully created!',
        color=color,
        url='https://github.com/rtunaboss/SoleboxAccountGenerator',
    )

    embed.set_footer(text=f'BONZAY Solebox • {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',icon_url='https://cdn.discordapp.com/attachments/527830358767566848/622854816120569887/Bonzay.png')
    embed.add_embed_field(name='Username', value=f'{email}')
    embed.add_embed_field(name='Password', value=f'||{passwd}||', inline=False)
    hook.add_embed(embed)
    hook.execute()


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
        with logger.print_lock:
            print(gettime() + ' [STATUS] -> Trying to scrape stoken...')
        index_url = 'https://www.solebox.com/en/my-account/'
        index_r = s.get(url=index_url, headers=headers)
        if 'captcha.js' in index_r.text:
            print(Fore.RED + gettime() + ' [ERROR] -> Encountered CloudFare.')
            return
        if index_r.status_code == 200:
            soup = bs(index_r.text, 'lxml')
            stoken = soup.find('input', {'name': 'stoken'})['value']
            with logger.print_lock:
                print(Fore.GREEN + Style.BRIGHT + gettime() + f' [SUCCESS] -> Successfully scraped stoken: {stoken} !')
            return stoken
        else:
            with logger.print_lock:
                print(Fore.RED + gettime() + ' [ERROR] -> Bad request. Satus code %d, unable to get stoken...' % index_r.status_code)
            return
    except:
        with logger.print_lock:
            print(Fore.RED + gettime() + ' [ERROR] -> Unable to get stoken.')

def scrapeCountryIds():
    country_data = {}
    with logger.print_lock:
        print(gettime() + ' [STATUS] -> Scraping country IDs...')
    s = cfscrape.create_scraper()
    r = s.get(url='https://www.solebox.com/', headers=headers)
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
    with logger.print_lock:
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
with open('useragents.txt', 'r') as f:
# with open('commonagents.txt', 'r') as f:
    useragents = f.read()
    useragents = useragents.split('\n')

with open('userdata.json', 'r') as f:
    userData = json.loads(f.read())

webhook_url = userData['webhook_url']
firstName = userData['firstName']
if firstName == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your firstName!')
    input()
    quit()
lastName = userData['lastName']
if lastName == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your lastName!')
    input()
    quit()
phoneNum = userData['phoneNum']
if phoneNum == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your phoneNum!')
    input()
    quit()
passwd = userData['passwd']
if passwd == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your passwd!')
    input()
    quit()
addyFirstLine = userData['addyFirstLine']
if addyFirstLine == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your addyFirstLine!')
    input()
    quit()
houseNum = userData['houseNum']
if houseNum == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your houseNum!')
    input()
    quit()
zipcode = userData['zipcode']
if zipcode == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your zipcode!')
    input()
    quit()
city = userData['city']
if city == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your city!')
    input()
    quit()
country_name = userData['country_name']
if country_name == '':
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your userdata.json, you forgot to fill in your country_name!')
    input()
    quit()

stateUS = userData['stateUS']
if len(stateUS) > 2:
    with logger.print_lock:
        print(gettime() + ' [ERROR] -> Check your State settings! Correct formatting: "NY" or "TX"')

addySecondLine = userData['addySecondLine']
catchall = userData['catchall']
if catchall == '':
    catchall = 'gmail.com'
if '@' in catchall:
    catchall = catchall.replace('@', '')
    
country_id = getCountryId(country_name)
if country_id == None:
    input()
    quit()



headers = {
    'authority': 'www.solebox.com',
    'method': 'GET',
    'path': '/',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6',
    # 'cache-control': 'no-cache',
    # 'referer': 'http://www.solebox.com/',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'upgrade-insecure-requests': '1',
}



# headers = {
#     # 'authority': 'www.solebox.com',
#     # 'method': 'GET',
#     # 'path': '/',
#     # 'scheme': 'https',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-encoding': 'gzip, deflate',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6',
#     # 'cache-control': 'no-cache',
#     # 'sec-fetch-mode': 'navigate',
#     'Connection': 'keep-alive',
#     # 'sec-fetch-site': 'none',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
# }

# :method: GET
# :scheme: https
# :authority: www.solebox.com
# :path: /mein-konto/
# Cookie: cto_bundle=vmAr8F9ianNlb1E1VWp5a3hSNTY5QWV3SkxjVFpMZVZMTEpoY3BHaWFvdmx3NSUyQktqdk94aHlHNllXU2tZV3BiejhSdFNCTHVvTmVRT25Ub0xtenVSSDNVbjJ6RmY4Qll4UEFPNVpHMHMlMkI4dFA2a1FNJTJCMmp2UXJBN0x3VFliQVByeEFZbw; _px3=9014804bb6db7c387f7e5d0ffe5cd08880e3f9d5cae56e7871b1484d9e0c286e:rnBMvmhhOnRtTqb6UInpqUJaIa72Z+TT09RJyjPow2DBhXtNg4+DI8AMigmFp7+cWb2KO5IdxJE2pQY0Z8JgWg==:1000:vE+U1gmTOT1uwX7ZOucNgyhUntNrh1IwuW1puaZliq1R6jgpAEKFsZ0nStDBwbDzHRy7AC8mhQljic+jK6M0u5cf5PfpEhwwyEAIAk8UBMqHqNx9JzOv9J5swyCrF70J51l2fS33Lfpnh8bkSZV9sBcxqCAcgsHQV7o4r3PjNkA=; __utma=1.1099094876.1576941685.1576941685.1576941685.1; __utmb=1.2.10.1576941685; __utmc=1; __utmz=1.1576941685.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); px-abgroup=A; px-abper=100; language=0; _fbp=fb.1.1576941685612.724889629; _pxvid=8d430e2f-2405-11ea-ac46-0242ac12000a; cto_lwid=54e30eff-8413-44ae-8c4f-ac1166ee2436; __utmt=1; displayedCookiesNotification=1; mlid=undefined
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Encoding: gzip, deflate, br
# Host: www.solebox.com
# User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1
# Accept-Language: en-us
# Referer: https://www.solebox.com/
# Connection: keep-alive

linetwolist = ['apt', 'apartment', 'dorm', 'suite', 'unit', 'house', 'unt', 'room', 'floor']

####################          Main function          ####################
def generateAccount():
    ##########     Initializing a session & getting stoken     ##########
    useragent = random.choice(useragents)
    headers['user-agent'] = useragent
    # headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    with logger.print_lock:
        print(gettime() + ' [STATUS] -> Account generation has started...')
    # s = cfscrape.create_scraper()
    s = requests.Session()
    if proxyList:
        proxy_is_bad = True
        while proxy_is_bad:
            s.proxies = random.choice(proxyList)
            with logger.print_lock:
                print(gettime() + ' [STATUS] -> Checking proxy...')
            test = s.get('https://www.solebox.com/', headers=headers)
            if test.status_code in (302, 200):
                with logger.print_lock:
                    print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Proxy working...')
                proxy_is_bad = False
            elif 'captcha.js' in test.text:
                with logger.print_lock:
                    print(Fore.RED + gettime() + ' [ERROR] -> Encountered CloudFare, rotating proxy...')
            else:
                with logger.print_lock:
                    print(Fore.RED + gettime() + ' [ERROR] -> Proxy banned, rotating proxy...')
            time.sleep(1)
    stoken = getStoken(s)
    if stoken is None:
        return
    time.sleep(1)
    s.get(url='https://www.solebox.com/en/open-account/', headers=headers)
    ##########     Jigging info     ##########
    global firstName, lastName, phoneNum, jiggedFirstLineAddress, jiggedSecondLineAddress
    if jigFirstAndLast:
        firstName = get_first_name()
        lastName = get_last_name()
    elif jigFirst:
        firstName = get_first_name()
    if jigPhone:
        phoneNum = f'+1{random.randint(300,999)}{random.randint(300,999)}{random.randint(300,999)}'
    if jigFirstLineAddress:
        jiggedFirstLineAddress = f'{2*(chr(random.randint(97,97+25)).upper() + chr(random.randint(97,97+25)).upper())} {addyFirstLine}'
    else:
        jiggedFirstLineAddress = addyFirstLine
    if jigSecondLineAddress:
        jiggedSecondLineAddress = f'{random.choice(linetwolist)} {random.randint(1,20)}{chr(random.randint(97,97+25)).upper()}'
    else:
        jiggedSecondLineAddress = addySecondLine
    email = f'{get_first_name()}{random.randint(1,9999999)}@{catchall}'
    time.sleep(0.5)
    with logger.print_lock:
        print(gettime() + ' [STATUS] -> Trying to create an account...')
    ##########     Configuring payload for registering and POSTing it to create an account     ##########
    register_payload = {
            'stoken': stoken,
            'lang': '1',
            'listtype': '',
            'actcontrol': 'register',
            'fnc': 'registeruser',
            'cl': 'register',
            'lgn_cook' : 0,
            'reloadaddress': '',
            'blshowshipaddress': 1,
            'option' : 3,
            'invadr[oxuser__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
            'invadr[oxuser__oxfname]': firstName,
            'invadr[oxuser__oxlname]': lastName,
            'invadr[oxuser__oxstreet]': jiggedFirstLineAddress,
            'invadr[oxuser__oxstreetnr]': houseNum,
            'invadr[oxuser__oxaddinfo]': jiggedSecondLineAddress,
            'invadr[oxuser__oxzip]': zipcode,
            'invadr[oxuser__oxcity]': city,
            'invadr[oxuser__oxcountryid]': country_id,
            'invadr[oxuser__oxstateid]': stateUS,
            'invadr[oxuser__oxbirthdate][day]': random.randint(1, 31),
            'invadr[oxuser__oxbirthdate][month]': random.randint(1, 12),
            'invadr[oxuser__oxbirthdate][year]': random.randint(1950, 2003),
            'invadr[oxuser__oxfon]': phoneNum,
            'lgn_usr': email,
            'lgn_pwd': passwd,
            'lgn_pwd2': passwd,
            'save' : 'Save',
        }

    register_post = s.post(url='https://www.solebox.com/index.php?lang=1&', headers=headers, data=register_payload)
    if register_post.status_code in (302, 200):
        with logger.print_lock:
            print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Successfully created an account.')
    else:
        with logger.print_lock:
            print(Fore.RED + gettime() + ' [ERROR] -> ERROR %d occurred: Unable to create an account.' % register_post.status_code)
        return
    time.sleep(1)
    with logger.print_lock:
        print(gettime() + ' [STATUS] -> Trying to update accounts shipping details.')    
    ##########     Updating shipping address     ##########
    s.get(url='https://www.solebox.com/en/my-address/', headers=headers)
    
    update_shipping_payload = {
        'MIME Type': 'application/x-www-form-urlencoded',
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
        'invadr[oxuser__oxstreet]': jiggedFirstLineAddress,
        'invadr[oxuser__oxstreetnr]': houseNum,
        'invadr[oxuser__oxaddinfo]': jiggedSecondLineAddress,
        'invadr[oxuser__oxzip]': zipcode,
        'invadr[oxuser__oxcity]': city,
        'invadr[oxuser__oxcountryid]': country_id,
        'invadr[oxuser__oxstateid]': stateUS,
        'invadr[oxuser__oxfon]': phoneNum,
        'changeClass': 'account_user',
        'oxaddressid': '-1',
        'deladr[oxaddress__oxsal]': random.choice(['MR', 'MRS']),  # MR OR MRS
        'deladr[oxaddress__oxfname]': firstName,
        'deladr[oxaddress__oxlname]': lastName,
        'deladr[oxaddress__oxcompany]': '',
        'deladr[oxaddress__oxstreet]': jiggedFirstLineAddress,
        'deladr[oxaddress__oxstreetnr]': houseNum,
        'deladr[oxaddress__oxaddinfo]': jiggedSecondLineAddress,
        'deladr[oxaddress__oxzip]': zipcode,
        'deladr[oxaddress__oxcity]': city,
        'deladr[oxaddress__oxcountryid]': country_id,
        'deladr[oxaddress__oxstateid]': stateUS,
        'deladr[oxaddress__oxfon]': phoneNum,
        'userform' : '',
    }

    time.sleep(1)
    update_shipping_post = s.post(url='https://www.solebox.com/index.php?lang=1&', headers=headers, data=update_shipping_payload)
    if update_shipping_post.status_code in (302,200):
        with logger.print_lock:
            print(Fore.GREEN + Style.BRIGHT + gettime() + ' [SUCCESS] -> Successfully updated accounts shipping details.')
        saveEmail(email, passwd)
        if webhook_url:
            send_webhook(webhook_url, email, passwd)
    else:
        with logger.print_lock:
            print(Fore.RED + gettime() + ' [ERROR] -> ERROR occurred: Unable to edit shipping details.')
        saveNoShipEmail(email, passwd)


####################          Loading proxies          ####################
proxyList = []
try:
    loadProxyUserPass('proxies')
except:
    loadProxyIpAuth('proxies')

with logger.print_lock:
    print(Style.BRIGHT + Fore.CYAN + 'SOLEBOX ACCOUNT GENERATOR + SHIPPING ADDRESS UPDATER')
totalproxies = len(proxyList)
if int(totalproxies) == 0:
    with logger.print_lock:
        print('No proxies loaded.')
else:
    with logger.print_lock:
        print('Loaded ' + Style.BRIGHT + f'{totalproxies}' + Style.NORMAL + ' proxies!')

####################          Generating accounts          ####################


##########     Checking if countryids are scraped     ##########
if os.stat('countrydata.json').st_size == 0:
    scrapeCountryIds()
##########     Generating the number of accounts specified     ##########

print('[STATUS] -> Account generation has started...')
if not proxyList:
    if how_many < 3:
        for acc in range(how_many):
            generateAccount()
    else:
        with logger.print_lock:
            print(Fore.YELLOW + gettime() + ' [WARNING] -> You are trying to create more than 3 accounts with no proxies! Add some proxies and try again.')
# generateAccount()
else:
    for acc in range(how_many):
        t = threading.Thread(target=generateAccount)
        threads.append(t)
        t.start()
        time.sleep(0.5)
            
    for t in threads:
        t.join()
