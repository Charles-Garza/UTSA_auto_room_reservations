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
from PyQt5.QtCore import pyqtSlot, Qt, QTimer

allReservations = []

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Auto reservations - UTSA study rooms'
        self.left = 350
        self.top = 250
        self.width = 640
        self.height = 580
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(640, 580)

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
        title.setStyleSheet("QLabel {color: white; font: 30pt Comic Sans MS}")
        title.setFixedWidth(640)
        title.move(0,30)
        title.setAlignment(Qt.AlignCenter)

        # Add sub title label and adjust styling
        subTitleLabel = QLabel("Automated Reservations:", self)
        subTitleLabel.setStyleSheet("QLabel {color: white; font: 18pt Comic Sans MS}")
        subTitleLabel.setFixedWidth(640)
        subTitleLabel.move(0, 380)
        subTitleLabel.setAlignment(Qt.AlignCenter)

        # Add quick search button and adjust styling
        quickSearchBtn = QPushButton("Start Automation", self)
        quickSearchBtn.setToolTip('Click this button to reserve a room now')
        quickSearchBtn.move(270, 420)
        quickSearchBtn.setStyleSheet("QPushButton {background-color:rgb(18, 42, 80); color: white;}")

        self.worker = WorkerObject()
        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()

        #Attach button to click action and start thread
        quickSearchBtn.clicked.connect(self.worker.loop)
        
        self.show() # show the window      

class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setPen(Qt.black)
        size = self.size()

        # Colored rectangles
        qp.setBrush(QColor(241, 90, 37))
        qp.drawRect(0, 0, 640, 580)

class WorkerObject(QtCore.QObject):
    def __init__(self):
        super(WorkerObject, self).__init__()

    def loop(self):
        try:
            #Setup selenium requirements

            # Example for mac users
            chromedriver = "/usr/local/bin/chromedriver"

            # Example for windows users
            #chromedriver = "C:\\Users\\charl\\Downloads\\chromedriver"

            os.environ["webdriver.chrome.driver"] = chromedriver    
            
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            
            while True:
                d = datetime.now()
                day = d.isoweekday()
                
                if len(allReservations) != 1 and (day == 2 or day == 4):
                    driver = webdriver.Chrome(chromedriver, options=options)
                    driver.get("https://utsa.evanced.info/dibs/")
                    autoReserve(self, driver) 
                else:
                    print("Not time to search yet!")

                if len(allReservations) != 0:
                    firstTime = allReservations[0]
                    hour = int(firstTime[8:9]) + 2
                    firstTime = '1' + str(hour) + firstTime[9:12]

                    today = date.today().strftime("%Y-%m-%d")
                    timestamp = (str(today) + " " + firstTime)
                    reservationTime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
 
                    if d > reservationTime:
                        allReservations.remove(allReservations[0])

                time.sleep(900) # 15 seconds then start search again
        except KeyboardInterrupt:
            print("Program was killed")

def autoReserve(self, driver):
    # Find username and password fields
    un = driver.find_element_by_id("username")
    pw = driver.find_element_by_id("password")
    count = 1 # Will be used to iterate through items

    # Use credentials
    un.send_keys(username)
    pw.send_keys(password)

    # Click the login button
    clickButton(driver, "/html/body/div/div/div/div[1]/form/div[3]/button")

    try:
        # First wait 3 seconds then select the room size desired
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SelectedRoomSize']/option[2]"))).click()

        # Select duration
        clickButton(driver, "//*[@id='SelectedTime']/option[2]")
        clickButton(driver, "//*[@id='frmSearch']/div[2]/div/div[3]/input")

        # Click on JPL
        clickButton(driver, "//*[@id='frmBuildings']/div/div/div[3]")
        
        container = driver.find_elements_by_class_name("item-link")

        for item in container:
            name = item.find_element_by_xpath("//*[@id='frmTimes']/div/div/div["+str(count)+"]")
            count += 1
            time = name.text
            print(time)
            if re.match("2:00 PM-4:00 PM", time):
               item.click()
               count = 1
               break

        if count == 1:
            print("Time slot available!")
            reserveRoom(self, driver, count, time)
        else:
            print("\nNo time slot available!")
            driver.close()    
    except Exception as e:
        print(e)
        #print("\nThere seemed to be an error here")
        driver.close()

def reserveRoom(self, driver, count, time):
    rooms = driver.find_elements_by_class_name("item-link")
    clicked = False
    saved = False

    for item in rooms:
        roomNumber = item.find_element_by_xpath("//*[@id='frmRooms']/div/div/div["+str(count)+"]")

        count += 1
        text = roomNumber.text
        print(text)

        if re.match(" Room 3[0-9]", text):
            item.click()
            clicked = True
            break
                
        if re.match(" Room 2[5-9]", text) and saved != True:
            savedItem = item
            saved = True
        elif re.match(" Room 4[0-2]", text) and saved != True:
            savedItem = item
            saved = True
                        
    if clicked == False:
        savedItem.click() 

    # input phone number
    try:
        # Optional element
        phoneNumber = driver.find_element_by_id("Phone")
        phoneNumber.send_keys(phonenumber)

        driver.find_element_by_id("btnCallDibs").click()
        allReservations.append(time)
        print("\nReservation successful!\nYou reserved: " + text)
    except Exception:
        print("No preferred rooms were found!")
    driver.close()

def clickButton(driver, xpath):
    driver.find_element_by_xpath(xpath).click()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
