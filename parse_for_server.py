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
last_stop = 387764

start_from = int(input())
end_on = int(input())

print('Beginning')
with webdriver.Chrome(options=options) as browser:
    print('Logged into the browser')
    for i in range(start_from,end_on,-1):
        page = url+str(i)
        browser.get(page)
        time.sleep(1)
        if browser.find_element(By.ID,'bodyDiv').text not in ['Omlouváme se, při načítání rozhodnutí došlo k chybě...','K zobrazení tohoto rozhodnutí nemáte oprávnění.']:
            try:
                decision = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div/p[6]").text
                output = [row.text for row in browser.find_elements(By.TAG_NAME,'dd')]
                output.append(decision)
                output = tuple(output)
                print(i,output)                
                with open('output.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(output)
                with open('links.csv','a',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(page)

            except:
                continue
        else:
            print('Wrong url')
        time.sleep(random.randint(1,2))

