# SoleboxAccountGenerator

This Python script creates Solebox accounts and **adds a shipping address to them**.
Sometimes it takes a couple of tries to make it successfully generate accounts, just make sure you have working proxies and give it a couple of tries. Solebox is very strict and will temporarily ban you/you'll run into Cloudfare very often...

**Use of proxies is highly recommended.**

DM me on Discord rtuna#4321 if you need any help setting this up.

## Before running:
1. Make sure you have Python (preferably 3.8.0) installed
2. download & unzip this folder, and `cd` to here
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
## To run:
open your terminal, change your directory to this folder/repo and run:

- on Mac: `python3 soleboxaccgen.py`

- on Widnows: `py3 soleboxaccgen.py`

## Where do I find generated accounts?
- If everything goes smoothly, accounts should be in `valid_emails.txt`
- if an error occurs when trying to update a shipping address, they'll be in `no_ship_addy_emails.txt` and you'll need to update shipping address manually (or just gen new ones 😝)

This is how it should look like when you run it:
![How it should look like](https://i.imgur.com/hc8UXS5.png)


## Notes:
- If you don't have a catchall, feel free to leave the catchall field blank but you won't get confirmation emails (it will just create an account with a random gmail)
