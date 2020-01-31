# Automatic study rooms
This is a program designed around automation that makes reservations for study rooms at the University of Texas at San Antonio on behalf of the user

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
    
    _If you have any difficulties with installing chromium refer to the documentation for chromium [here](https://chromedriver.chromium.org/getting-started)_
    
3. Step 3:
    Install PyQt5.
    
    _Install by running this command_: **pip install PyQt5**

After you have installed all the dependencies, you must edit the auto.py file to refernce the chromedriver path to the location of your chromedriver file.

**After this is done, you can now run the project by executing this command:**

`python auto.py`
