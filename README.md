# SoleboxAccountGenerator

This Python script creates Solebox accounts and **adds a shipping address to them**.
Sometimes it takes a couple of tries to make it successfully generate accounts, just make sure you have working proxies and give it a couple of tries.

**Use of proxies is highly recommended.**

DM me on Discord rtuna#4321 if you need any help setting this up.

## Before running:
1. Make sure you have Python (preferably 3.8.0) installed
2. download & unzip this folder, and `cd` to here
3. run `pip install -r requirements.txt`
4. Add your info into `userdata.json`

5. Edit this **in the code**:
    ```python3
    how_many = 3
    jigFirstAndLast = False #or True
    jigFirst = False #or True
    jigPhone = True #or False
    jigFirstLineAddress = True #or False
    jigSecondLineAddress = True #or False
    ```
## To run:
open your terminal, change your directory to this folder/repo and run:

- on Mac: `python soleboxaccgen.py`

- on Widnows: `py soleboxaccgen.py`
