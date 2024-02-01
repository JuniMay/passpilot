import base64
import datetime
from typing import Dict, Any, List, Optional

from time import sleep
from difflib import HtmlDiff
from bs4 import BeautifulSoup
import re,os,random
import openai
from passpilot.driver import driver

from passpilot.config import Config
CHROME="Chrome"
FIREFOX="Firefox"

def encode_image(image_path:str):
    with open(image_path,"rb") as image_file:
        return base64.b64encode((image_file.read())).decode('utf-8')
class Agent:
    _caller_prefix="Agent"
    _compatible_browsers=[CHROME]
    _browser_instance_type=None # The used browser now
    _option=None
    _base_config={
        "browser":{
            "enabled":True
        },
        "proxy":{
            "enabled":False,
            "ip":None,
            "port":None
        },
        "user_agent":{
            "enabled":False,
            'engine':"Mozilla/5.0",
            "os":"(Windows NT 10.0; Win64; x64)",
            "Webkit":"AppleWebKit/537.36",
            "KHTML":"(KHTML, like Gecko)",
            "browser":"Chrome/120.0.6099.227 Safari/537.36"
        },
        "others":{
            "headless":False,

        },
       "Agent":{
           "first_shot_url":'https://www.baidu.com',
           "timeout":10, #10 seconds
           "first_shot_max_time":3,
           "scripts":"",
           "scripts_after_load":""
       }
    }
    _arg_mappings = {
        "no_ssl_errors": ["--ignore-certificate-errors"],
        "disable_notifications": ["--disable-notifications"],
        "maximized": ["--start-maximized"],
        "no_default_browser_check": ["--no-default-browser-check"],
        "headless": ["--headless"],
        "user-agent":["--user-agent=__USER_AGENT__"],
        "proxy":["--proxy-server=__PROXY__"]
    }

    @classmethod
    def launch(cls,**kwargs):
        for arg in kwargs:
            if arg in Agent._compatible_browsers and kwargs[arg]:
                Agent._browser_instance_type=arg
                break
            if not Agent._browser_instance_type:
                raise Exception("We need a specify browser in".join(Agent._compatible_browsers))

        # from driver import driver
        #load driver instance
        webdriver_constructor=None
        cls._option=None
        webagent_instance=None
        webdriver_constructor=driver
        #have a shot to launch the driver
        try_times=0
        while try_times<Agent._base_config['Agent']["first_shot_max_time"]:
            try:
                if Agent._browser_instance_type == CHROME:
                    webagent_instance=webdriver_constructor(Chrome=1,options=cls._option)
                if Agent._browser_instance_type==FIREFOX:
                    webagent_instance = webdriver_constructor(FIRFOX=1,options=cls._option)

                if not cls.first_shot(webagent_instance):
                    webagent_instance.quit()
                    #raise Exception("Failed to launch! ")
                else:
                    #webagent_instance.quit()  delete this line or get error "ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it"
                    webagent_instance.set_config(cls._base_config)
                    print("Successful start!")
                    break
            except Exception as e:
                try_times+=1
                if try_times<Agent._base_config['Agent']['first_shot_max_time']:
                    continue
                else:
                    raise Exception("Agent cannot work,please check")
        #Configure


        #Restore
        cls.flush()
        res=webagent_instance
        return res
    @classmethod
    def first_shot(cls,webagent)->bool:
        '''
        :return: Whether the first shot was successful or not
        '''
        try:
            webagent.visit(Agent._base_config['Agent']['first_shot_url'])
            sleep(0.5)# sleep 0.5 seconds
            return True
        except Exception as e:
            return False
    @classmethod
    def set_proxy(cls,enabled:bool,ip:str=None,port:int=None)->None:
        cls._base_config['proxy']['enabled']=enabled
        if enabled:
            cls._base_config['proxy']['ip']=ip
            cls._base_config['proxy']['port']=port
    @classmethod
    def get_proxy(cls)->dict:
        return cls._base_config['proxy']
    @classmethod
    def set_useragent(cls,user_agent:dict)->None:
        cls._base_config['user_agent']=user_agent
    @classmethod
    def set_useragent(cls,enabled,engine:str=None,os:str =None,Webkit:str =None,browser:str =None)->None:
        '''
        :param enabled:
        :param engine:
        :param os:
        :param Webkit:
        :param browser:
        :return: None
        We use user-agent like this:
            'engine':"Mozilla/5.0",
            "os":"(Windows NT 10.0; Win64; x64)",
            "Webkit":"AppleWebKit/537.36",
            "KHTML":"(KHTML, like Gecko)",
            "browser":"Chrome/120.0.6099.227 Safari/537.36"
        '''
        cls._base_config['user_agent']['enabled']=enabled
        cls._base_config['user_agent']['engine']=engine if engine !=None else cls._base_config['user_agent']['engine']
        cls._base_config['user_agent']['os']=os if os !=None else cls._base_config['user_agent']['os']
        cls._base_config['user_agent']['Webkit']=Webkit if Webkit!=None else cls._base_config['user_agent']['Webkit']
        cls._base_config['user_agent']['browser']=browser if browser !=None else cls._base_config['user_agent']['browser']
    @classmethod
    def get_useragent(cls)->dict:
        return cls._base_config['user_agent']
    @classmethod
    def set_options(cls,options:list):
        pass
    @classmethod
    def flush(cls)->None:
        '''
        :return: None

        This function is used to restore the default settings
        '''
        cls._option = None
        cls._browser_instance_type = None  # The used browser now
        cls._base_config = {
            "browser": {
                "enabled": True
            },
            "proxy": {
                "enabled": False,
                "ip": None,
                "port": None
            },
            "user_agent": {
                "enabled": False,
                'engine': "Mozilla/5.0",
                "os": "(Windows NT 10.0; Win64; x64)",
                "Webkit": "AppleWebKit/537.36",
                "KHTML": "(KHTML, like Gecko)",
                "browser": "Chrome/120.0.6099.227 Safari/537.36"
            },
            "others": {

            },
            "Agent": {
                "first_shot_url": 'https://www.baidu.com',
                "timeout": 10,  # 10 seconds
                "first_shot_max_time": 3
            }
        }




    ##################################################
    # def __init__(self,config:Config) -> None:
    #     pass
    def __init(self)->None:
        pass
    def diff_html(self, before: str, after: str) -> str:
        return HtmlDiff().make_file(before.splitlines(), after.splitlines(), context=True)

    def check_msg(self, html: str) -> str:
        # check if there is captcha or not and return the type of the captcha
        captcha_type={"string","sliding","rotating","find"}
        current_time=datetime.now()
        screenshot_name="screenshot_"+self.driver.title+current_time+".png"
        self.driver.save_screenshot(screenshot_name)
        screenshot_base64=encode_image(screenshot_name)
        os.remove(screenshot_name)

        pass
    def solve_cpatcha(self,html:str)->str:

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "user",
                 "content": r"你是一个 HTML 登陆提示信息提取器，会高精度检测 HTML 内容中可能是登陆失败提示信息的元素，并且以 `fatal_msg=<message>` 的格式输出而不包含任何冗余信息。"},
                {"role": "assistant", "content": "好的，我明白。"},
                {"role": "user", "content": r"<class xxxxxxxxxerror xxx='xxxerrorxxx' xxxxxxx='xxxxx>密码错误</class>"},
                {"role": "assistant", "content": r"结果为：fatal_msg=`密码错误`"},
                {"role": "user", "content": f'HTML 如下：{user_msg}'}
            ],
            temperature=0
        )
        if response['usage']:
            return response.choices[0].message.content
        else:
            print(response)
            return None
    def perform(self, config: Config,driver):

        actions: Dict[str, Dict[str, Any]] = config.data['actions']
        print(actions)
        # sort preactions
        actions = sorted(actions.items(), key=lambda x: x[1]['seq'])

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
                driver.visit(config.data['site']['url'])
                for name, action in actions:
                    print("Processing:",name)
                    xpath = action['xpath']
                    act = action['action']
                    if act == 'click':
                        driver.random_delay(1, 2)
                        driver.click(xpath)
                        continue
                    if act== 'type':
                        driver.random_delay(1,2)
                        if action['form']=="id":
                            driver.humanoid_type(xpath,username)
                            continue
                        if action['form']=="pw":
                            driver.humanoid_type(xpath,password)
                            continue
                    if act=='detect':
                        #Here is for detect some captcha information
                        now_html=driver.html()
                        self.detect_fatal_msg(now_html)
                        continue
                    if act=='check':
                        #Here is for check if there is some warnings or not
                        driver.detect_fatal_msg()
                        continue
                    if act =='press':
                        #Here is for press certain key such as Enter
                        continue
                    print("Unknown action:", action)
                html_before = driver.html()
                # simplest login by enter
                driver.enter()
                #Here is for solving the  captcha
                driver.delay(10)
                html_after = driver.html()
                diff = driver.diff_html(html_before, html_after)
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

