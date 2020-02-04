# Solebox account generator




This Python script creates Solebox accounts and **adds a shipping address to them**.
 
**Use of proxies is highly recommended.**

DM me on Discord rtuna#4321 if you need any help setting this up. **BEFORE DMing ME, READ THROUGH THIS FILE**

## Before running:
1. Make sure you have Python (preferably 3.8.0) installed
2. download & unzip this the zip you donwloaded, open your CMD/Terminal and `cd` to this folder.
3. run `pip install -r requirements.txt`
4. Add your info into `userdata.json`

5. (ADVANCED) Feel free to edit this **in the code**:
    ```python3
    jigFirstAndLast = False #or True
    jigFirst = False #or True
    jigPhone = True #or False
    jigFirstLineAddress = True #or False
    jigSecondLineAddress = True #or False
    ```

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
    "firstName": "John",
    "lastName": "Doe",
    "phoneNum": "123456789",
    "catchall": "catchall.com",
    "passwd": "myPassword",
    "addyFirstLine": "Oxford Streed",
    "houseNum": "33",
    "addySecondLine": "apt 6",
    "zipcode": "FA6 S2C",
    "city": "London",
    "country_name": "United Kingdom",
    "stateUS": "",
    "webhook_url" : "https://discordapp.com/api/webhooks/..."
}
```
5. Script was working fine but now I just get `403` errors all the time?
     - Regenerate proxies (make sure you try both static and rotating)
     - if that doesn't help, contact me. Solebox most likely changed their security and an update will be needed.

## To run:
open your terminal, change your directory to this folder/repo and run:

- on Mac: `python3 soleboxaccgen.py`

- on Widnows: `py soleboxaccgen.py`

## Where do I find generated accounts?
- If everything goes smoothly, accounts should be in `valid_emails.txt` as well as if you have a webhook setup, you'll get a Discord notification.
- if an error occurs when trying to update a shipping address, they'll be in `no_ship_addy_emails.txt` and you'll need to update shipping address manually (or just gen new ones 😝)

This is how it should look like when you run it:
![How it should look like](https://i.imgur.com/Tc0GxtO.png)


## Notes:
- If you don't have a catchall, feel free to leave the catchall field blank but you won't get confirmation emails (it will just create an account with a random gmail)

## FAQ:
- What is `cd` and how do I use it?
    - From [wikipedia](https://en.wikipedia.org/wiki/Cd_(command)): "the `cd` command is a command-line shell command used to change the current working directory" -  so what you need to do is change your working directory, to the Folder (or directory) of this script.
- How do I install Python?
    - [This should help you](https://realpython.com/installing-python/)
- I am getting `[ERROR] -> Bad request. Satus code 403` or `[ERROR] -> Encountered CloudFare...` all the time, what do I do?
    - Keep trying and or switch proxies. This also happens frequently when the site is under a heavy load (When a restock/drop happens etc.)
