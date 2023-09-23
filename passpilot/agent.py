
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
import random

class Agent:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
    
    def visit(self, url: str) -> None:
        self.driver.get(url)
        
    def html(self) -> str:
        return self.driver.page_source

    def close(self) -> None:
        self.driver.close()

    def quit(self) -> None:
        self.driver.quit()
        
    def quick_type(self, xpath: str, content: str) -> None:
        element = self.driver.find_element(By.XPATH, xpath)
        element.send_keys(content)
    
    def humanoid_type(self, xpath: str, content: str) -> None:
        self.scroll_to(xpath)
        element = self.driver.find_element(By.XPATH, xpath)
        for c in content:
            self.random_delay(0.1, 1)
            element.send_keys(c)

    def click(self, xpath: str) -> None:
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        
    def enter(self) -> None:
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER)
        action.perform()
        
    def scroll_to(self, xpath: str) -> None:
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def delay(self, secs: float) -> None:
        sleep(secs)
        
    def random_delay(self, min_secs: float, max_secs: float) -> None:
        self.delay(secs=random.uniform(min_secs, max_secs))