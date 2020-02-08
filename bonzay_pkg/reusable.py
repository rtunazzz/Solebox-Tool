import datetime
import threading
import os
import json
import requests

# ---------- Basic Functions ---------- #

def getTime():
    """
    Simple function that returns a string containing info about current time and current thread (name).

    Args:
        None
    
    Returns:
        now {str}   - String in the format of '[time] [threadname] '
    """
    now = str(datetime.datetime.now().time())
    now = now[:-3] #only want 3 decimal places
    thread_name = threading.currentThread().getName()
    thread_name = thread_name.replace('Thread', 'Task')
    now = f'[{now}] [{thread_name}] '
    return now

def logMessage(status, message):
    # logging can be setup later if needed
    if status != "debug":
        status = f"[{status}]"
        print(getTime() + f"{status.upper():<9} -> {message}")

# ---------- Proxy Functions ---------- #

def loadProxies(filename):
    """
    Reads proxies from a file and parses them to be ready to use with Python `requests` library

    Args:
        filename {str}                      - Name of the file (.txt) where are the proxies located
    Returns:
        formatted_proxy_list {list [dict]}  - List of dictionaries, that are formatted and ready-to-use with Python

    Notes:
        *can be read from a file and split by a separator (usually new line)
    """
    
    with open(filename, 'r') as f:
        file_contents = f.read()
        file_contents = file_contents.split('\n')
    formatted_proxy_list = []
    logMessage("info", "Parsing proxies")
    try:
        try:
            # Userpass
            for i in range(0, len(file_contents)):
                if ':' in file_contents[i]:
                    tmp = file_contents[i]
                    tmp = tmp.split(':')
                    proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                            'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
                    formatted_proxy_list.append(proxies)
        except:
            # IP auth
            for n in range(0, len(file_contents)):
                if ':' in file_contents[n]:
                    temp = file_contents[n]
                    proxies = {'http': 'http://' + temp,  'https': 'http://' + temp}
                    formatted_proxy_list.append(proxies)

        logMessage("info", "Successfully parsed proxies.")
    except Exception as e:
        logMessage("critical", f"Failed to parse proxies. Exception: {e}")
        return None
    return formatted_proxy_list

def isProxyGood(url: str, proxy: dict, headers: dict):
    """
    A simple proxy tester to make sure a proxy is working (can see) on a website.

    Args:
        url     - URL where you want to test the proxy
        proxy   - Proxy that you want to test
        headers - Headers that you want to test with the proxy
    
    Returns:
        True or False
    """
    logMessage("debug", f"Testing proxy for {url}")
    test = requests.get(url=url, headers=headers, proxies=proxy)
    if test.status_code in (302, 200):
        logMessage("debug", f"Proxy working for {url}!")
        return True
    elif 'captcha.js' in test.text:
        logMessage("info", "Encounered captcha, rotating proxy...")
        return False
    else:
        logMessage("info", "Proxy banned, rotating proxy...")
        return False

# ---------- File management Functions ---------- #

def readFile(filename: str):
    """Reads from a file"""
    filetype = filename.split('.')[-1]
    if filetype == 'json':
        if os.stat(filename).st_size == 0:
            return {}
        with open(filename, 'r') as f:
            j = json.load(f)
        return j

    elif filetype == 'txt':
        with open(filename, 'r') as f:
            return f.read()
    else:
        print(f"[ERROR - readFile] - Error reading {filename} - unsupported filetype.")

def saveIntoFile(filename: str, data):
    """Saves data into a file"""
    filetype = filename.split('.')[-1]

    if filetype == 'json' and type(data) == dict:
        with open(filename, 'w') as f:
            json.dump(data, f)
    elif filetype == 'txt':
        with open(filename, 'w') as f:
            f.write(data)
    else:
        print(f"[ERROR - saveIntoFile] - Error writing into {filename}.")

def appendIntoFile(filename: str, data):
    """Appends data into a file"""
    filetype = filename.split('.')[-1]

    if filetype == 'json' and type(data) == dict:
        with open(filename, 'a') as f:
            json.dump(data, f)
    elif filetype == 'txt':
        with open(filename, 'a') as f:
            f.write(data)
    else:
        print(f"[ERROR - appendIntoFile] - Error writing into {filename}.")

def loadUseragents():
    """
    Loads useragents from a file and sets the file contents to global variable.
    
    IMPORTANT: files should be located in the same directory, under `useragents` folder.

    Args:
        - None
    
    Returns:
        - A list, (with either 1 or 2 values)
            - 2 values
                • [0] = desktop_useragents
                • [1] = mobile_useragents
            - 1 value
                • [0] = useragents
    """
    useragent_type_list = []
    try:
        desktop_useragents = readFile("./useragents/desktop-useragents.txt")
        desktop_useragents = desktop_useragents.split('\n')

        mobile_useragents = readFile("./useragents/mobile-useragents.txt")
        mobile_useragents = mobile_useragents.split('\n')

        useragent_type_list.append(desktop_useragents)
        useragent_type_list.append(mobile_useragents)

    except:
        useragents = readFile("./useragents/useragents.txt")
        useragents = useragents.split('\n')
        useragent_type_list.append(useragents)

    return useragent_type_list