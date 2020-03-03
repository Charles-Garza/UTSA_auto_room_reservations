import sys, os, re, time
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from secrets import username, password, phonenumber
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class App(QWidget):
    
    # initialize the base of the GUI
    def __init__(self):
        super().__init__()
        self.title = 'Auto reservations - UTSA study rooms'
        self.left = 150
        self.top = 50
        self.width = 440
        self.height = 280
        self.initUI()
    
    # initialize the additional components of GUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(420, 180)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.resize(self.width, self.height)

        # Add title label and adjust styling
        title = QLabel("Automatic Room Reservations", self)
        title.setStyleSheet("QLabel {color: white; font: 24pt Comic Sans MS}")
        title.setFixedWidth(340)
        title.move(40, 10)
        title.setAlignment(Qt.AlignCenter)

        # Add sub title label and adjust styling
        subTitleLabel = QLabel("Automated Reservations:", self)
        subTitleLabel.setStyleSheet("QLabel {color: white; font: 18pt Comic Sans MS}")
        subTitleLabel.setFixedWidth(340)
        subTitleLabel.move(40, 50)
        subTitleLabel.setAlignment(Qt.AlignCenter)

        # Add quick search button and adjust styling
        self.quickSearchBtn = QPushButton("Start Automation", self)
        self.quickSearchBtn.setToolTip('Click this button to reserve a room now')
        self.quickSearchBtn.move(145, 80)
        self.quickSearchBtn.resize(140, 25)
        self.quickSearchBtn.setStyleSheet("QPushButton {background-color:rgb(18, 42, 80); color: white;}")

        # Create the thread objects
        self.worker = WorkerObject()
        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()

        # Attach button to click action and start thread
        self.quickSearchBtn.clicked.connect(self.worker.loop)
        self.quickSearchBtn.clicked.connect(self.on_click)

        # Cancel label
        self.cancel_lbl = QLabel("Cancel your reservations:", self)
        self.cancel_lbl.setStyleSheet("QLabel {color: white; font: 18pt Comic Sans MS}")
        self.cancel_lbl.setFixedWidth(340)
        self.cancel_lbl.move(40, 110)
        self.cancel_lbl.setAlignment(Qt.AlignCenter)

        # Kill the thread from this button
        self.cancel_btn = QPushButton("Stop", self)
        self.cancel_btn.setToolTip('Click this button to cancel automatic reservations')
        self.cancel_btn.move(180, 140)
        self.cancel_btn.setStyleSheet("QPushButton {background-color:rgb(18, 42, 80); color: white;}")
        self.cancel_btn.clicked.connect(self.cancel)

        self.show() # Show the window

    # function will change button label once clicked and set threads 
    # activity to true
    def on_click(self):
        self.quickSearchBtn.resize(140, 25)
        self.quickSearchBtn.setText("Clicked and running!")
        self.worker.threadActive = True

    # Function will kill the active thread
    def cancel(self):
        self.worker.stop()
        self.quickSearchBtn.resize(140, 25)
        self.quickSearchBtn.setText("Restart Automation")


class PaintWidget(QWidget):
    # Function to paint a scene
    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setPen(Qt.black)
        size = self.size()

        # Colored rectangles
        qp.setBrush(QColor(241, 90, 37))
        qp.drawRect(0, 0, 640, 580)


class WorkerObject(QtCore.QObject):
    # initialize the thread
    def __init__(self):
        super(WorkerObject, self).__init__()
        self.threadActive = True

    # Function that will be handling all logic 
    def loop(self):
        try:
            ''' Setup selenium requirements '''
            # Example for mac users
            chromedriver = "/usr/local/bin/chromedriver"

            # Example for windows users
            #chromedriver = "C:\\Users\\charl\\Downloads\\chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver    
            
            # options to be a headless browser
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")

            # Continually do this until stopped
            while True and self.threadActive:
                d = datetime.now() # Timestamp datetime
                day = d.isoweekday() # Numerical day of the week

                # Once it turns to tuesday then search
                if d.hour == 0 and (day == 2 or day == 4):
                    driver = webdriver.Chrome(chromedriver, options=options)
                    driver.get("https://utsa.evanced.info/dibs/")
                    auto_reserve(self, driver) # Reserve a room
                else:
                    print('Not time to search yet! Current time:', d)

                    # Sleep for 30 minutes then check if tuesday/thursday
                    time.sleep(18000)

        except Exception as e:
            print("Something went wrong", e)

    # Function that will stop the thread
    def stop(self):
        print("\n<======= Stopping thread ======>\n")
        self.threadActive = False


def auto_reserve(self, driver):
    # Find username and password fields
    un = driver.find_element_by_id("username")
    pw = driver.find_element_by_id("password")
    count = 1 # Will be used to iterate through items

    # Use credentials
    un.send_keys(username)
    pw.send_keys(password)

    # Click the login button
    click_button(driver, "/html/body/div/div/div/div[1]/form/div[3]/button")

    try:
        # First wait 3 seconds then select the room size desired
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SelectedRoomSize']/option[2]"))).click()

        # Select duration
        click_button(driver, "//*[@id='SelectedTime']/option[2]")

        # Choose days to look for a time
        choose_next_week_time(driver)

        # Click search button
        click_button(driver, "//*[@id='frmSearch']/div[2]/div/div[3]/input")

        # Click on JPL
        click_button(driver, "//*[@id='frmBuildings']/div/div/div[3]")
        
        container = driver.find_elements_by_class_name("item-link")

        # Iterate through the list of displayed times
        for item in container:
            name = item.find_element_by_xpath("//*[@id='frmTimes']/div/div/div["+str(count)+"]")
            count += 1
            time_available = name.text

            if re.match("2:00 PM-4:00 PM", time_available):
               item.click()
               count = 1
               break

        # Show that a time is available to select
        if count == 1:
            print("Time slot available!\n" + time_available)
            reserve_room(driver, count, time_available)
        # No time was available to select
        else: 
            print("\nNo time slot available!")
            driver.close() # Close the browser   

    except Exception as e:
        print(e) # Print the exception
        driver.close() # Close the browser


def choose_next_week_time(driver):
    # Choose any time from the times drop down menu
    click_button(driver, "//*[@id='SelectedTimeSort']/option[2]")

    # Choose tuesday from the search date drop down
    click_button(driver, "//*[@id='SelectedSearchDate']/option[8]")


def reserve_room(driver, count, time_available):
    rooms = driver.find_elements_by_class_name("item-link")
    clicked = False
    saved = False

    # Iterate through all available rooms
    for item in rooms:
        roomNumber = item.find_element_by_xpath("//*[@id='frmRooms']/div/div/div["+str(count)+"]")

        count += 1
        text = roomNumber.text
        print(text)

        # Check if a room matches the specified regex
        if re.match(" Room 3[0-9]", text):
            item.click()
            clicked = True
            break

        # Check for any room matching the specified regex        
        if re.match(" Room 2[5-9]", text) and saved != True:
            savedItem = item
            saved = True
        elif re.match(" Room 4[0-2]", text) and saved != True:
            savedItem = item
            saved = True
                  
    # Used if primary preferred room was not available
    if not clicked:
        savedItem.click()

    try:
        # Optional element
        # Input phone number
        phoneNumber = driver.find_element_by_id("Phone")
        phoneNumber.send_keys(phonenumber)

        # Click the button to finalize reservation
        driver.find_element_by_id("btnCallDibs").click()
        print("\nReservation successful!\nYou reserved: " + text)
        
        driver.close() # Close the browser
        time.sleep(86400)  # Sleep 1 day then start search again
    except Exception:
        print("No preferred rooms were found!")
        driver.close() # Close the browser
        time.sleep(300) # Sleep for 5 minutes

# Function that will click each link
def click_button(driver, xpath):
    driver.find_element_by_xpath(xpath).click()

# Start the application from main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
