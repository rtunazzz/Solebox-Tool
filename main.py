# -------------------------------------------------------------------------------- SETUP & IMPORTS -------------------------------------------------------------------------------- #

print(r'''
 ____    ____   _   _  ______       __     __ _        
|  _ \  / __ \ | \ | ||___  /    /\ \ \   / /(_)       
| |_) || |  | ||  \| |   / /    /  \ \ \_/ /  _   ___  
|  _ < | |  | || . ` |  / /    / /\ \ \   /  | | / _ \ 
| |_) || |__| || |\  | / /__  / ____ \ | | _ | || (_) |
|____/  \____/ |_| \_|/_____|/_/    \_\|_|(_)|_| \___/ 
------
https://github.com/rtunaboss/SoleboxAccountGenerator
• developed by: rtuna#4321 | @rTunaboss
• for personal use only
------''')

from colorama import Fore, Style, init
import threading
import time

from bonzay_pkg.solebox import SoleboxGen
from bonzay_pkg.reusable import readFile

init(autoreset=True)
print_lock = threading.Lock()

# -------------------------------------------------------------------------------- FUNCTIONS -------------------------------------------------------------------------------- #

def SoleboxGenerateAccount():
    gen = SoleboxGen()
    gen.generateAccount(print_lock)
    gen.updateShippingAddress(print_lock, new_account=True)

def SoleboxCheckAccount(email, passwd):
    gen = SoleboxGen()
    gen.checkAccount(print_lock, email, passwd)

def SoleboxCheckShippingAddress(email, passwd):
    gen = SoleboxGen()
    gen.checkShippingAddress(print_lock, email=email, passwd=passwd)

def SoleboxUpdateShippingExistingAccount(email, passwd):
    gen = SoleboxGen()
    gen.updateShippingAddress(print_lock, new_account=False, email=email, passwd=passwd)

def start():
    print(Style.BRIGHT + Fore.CYAN + "Welcome to BONZAY Tools!")
    print(Fore.LIGHTYELLOW_EX + "Please select an option:")
    print(Fore.LIGHTYELLOW_EX + "[1] - Generate Solebox accounts")
    print(Fore.LIGHTYELLOW_EX + "[2] - Check valid Solebox accounts")
    print(Fore.LIGHTYELLOW_EX + "[3] - Check Solebox accounts' shipping addresses")
    print(Fore.LIGHTYELLOW_EX + "[4] - Update Solebox shipping addresses")
    print("------")

    # ----- Get input (which option) ----- #
    while(1):
        option = input()
        try:
            option = int(option)
            if type(option) is int:
                break
        except:
            print("Not an integer. Try again:")


    # ---------------------------------------- [1] - Solebox Account Generator ---------------------------------------- #
    if option == 1:
        # print("\n"*100)
        print(Style.BRIGHT + Fore.CYAN + "SOLEBOX ACCOUNT GENERATOR")

        # ----- Get input (how many accs to generate) ----- #
        how_many = None
        while(1):
            try:
                how_many = int(input("How many accounts would you like to create?\n"))
            except ValueError:
                print("That is not an integer. Try again...")
            if type(how_many) == int:
                break
        print("Starting to generate Solebox accounts...")
        threads = []
        for _ in range(how_many):
            t = threading.Thread(target=SoleboxGenerateAccount)
            threads.append(t)
            t.start()
            time.sleep(0.5)
                
        for t in threads:
            t.join()
        print("\nFinished generating Solebox accounts.")

    # ---------------------------------------- [2] - Solebox Valid Account Checker ---------------------------------------- #
    if option == 2:
        # ----- Load all accounts with shipping ----- #
        print("Loading accounts from solebox-valid.txt")
        f = readFile("./accounts/solebox-valid.txt")
        accounts = f.split('\n')

        print("Starting to check valid Solebox accounts...")
        # ----- Create one thread for each account ----- #
        threads = []
        for account in accounts:
            if account.strip() == '':
                continue
            # check if there's no newline in password
            username, password = account.split(':')
            t = threading.Thread(target=SoleboxCheckAccount, args=(username, password))
            threads.append(t)
            t.start()
            time.sleep(0.5)
                
        for t in threads:
            t.join()
        print("\nFinished checking Solebox accounts.")


    # ---------------------------------------- [3] - Solebox Shipping Address Checker ---------------------------------------- #
    if option == 3:
        # ----- Load all accounts with shipping ----- #
        print("Loading accounts from solebox-valid.txt")
        f = readFile("./accounts/solebox-valid.txt")
        accounts = f.split('\n')
    
        print("Starting to check Solebox account's shipping addresses.")
        # ----- Create one thread for each account ----- #
        threads = []
        for account in accounts:
            if account.strip() == '':
                continue
            # check if there's no newline in password
            username, password = account.split(':')
            t = threading.Thread(target=SoleboxCheckShippingAddress, args=(username, password))
            threads.append(t)
            t.start()
            time.sleep(0.5)
                
        for t in threads:
            t.join()
        print("\nFinished checking Solebox account's shipping addresses.")

    # ---------------------------------------- [4] - Solebox Shipping Address Updater ---------------------------------------- #
    if option == 4:
        return #TODO NOT WORKING
        # ----- Load all accounts with NO shipping ----- #
        print("Loading accounts from solebox-no-shipping.txt")
        f = readFile("./accounts/solebox-no-shipping.txt")
        accounts = f.split('\n')
    
        print("Starting to add addresses to Solebox accounts...")
        # ----- Create one thread for each account ----- #
        threads = []
        for account in accounts:
            # check if there's no newline in password
            username, password = account.split(':')
            t = threading.Thread(target=SoleboxUpdateShippingExistingAccount, args=(username, password))
            threads.append(t)
            t.start()
            time.sleep(0.5)
                
        for t in threads:
            t.join()
        print("\nFinished adding addresses to Solebox accounts.")


# -------------------------------------------------------------------------------- RUNNING -------------------------------------------------------------------------------- #
start()

# SoleboxUpdateShippingExistingAccount(email, passwd) #TODO NOT WORKING