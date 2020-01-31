# Automatic study rooms
This is a program designed to automatically reserve study rooms for you at the University of Texas at San Antonio

**Dependencies needed:**

- Python 3

- chromedriver/chromium for selenium
  * Steps to download and install the necessary dependencies are outlined below:
  1. Step 1:

    You can download chromium from [here](https://chromedriver.chromium.org/downloads).

  2. Step 2:

    **MacOs:**
    You can follow the instructions located [here](https://www.swtestacademy.com/install-chrome-driver-on-mac/) to install.

    **Windows:**
    Extract the file to wherever you would like. 

    _If you have any dificulties with installing chromium refer to the documentation for chromium which is listed [here](https://chromedriver.chromium.org/getting-started)_
    

  3. Step 3:

    Install PyQt5.
    _Install by running this command_: **pip install PyQt5**

  After you have installed all the dependencies, you must edit the file to refernce the chromedriver path to the location of your chromedriver file.

  **After this is done, you can now run the project by executing this command:**
  `python auto.py`
