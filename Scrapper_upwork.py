import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
  "Accept-Encoding": "gzip, deflate",
  "DNT": "1",
  "Connection": "close",
  "Upgrade-Insecure-Requests": "1"
}

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--enable-javascript")
options.add_argument('log-level=3')
options.add_argument("--window-size=1024,768")
for x, y in headers.items():
    options.add_argument(f'--{x}={y}')
    
job = input('enter work to search for: ')
no_of_pages = int(input('enter number of pages: '))
print('wait for jobs to be scrapped........')
edge = uc.Chrome(options=options)
edge.get('https://www.upwork.com/')
h = edge.find_element(By.CLASS_NAME, 'nav-search-autosuggest-input')
time.sleep(5)
h.send_keys(job)
h.send_keys(Keys.RETURN)
time.sleep(5)
ele = edge.find_element(By.XPATH, '//ul[@class = "air3-tab-list"]').find_elements(By.TAG_NAME, 'li')[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
edge.get(ele)
titles = []
links = []
info = []
describtion = []
time.sleep(5)
for i in range(no_of_pages):
  x = edge.find_elements(By.TAG_NAME, 'article')
  for i in x:
    titles.append(i.find_element(By.TAG_NAME, 'a').text)
    links.append(i.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    info.append(i.find_element(By.TAG_NAME, 'ul').text.replace('\n',' '))
    describtion.append(i.find_element(By.TAG_NAME, 'p').text)
  edge.find_element(By.CLASS_NAME,'air3-pagination-item').find_element(By.TAG_NAME,'button').click()

data = pd.DataFrame({'Title':titles,'Describtion':describtion,'Info':info,'Link':links})
data.index = data.index + 1
print(data)
data.to_csv(#path to save csv file in )
edge.quit()
