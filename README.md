<p align="center"><img width=50% src="https://i.imgur.com/xncrVHK.png"></p>




## Update Feb/8/2020:
I completely rewrote the whole generator, it can now also **check if accounts are valid** (Accounts to check are loaded from `solebox-valid.txt`) and **check if an account has a shipping address** (accounts also get loaded from `solebox-valid.txt`)

# Account Generator
Here is a [demo](https://i.imgur.com/eEcF5R0.mp4)

**Use of proxies is NECESSARY.**

DM me on Discord rtuna#4321 if you need any help setting this up. **BEFORE DMing ME, READ THROUGH THIS FILE**

## Before running:
1. Make sure you have Python (preferably 3.8.0) installed
2. download & unzip this the zip you donwloaded, open your CMD/Terminal and `cd` to this folder.
3. run `pip install -r requirements.txt`
4. Add your info into `userdata.json`
5. Feel free to turn on/off any "jigging" in the `userdata.json` but **for some reason if you set `jig_first_line` to false, you'll run into errors and most likely won't be able to generate any accounts. Feel free to try it though! **

## To run:
open your terminal, change your directory to this folder/repo and run:

- on Mac: `python3 main.py`

- on Widnows: `py main.py`

## Common errors:
1. The script closes itself after you input the number of accounts you want to generate? YOU DIDN'T FOLLOW THE INSTURCTIONS AND YOU'RE RUNNING IT THE WRONG WAY, FOLLOW [THESE STEPS](https://github.com/rtunaboss/SoleboxAccountGenerator#before-running)
2. `[FATAL ERROR] -> "Some dependencies are not installed."` = you don't have any of the dependencies installed. Make sure you did everything in [Before running](https://github.com/rtunaboss/SoleboxAccountGenerator#before-running). If that doesn't fix it, try running:
     - on Windows `py -m pip install -r requirements.txt`
     - on Mac `python3 -m pip install -r requirements.txt`
     
3. `'pip' is not recognized as an internal or external command, operable program or batch file.` or anything related to this -> either you don't have Python in Path (`setx PATH "%PATH%;C:\Python38\Scripts"` - ONLY IF YOU'RE ON WINDOWS). If that doesn't help, try running:
     - on Windows `py -m pip install -r requirements.txt`
     - on Mac `python3 -m pip install -r requirements.txt`
4. I keep getting `keyerror firstname` = you replaced something you weren't supposed to replace in the `userdata.json` file. Make sure it's filled in like this:
```json
{
    "profile" : {
        "first_name": "John",
        "last_name": "Doe",
        "phone_num": "+1420690690",
        "catchall": "mycatchall.com",
        "passwd": "PA$$WORD",
        "address_first_line": "Washington Street",
        "house_number": "123",
        "address_second_line": "Apt 33",
        "zipcode": "10000",
        "city": "New York",
        "country_name": "United States",
        "us_state": "NY",
        "webhook_url" : "https://discordapp.com/api/webhooks/..." //can be left blank
    },
    "settings": {
        "jig_name": true,
        "jig_first_line": true,
        "jig_second_line": true,
        "jig_phone_number": true
    }
}
```
5. Script was working fine but now I just get `403` errors all the time?
     - Regenerate proxies (make sure you try both static and rotating)
     - if that doesn't help, contact me. Solebox most likely changed their security and an update will be needed.

## Where do I find generated accounts?
- If everything goes smoothly, accounts should be in the **accounts folder** in `solebox-valid.txt` as well as if you have a webhook setup, you'll get a Discord notification.
- if an error occurs when trying to update a shipping address, they'll be in the **accounts folder** `solebox-no-shipping.txt` and you'll need to update shipping address manually (or just gen new ones 😝)


## Notes:
- If you don't have a catchall, feel free to leave the catchall field blank but you won't get confirmation emails (it will just create an account with a random gmail)

## FAQ:
- What is `cd` and how do I use it?
    - From [wikipedia](https://en.wikipedia.org/wiki/Cd_(command)): "the `cd` command is a command-line shell command used to change the current working directory" -  so what you need to do is change your working directory, to the Folder (or directory) of this script.
- How do I install Python?
    - [This should help you](https://realpython.com/installing-python/)
- I am getting `[ERROR] -> Bad request. Satus code 403` or `[ERROR] -> Encountered CloudFare...` all the time, what do I do?
    - Keep trying and or switch proxies. This also happens frequently when the site is under a heavy load (When a restock/drop happens etc.)
