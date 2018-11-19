import requests, bs4, time, sqlite3, TimeTableDatabase
import sys, pyperclip, pprint, re, os, shutil, datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

TimeTable_Url = "https://timetable.dundee.ac.uk/Scientia/SWS/Dundee1819/default.aspx"
TimeTable_Module_Select_Button = "LinkBtn_modules"
TimeTable_Department_ID = "dlFilter"
TimeTable_School_Value = "B8FB2C52859E2190D0FDBC07A892F3D4"
TimeTable_Module_Select_Id = "dlObject"
TimeTable_Module_Paraclinical = "DS20006-SEM1-2-A"
TimeTable_Module_ClinicalIntroduction = "DS22007-SEM1-2-A"
TimeTable_ViewTimeTable = "bGetTimetable"
TimeTable_Combine_Button = '//*[@id="RadioType_2"]'

def StripHTML(HTMLSTRIPLIST, Text):
    print(Text)
    print(HTMLSTRIPLIST)
    print("STRIPPING HTML")
    for HTML in HTMLSTRIPLIST:
        print("HTML TERM " + str(HTML))
        if HTML in Text:
            print("HTML FOUND")
            for term in HTMLSTRIPLIST:
                Text = Text.replace(HTML, "")

    return Text

def CommitToDb(listofvalues, classes):
    HTMLTOSTRIP2 = ['<td>', '</td>', '<tr>', '</tr>', '<tr class="columnTitles">', 'Activity', 'Type', 'Start', 'End', 'Duration', 'Weeks', 'Staff', 'Room']
    i = 0
    x = 0

    while i < len(listofvalues):

        if x == (len(classes[i]) + 1):
            continue

        while x < len(classes[i]):

            DBInput = StripHTML(HTMLTOSTRIP2, str(classes[i][x]))

            if DBInput != "":
                print("inputting DB")
                DBInputList = DBInput.splitlines()
            if i == 0:
                DBInputList.append("Monday")
            elif i == 1:
                DBInputList.append("Tuesday")
            elif i == 2:
                DBInputList.append("Wednesday")
            elif i == 3:
                DBInputList.append("Thursday")
            elif i == 4:
                DBInputList.append("Friday")
            for line in DBInputList:
                if line == "":
                    DBInputList.remove(line)

            print("DB LIST:")
            print(DBInputList)
            print(len(DBInputList))
            TimeTableDatabase.ClearDB()
            TimeTableDatabase.CommitToDatabase(DBInputList, "all")
            # check if a row with the lecture ID exists, and if it does, instead update the row instead of making a copy

            x += 1

        i += 1
        x = 0


browser = webdriver.Chrome()
browser.get(TimeTable_Url)

try:
    elementfound = -1
    ModuleID_Selector = browser.find_element_by_id(TimeTable_Module_Select_Button)
    elementfound = 0
    ModuleID_Selector.click()
    time.sleep(1)
    DepartmentID_Selector = browser.find_element_by_id(TimeTable_Department_ID)
    elementfound = 1
    SchoolID_Selector = browser.find_element_by_xpath(('//option[@value="%s"]') % (TimeTable_School_Value))
    elementfound = 2
    print("1: Found both elements")
except:
    print("1: Didn't find element - " + str(elementfound))

DepartmentID_Selector.click()
time.sleep(1)
SchoolID_Selector.click()

try:
    elementfound = 0
    ParaClinical_Module_Select = browser.find_element_by_xpath(('//option[@value="%s"]') % (TimeTable_Module_Paraclinical))
    elementfound = 1
    Clinical_Module_Select = browser.find_element_by_xpath(('//option[@value="%s"]') % (TimeTable_Module_ClinicalIntroduction))
    elementfound = 2
    ViewTimeTable_Button_Select = browser.find_element_by_id(TimeTable_ViewTimeTable)
    elementfound = 3
    TimeTable_Combine_Button_Select = browser.find_element_by_xpath(TimeTable_Combine_Button)
    print("2: Found all 4 elements")
except:
    print("2: Didn't find element - " + str(elementfound))
    # Add fail safes to scraper, so that if no data is scraped DB isn't wrecked

TimeTable_Combine_Button_Select.click()

ActionChains(browser) \
    .key_down(Keys.CONTROL) \
    .click(ParaClinical_Module_Select) \
    .click(Clinical_Module_Select)\
    .key_up(Keys.CONTROL) \
    .perform()

time.sleep(1)

ViewTimeTable_Button_Select.click()

time.sleep(3)

soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
listofvalues = soup.find_all("table", "spreadsheet")

i = 0
classes = [] # Add fail safes to scraper, so that if no data is scraped DB isn't wrecked

while i < len(listofvalues):#list_of_inner_text):
    pprint.pprint(listofvalues[i])#(list_of_inner_text[i])
    holdover = listofvalues[i] #all the lectures by the day

    soup2 = bs4.BeautifulSoup(str(holdover), 'html.parser')

    classes.append(i) #all the lectures divided up
    classes[i] = (soup2.find_all("tr"))
    print("\n")
    i += 1

CommitToDb(listofvalues, classes)
