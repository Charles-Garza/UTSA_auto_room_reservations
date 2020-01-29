import sys
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt


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

        #Add label and adjust styling
        title = QLabel(self)
        title.setText("Automatic Room Reservations")
        title.setStyleSheet("QLabel {color: white; font: 30pt Comic Sans MS}")
        title.move(55,30)

        # Add label and adjust styling
        title = QLabel(self)
        title.setText("Quickly Schedule A Reservation")
        title.setStyleSheet("QLabel {color: white; font: 18pt Comic Sans MS}")
        title.move(150, 380)

        #Add quick search button and adjust styling
        quickSearch = QPushButton('Quick reserve', self)
        quickSearch.setToolTip('Click this button to reserve a room now')
        quickSearch.move(270, 420)
        quickSearch.setStyleSheet("QPushButton {background-color:rgb(18, 42, 80); color: white;}")

        #Attach button to click action
        quickSearch.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        quickReserve()

class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setPen(Qt.black)
        size = self.size()

        # Colored rectangles
        qp.setBrush(QColor(241, 90, 37))
        qp.drawRect(0, 0, 640, 580)

def quickReserve():
    #Setup selenium requirements
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chromedriver = "C:\\Users\\charl\\Downloads\\chromedriver"

    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(chromedriver, options=options)
    driver.get("https://utsa.evanced.info/dibs/")

    count = 1 #To iterate through items

    # #Find username and password fields
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    # #Use credentials
    username.send_keys("abc123")
    password.send_keys("password")

    # #Click the login button
    driver.find_element_by_xpath("/html/body/div/div/div/div[1]/form/div[3]/button").click()

    try:
        # #Select the room size
        driver.find_element_by_xpath("//*[@id='SelectedRoomSize']/option[2]").click()


        # #Select duration
        driver.find_element_by_xpath("//*[@id='SelectedTime']/option[2]").click()

        driver.find_element_by_xpath("//*[@id='frmSearch']/div[2]/div/div[3]/input").click()

        # #Click on JPL
        driver.find_element_by_xpath("//*[@id='frmBuildings']/div/div/div[3]").click()

        container = driver.find_elements_by_class_name("item-link")

        for item in container:
            name = item.find_element_by_xpath("//*[@id='frmTimes']/div/div/div["+str(count)+"]")
            count += 1
            print(name.text)
            if re.match("2:00 PM-4:00 PM", name.text):
               item.click()
               break

        count = 1

        rooms = driver.find_elements_by_class_name("item-link")
        clicked = 0

        for item in rooms:
            roomNumber = item.find_element_by_xpath("//*[@id='frmRooms']/div/div/div["+str(count)+"]")
            count += 1
            print(roomNumber.text)
            if re.match(" Room 3[0-9]", roomNumber.text):
                item.click()
                clicked = 1
                break

        count  = 1

        if clicked != 1:
            for item in rooms:
                roomNumber = item.find_element_by_xpath("//*[@id='frmRooms']/div/div/div[" + str(count) + "]")
                count += 1
                print(roomNumber.text)
                if re.match(" Room 2[5-9]", roomNumber.text):
                    item.click()
                    break
                elif re.match(" Room 4[0-2]", roomNumber.text):
                    item.click()
                    break

        count = 1

        # #input phone number
        phoneNumber = driver.find_element_by_id("Phone")
        phoneNumber.send_keys("phonenumber")

        driver.find_element_by_id("btnCallDibs").click()

        driver.close()
    except:
        print("error")
        driver.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())