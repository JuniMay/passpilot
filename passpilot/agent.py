
from typing import Dict, Any, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from .recognizer import recognizer
from time import sleep
import random

from passpilot.config import Config

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
        
    def perform(self, config: Config):
        
        preactions: Dict[str, Dict[str, Any]] = config.data['preactions']
        
        # sort preactions
        preactions = sorted(preactions.items(), key=lambda x: x[1]['seq'])
        
        print(preactions)
        html_before=self.html()
        username_xpath = config.data['fields']['username']['xpath']
        username_file = config.data['fields']['username']['file']
        password_xpath = config.data['fields']['password']['xpath']
        password_file = config.data['fields']['password']['file']
        
        usernames = []
        passwords = []
        
        with open(username_file, 'r') as f:
            usernames = f.read().splitlines()
            
        with open(password_file, 'r') as f:
            passwords = f.read().splitlines()
            
        count = 0
            
        for username in usernames:
            for password in passwords:
                
                self.visit(config.data['site']['url'])
                
                for name, preaction in preactions:
                    xpath = preaction['xpath']
                    action = preaction['action']
                    
                    if action == 'click':
                        self.random_delay(1, 2)
                        self.click(xpath)
                        
                    else:
                        print("Unknown action:", action)
                
        
                self.random_delay(1, 2)
                self.humanoid_type(username_xpath, username)
                self.random_delay(1, 2)
                self.humanoid_type(password_xpath, password)
                
                # simplest
                self.enter()
                
                self.delay(5)
                html_after=self.html()
                r=recognizer(html_after,html_before)
                r.html_diff()
                fatalMsg=r.detectFatalMsg(r.html_diff)
                count += 1
                
                print("[!]login count: ", count,"\tFatalMsg:",fatalMsg)
            