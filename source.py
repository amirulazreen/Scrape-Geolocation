from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd 
import sqlite3

namex = []
addressx = []
wazex = []
timex = []

def load():
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_argument('--window-position=950,0')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = 'https://www.subway.com.my/find-a-subway'
    driver.get(url)

    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[id="fp_searchAddress"]')
    search_bar.click()
    search_bar.send_keys("kuala lumpur")
    search_bar.send_keys(Keys.RETURN)

    for x in driver.find_elements(By.XPATH, "//*[@id='fp_locationlist']/div/div"):
        name = x.find_element(By.TAG_NAME, "h4")
        namex.append(name.text)

        address = x.find_element(By.TAG_NAME, "p")
        addressx.append(address.text)

        waze = x.find_element(By.XPATH, ".//div/a[2]")
        url = waze.get_attribute("href")
        wazex.append(url)

        time = x.find_elements(By.TAG_NAME, "p")
        period = '\n'.join([times.text for times in time[1:]])
        timex.append(period)

    df = pd.DataFrame({
    'name': namex,
    'address' : addressx,
    'time' : timex,
    'waze' : wazex
     })
    
    df = df[df['name'].str.strip() != '']

    conn = sqlite3.connect('subway.db')
    df.to_sql('store', conn, if_exists='replace', index=False)

    
    cursor = conn.cursor()
    cursor.execute("UPDATE store SET time = REPLACE(time, '\n', ' ')")
    conn.commit()
    cursor.close()
    conn.close()

    print("COMPLETED")

    driver.quit()

load()