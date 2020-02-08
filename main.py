# -------------------------------------------------------------------------------- SETUP & IMPORTS -------------------------------------------------------------------------------- #

print(r'''
 ____     ___    _   _   _____     _     __   __      _         
| __ )   / _ \  | \ | | |__  /    / \    \ \ / /     (_)   ___  
|  _ \  | | | | |  \| |   / /    / _ \    \ V /      | |  / _ \ 
| |_) | | |_| | | |\  |  / /_   / ___ \    | |    _  | | | (_) |
|____/   \___/  |_| \_| /____| /_/   \_\   |_|   (_) |_|  \___/ 
------
https://github.com/rtunaboss/SoleboxAccountGenerator
• developed by: rtuna\#4321 | @rTunaboss
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
    print("Starting to generate accounts...")
    gen = SoleboxGen()
    gen.generateAccount(print_lock)
    gen.updateShippingAddress(print_lock, new_account=True)
    print("Finished generating accounts.")

def SoleboxUpdateShippingExistingAccount():
    print("Starting to update shipping addresses...")
    gen = SoleboxGen()
    gen.updateShippingAddress(print_lock, new_account=False)
    print("Finished updating addresses...")

def start():
    print(Style.BRIGHT + Fore.CYAN + "Welcome to BONZAY Tools!")
    print(Fore.LIGHTYELLOW_EX + "Please select an option:")
    print(Fore.LIGHTYELLOW_EX + "[1] - Generate Solebox accounts")
    print(Fore.LIGHTYELLOW_EX + "[2] - Check Solebox counts")
    print(Fore.LIGHTYELLOW_EX + "[3] - Check Solebox shipping addresses")
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
        
        threads = []
        for _ in range(how_many):
            t = threading.Thread(target=SoleboxGenerateAccount)
            threads.append(t)
            t.start()
            time.sleep(0.5)
                
        for t in threads:
            t.join()

    # ---------------------------------------- [2] - Solebox Account Checker ---------------------------------------- #
    if option == 2:
        # ----- Load all accounts ----- #
        f = readFile("./accounts/solebox-no-shipping.txt")
        accounts = f.split('\n')
        # ----- Create one thread for each account ----- #
        # threads = []
        # for _ in range(how_many):
        #     t = threading.Thread(target=SoleboxGenerateAccount)
        #     threads.append(t)
        #     t.start()
        #     time.sleep(0.5)
                
        # for t in threads:
        #     t.join()


    # ---------------------------------------- [3] - Solebox Shipping Address Checker ---------------------------------------- #
    if option == 3:
        pass

    # ---------------------------------------- [4] - Solebox Shipping Address Updater ---------------------------------------- #
    if option == 4:
        pass


# -------------------------------------------------------------------------------- RUNNING -------------------------------------------------------------------------------- #
# start()
