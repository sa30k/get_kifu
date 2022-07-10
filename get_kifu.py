import argparse
import os
import tqdm
from time import sleep

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(options=Options())

parser = argparse.ArgumentParser()
parser.add_argument('--num_page', type=int, default=500)
parser.add_argument('--save_directory', default='kifu')
args = parser.parse_args()

os.makedirs(args.save_directory, exist_ok=True)

for i in tqdm.tqdm(range(1, args.num_page+1)):
    target_url = 'https://shogidb2.com/latest/page/{}'.format(i)
    driver.get(target_url)

    elements = driver.find_elements(By.CLASS_NAME, 'list-group-item')

    kif_urls = []
    for element in elements:
        kif_url = element.get_attribute('href')
        kif_urls.append(kif_url)

    for url in kif_urls:
        driver.get(url)
        driver.find_element(By.ID, 'csa-export').click()
        sleep(1)
        e = driver.find_element(By.ID, 'kifu-modal')
        text = e.text
        filename = url.split('/')[-1]
        file = open(f'{args.save_directory}/{filename}.csa', 'w')
        file.write(text)
        file.close()

driver.quit()
