from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import random

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
url = 'https://rozhodnuti.justice.cz/rozhodnuti/'
options = webdriver.ChromeOptions()
options.add_argument(user_agent)
options.add_argument('--headless')

last_check = 41590

array = ['Jednací číslo','Soud','Soudce','Identifikátor ECLI','Předmět řízení','Datum vydání','Datum zveřejnění','Klíčová slova']
valid_urls = []
print('Начинаем')
with webdriver.Chrome(options=options) as browser:
    print('Зашел в браузер')
    for i in range(425550,41590,-1):
        page = url+str(i)
        browser.get(page)
        time.sleep(1)
        if browser.find_element(By.ID,'bodyDiv').text not in ['Omlouváme se, při načítání rozhodnutí došlo k chybě...','K zobrazení tohoto rozhodnutí nemáte oprávnění.']:
            valid_urls.append(page)
            try:
                decision = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div/p[6]").text
                output = [row.text for row in browser.find_elements(By.TAG_NAME,'dd')][:-2]
                output.append(decision)
                output = tuple(output)
                array.append(output)
                print(f'{i} success')
            except:
                continue
        else:
            print('Wrong url')
        time.sleep(random.randint(1,2))

with open('output.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(array)

with open('links.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(valid_urls)
