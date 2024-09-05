from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re

cookies = [
    {"name": "auth_token", "value": "543ee7e3097f42ea4339a43e78109d6c63614a86"},
    {"name": "ct0", "value": "34c049c0ab718bc1f4dc423a5215706d68d5cc638e3f0eab6b436e27719728134c1f0ff45bc87f6fb2fb2f10211ff09ae0d71c99967d7b684cf12427cee5938019bf298fce9d1098d30b55b28779d29c"},
    # Add other cookies as needed
]

class Sel(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.toutiao.com/c/user/token/MS4wLjABAAAAdG03Zz3A5JFDQ7cvPAhk4mWiXZzMDEcThpoKYuBBkfZhUzg8YneMVr2Lok4e1Dcw/?source=profile"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        driver = self.driver
        delay = 3
        driver.get(self.base_url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the bottom of the page.")
                break  # Exit the loop if no new content is loaded
            last_height = new_height
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        print("done")
        with open(f'./page_source.html', 'w', encoding='utf-8') as file:
            file.write(html_source)


if __name__ == "__main__":
    unittest.main()
