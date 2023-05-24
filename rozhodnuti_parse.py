
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from concurrent.futures import ThreadPoolExecutor

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
url = 'https://rozhodnuti.justice.cz/rozhodnuti/'


options = webdriver.ChromeOptions()
options.add_argument(user_agent)
options.add_argument('--headless')


last_check = 41590

array = ['negotiation','soud','soudce','identifikátor','subject','release_date','publication_date','key_words']
valid_urls = []
print('Beginning')

def parse_page(i):
    page = url+str(i)
    with webdriver.Chrome(options=options) as browser:
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
                return
        else:
            print('Wrong url')

# Creating a thread pool
with ThreadPoolExecutor(max_workers=3) as executor:
    # Start parsing for each value of i
    executor.map(parse_page, range(425550, 41590, -1))

# Saving data to CSV files
with open('output.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(array)

with open('links.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(valid_urls)
