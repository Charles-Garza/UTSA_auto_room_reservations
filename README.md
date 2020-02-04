# Automatated study room reservations
This is a program designed around automation that handles reserving study rooms automatically at the University of Texas at San Antonio.

**Dependencies needed:**

- Python 3

- chromedriver/chromium for selenium

- PyQt5

**Getting started:**
    
First you must download and install the necessary dependencies.

The instructions to do so are as follows:

1. Step 1:

    You can download chromium from [here](https://chromedriver.chromium.org/downloads).

2. Step 2:

    **MacOs:**
    You can follow [these](https://www.swtestacademy.com/install-chrome-driver-on-mac/) instructions provided to install.

    **Windows:**
    Extract the file to wherever you would like. 
    
    _If you have any difficulties with installing chromium refer to the documentation provided [here](https://chromedriver.chromium.org/getting-started)_
    
3. Step 3:
    
    Install PyQt5 by running this command: `pip install PyQt5`

4. Step 4:

    After you have installed all the dependencies, you must edit the auto.py file to reference the chromedriver path to the location of your chromedriver file.

5. Step 5:
    
    Edit the secrets.py file to contain your valid utsa login credentials and phone number.

    If you do not want mobile notifications, then edit your secrets.py file like so:
    ```
    username = "abc123"
    password = "password"
    phonenumber = ""
    ```

**Now to execute the program run the command**: `python auto.py`
