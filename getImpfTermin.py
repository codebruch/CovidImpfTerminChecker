from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import decimal 
import os, sys
from datetime import datetime
import time
import locale
import requests
import argparse
import socketio
import json
import pandas as pd

calledTimes = 0

#Table Structure

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # 
print(os.getcwd())



chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
path = os.path.dirname(os.path.abspath(__file__))
prefs = {"download.default_directory":path}



chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(r"C:\\Users\\d047102\\Desktop\\StockIntelligenceDataService\\chromedriver.exe",options=chrome_options) #C:\\Users\\d047102\\Desktop\\DemoDataGrabber
#//*[@id="app--idDemoSearchField-inner"]

driver.get("https://001-iz.impfterminservice.de/impftermine/service?plz=69124")
#driver.maximize_window()

#/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span
TerminFound = True
while TerminFound:
    try: 
        time.sleep(2)   
        cookiesButton = driver.find_elements_by_xpath('.//html/body/app-root/div/div/div/div[2]/div[2]/div/div[1]/a')
        if len(cookiesButton) > 0:
            cookiesButton[0].click()
            print(str(datetime.now()) + " - cookiesButton click")
        else:
            print(str(datetime.now()) + " - cookiesButton notfound")


        

        neinButton = WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span')))
        neinButton.click()
        print(str(datetime.now()) + " - neinButton click")
        count = 0
        while count < 3:
            response = WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/div/div')))
           

            try:  
                txtTmp = response.text
              
            except StaleElementReferenceException as e:
                print(e)
                continue  

            print(str(datetime.now()) + ' - Antwort: ' + txtTmp +   str(count))
            
            time.sleep(3)
            count = count + 1
            if txtTmp != 'Bitte warten, wir suchen verfügbare Termine in Ihrer Region.':
                if txtTmp == 'Es wurden keine freien Termine in Ihrer Region gefunden. Bitte probieren Sie es später erneut.\n\nSobald genügend Impfstoff und die entsprechenden Kapazitäten vorhanden sind, werden die Impfzentren weitere Termine einstellen.':
                    print(str(datetime.now()) + " - Kein Termin")
                    count = 4

                else:
                    print(str(datetime.now()) + " - termin?" )
                    print(str(txtTmp))
                    TerminFound = False


    except (TimeoutException):
        print(str(datetime.now()) + " - timeout nein button not found")


print(str(datetime.now()) + " - termin?" )
time.sleep(20000)   