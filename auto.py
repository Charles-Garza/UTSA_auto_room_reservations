import os
import re
from selenium import webdriver

#Setup selenium requirements
chromedriver = "C:\\Users\\charl\\Downloads\\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("https://utsa.evanced.info/dibs/")

count = 1 #To iterate through items

#Find username and password fields
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

#Use credentials
username.send_keys("abc123")
password.send_keys("password")
# username.send_keys("ewn133")
# password.send_keys("charles david garza")

#Click the login button
driver.find_element_by_xpath("/html/body/div/div/div/div[1]/form/div[3]/button").click()

#Select the room size
driver.find_element_by_xpath("//*[@id='SelectedRoomSize']/option[2]").click()

#Select duration
driver.find_element_by_xpath("//*[@id='SelectedTime']/option[2]").click()

driver.find_element_by_xpath("//*[@id='frmSearch']/div[2]/div/div[3]/input").click()

#Click on JPL
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

#input phone number
phoneNumber = driver.find_element_by_id("Phone")
phoneNumber.send_keys("2104522462")

driver.find_element_by_id("btnCallDibs").click()