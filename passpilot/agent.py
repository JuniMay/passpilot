
from typing import Dict, Any, List, Optional
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from difflib import HtmlDiff
from bs4 import BeautifulSoup
import re
import random
import zhipuai

from passpilot.config import Config

class Agent:
    def __init__(self,config:Config) -> None:
        self.options=None
        self.broswer=config.data['options']['broswer']
        if self.broswer==None:
            self.broswer="Chrome"


        self.set_fingers(config)
        if self.broswer=='Chrome' :
            self.driver = webdriver.Chrome(options=self.options)
        if self.broswer=="Firefox":
            self.driver = webdriver.Firefox(options=self.options)


    def visit(self, url: str) -> None:
        self.driver.get(url)
    def set_fingers(self,config:Config)->None:
        if self.broswer=="Chrome":
            self.options=webdriver.ChromeOptions()
        if self.broswer=="Firefox":
            self.options=webdriver.FirefoxOptions()
        op=config.data['options']
        if 'user-agent' in op and not(op['user-agent']==""):
            ua="--user-agent="+op['user-agent']
            self.options.add_argument(ua)

        else:
            return
        return
    def MultiIP_login(self)->None:
        pass
    def solve_captcha(self)->None:
        pass
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

    def diff_html(self, before: str, after: str) -> str:
        return HtmlDiff().make_file(before.splitlines(), after.splitlines(), context=True)

    def check_captcha(self, html: str) -> None:
        # check if there is captcha or not and return the type of the captcha
        pass

    def detect_fatal_msg(self, diff: str) -> Optional[str]:
        soup = BeautifulSoup(diff, "html.parser")


        ele_error=set(soup.find_all(text=re.compile("error")))
        ele_chg=set(soup.select(".diff_chg"))
        ele_add=set(soup.select(".diff_added"))
        elements=ele_error|ele_chg|ele_add
        elements = soup.select(".diff_add")


        user_msg = ""

        for elem in elements:
            user_msg += str(elem)


        # print(user_msg)


        prompt = [
            {
                "role": "user",
                "content": r"你是一个 HTML 登陆提示信息提取器，会高精度检测 HTML 内容中可能是登陆失败提示信息的元素，并且以 `fatal_msg=<message>` 的格式输出而不包含任何冗余信息。"
            },
            {
                "role": "assistant",
                "content": "好的，我明白。"
            },
            {
                "role": "user",

                "content": r"<class xxxxxxxxxerror xxx='xxxerrorxxx' xxxxxxx='xxxxx>密码错误</class>"


            },
            {
                "role": "assistant",
                "content": r"结果为：fatal_msg=`密码错误`"
            },
            {
                "role": "user",
                "content": f'HTML 如下：{user_msg}'
            }
        ]


        response = zhipuai.model_api.invoke(
            model="chatglm_pro",
            prompt=prompt,
            temperature=0.0,
            top_p=0.75,
        )

        if response['success']:
            return response['data']['choices'][0]['content']
        else:
            print(response)
            return None

    def perform(self, config: Config):

        preactions: Dict[str, Dict[str, Any]] = config.data['preactions']

        # sort preactions
        preactions = sorted(preactions.items(), key=lambda x: x[1]['seq'])

        print(preactions)

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

                html_before = self.html()

                # simplest
                self.enter()

                self.delay(5)
                html_after = self.html()

                diff = self.diff_html(html_before, html_after)
                with open('dif.html','w',encoding='utf-8') as f:
                    f.write(diff)
                fatal_msg = self.detect_fatal_msg(diff)
                count += 1

                with open("diff.html", "w") as f:
                    f.write(diff)

                if fatal_msg:
                    print(f"[!]login count: {count}, fatal_msg: {fatal_msg}")
                    break
                else:
                    print(
                        f"[!]login count: {count}, failed to detect fatal msg.")
