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
import json
import pandas as pd
import platform
from playsound import playsound

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


if platform.system() == 'Windows':
    driver = webdriver.Chrome(path+ r"\\chromedriver.exe",options=chrome_options) 
    huh = path+ r'\\huup.mp3'
    alaarm = path+ r'\\alaarm.mp3'
else:
    driver = webdriver.Chrome(path+ r"/chromedriver",options=chrome_options) 
    huh = path+ r'/huup.mp3'
    alaarm = path+ r'/alaarm.mp3'



#//*[@id="app--idDemoSearchField-inner"]

urls = ["https://005-iz.impfterminservice.de/impftermine/service?plz=71636", 
		"https://001-iz.impfterminservice.de/impftermine/service?plz=69124",
		 "https://001-iz.impfterminservice.de/impftermine/service?plz=74889",
		 "https://001-iz.impfterminservice.de/impftermine/service?plz=77656",
		 "https://001-iz.impfterminservice.de/impftermine/service?plz=69469",
		 "https://229-iz.impfterminservice.de/impftermine/service?plz=70629"]


#driver.maximize_window()

#/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span
TerminFound = True
while TerminFound:
    for url in urls:
        plz = url.split('plz=')[1]
        #playsound(huh)

        if TerminFound == False:
            break
        driver.get(url)
        try: 
            time.sleep(2)   
            cookiesButton = driver.find_elements_by_xpath('.//html/body/app-root/div/div/div/div[2]/div[2]/div/div[1]/a')
            if len(cookiesButton) > 0:
                cookiesButton[0].click()
                print(str(datetime.now()) + " @ "+plz+ " - cookiesButton click")
            else:
                print(str(datetime.now()) + " @ "+plz+ " - cookiesButton notfound")


        

            neinButton = WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span')))
            neinButton.click()
            print(str(datetime.now()) + " @ "+plz+ " - neinButton click")
            count = 0
            while count < 4:
                if TerminFound == False:
                    break
                response = WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/div/div')))
                try:  
                    txtTmp = response.text
              
                except StaleElementReferenceException as e:
                    print(e)
                    continue  

                print(str(datetime.now()) + " @ "+plz+ ' - Antwort: ' + txtTmp )
            
                time.sleep(3)
                count = count + 1
                if 'Bitte warten' not in txtTmp:
                    #if txtTmp == 'Es wurden keine freien Termine in Ihrer Region gefunden. Bitte probieren Sie es später erneut.\n\nSobald genügend Impfstoff und die entsprechenden Kapazitäten vorhanden sind, werden die Impfzentren weitere Termine einstellen.':
                    print(str(datetime.now()) + " @ "+plz+" - Kein Termin in " + plz )
                    count = 4

                else:
                        print(str(datetime.now()) + " @ "+plz+ " - termin?" )
                        print(str(txtTmp))
                        TerminFound = False
                        playsound(alaarm)
            
        except (TimeoutException):
            print(str(datetime.now()) + " @ "+plz+ " - timeout nein button not found")

        
    print(str(datetime.now()) + " @ "+plz+ " - termin?" )
while True:
    time.sleep(20000)   
