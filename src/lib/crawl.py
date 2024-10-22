from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import os
import requests
import base64
import time

from database.db import create_connection, execute_query, close_connection
from driverUtil import close_handles

def search_selenium(search_name, search_limit):
    search_url = f"https://www.google.com/search?q={search_name}&hl=ko&tbm=isch"
    
    output_dir = "./output/crawl"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    service = ChromeService(executable_path=ChromeDriverManager().install())
    
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(search_url)
    
    search_count = 0
    
    while search_count < search_limit:
        # wait loading
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        
        images = browser.find_elements(By.TAG_NAME, "img")

        for i in range(len(images)):
            if search_count >= search_limit:
                break
            
            try:
                images[i].click()

                # wait original image loading
                original_image = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'sFlh5c FyHeAf iPVvYb')]")))

                img_src = original_image.get_attribute("src")
                if not img_src or not img_src.startswith("http"):
                    continue
                
                response = requests.get(img_src)
                if response.status_code == 200:
                    file_name = f"{search_count}.jpg"
                    file_path = os.path.join(output_dir, file_name)

                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    # encoding
                    jpg_data = base64.b64encode(response.content).decode('utf-8')

                    execute_query(connection, f'INSERT INTO sample(url, data) VALUES (\'{img_src}\', \'{jpg_data}\')')
                    
                    search_count += 1
                else:
                    print(f"Error: Image Download Failure")

                # close modal
                close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ioQ39e wv9iH MjJqGe cd29Sd')]")))
                close_button.click()

                # close tab
                close_handles(browser)
                time.sleep(1)

            except Exception as e:
                close_handles(browser)

        # scroll to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    browser.quit()

if __name__ == "__main__":
    global connection
    connection = create_connection()

    search_selenium(search_name="증명사진", search_limit=100)

    close_connection(connection)