<p align="center"><img width=80% src="https://i.imgur.com/IGGUkII.png"></p>

## Updates
If you would like to stay up to date regarding any future updates, follow me on [Twitter](https://twitter.com/rtunazzz)!

## Before you start
- Use of proxies is **NECESSARY**.
- If you can't set it up or you are having problems, **read through this file** and if you are still struggling after that, feel free to message me on Discord (`rtuna#4321`)

## Setup
1. Make sure you have Python (preferably 3.8+) installed
2. download & unzip this the zip you donwloaded, open your CMD/Terminal and `cd` to this folder.
3. run `pip install -r requirements.txt`
4. Add your info into `userdata.json`
5. Add proxies into `proxies.txt`
6. Feel free to turn on/off any "jigging" in the `userdata.json` but **for some reason if you set `jig_first_line` to false, you'll run into errors and most likely won't be able to generate any accounts!**

## Running

After you set everything up (see above), open your terminal, change your directory to this folder/repo (if you haven't done already) and run:

- on Mac: `python3 main.py`

- on Widnows: `py main.py`

## Common errors

1. The script closes itself
    -  You didn't follow the instructions and you are running it the wrong way. Follow [these steps](https://github.com/rtunazzz/Solebox-Tool#before-running).
2. `No module named XXX` = you don't have some of the dependencies installed. Make sure you did everything in [Before running](https://github.com/rtunazzz/Solebox-Tool#before-running). If that doesn't help, try running:
     - on Windows `py -m pip install -r requirements.txt`
     - on Mac `python3 -m pip install -r requirements.txt`

3. `'pip' is not recognized as an internal or external command, operable program or batch file.` or anything similar to that
     - on Windows `py -m pip install -r requirements.txt`
     - on Mac `python3 -m pip install -r requirements.txt`
4. Anything related to a `keyerror XXX` = There is something wrong with your `userdata.json` file. Make sure **there are no extra spaces and that you didn't delete any commas!** It should be filled in like this:
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

## FAQ
### What is `cd` and how do I use it?
Check out [this](https://www.techwalla.com/articles/how-to-use-quotcdquot-command-in-command-prompt-window) article.
### How do I install Python?
[This should help you install it](https://realpython.com/installing-python/)
### I am getting `[ERROR] -> Encountered CloudFare` all the time, what do I do?
Switch proxies or wait a bit and try again. **This also happens frequently when the site is under a heavy load** (When a restock/drop happens etc.)
### Where do I find generated accounts?
If everything goes smoothly, accounts will be in the **accounts folder** in `solebox-valid.txt` as well as if you have a webhook set up, you'll get a Discord notification. Accounts with no shipping address are saved into `solebox-no-shipping.txt`.


Made by [__rtuna__](https://twitter.com/rtunazzz).