from selenium import webdriver
from passpilot.actions import Actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from agentutils.URLUtils import URLUtils
from agentutils.Forms import Form
import re
from copy import deepcopy
class driver:
    _action_chain=[]
    _action=None
    _caller_prefix = "driver"
    _webdriver=None
    _config={

    }
    def __init__(self,**kwargs):

        options=kwargs.get("options")
        for arg in kwargs:
            if arg=="Chrome":
                Chrome_options=webdriver.ChromeOptions()
                self._webdriver=webdriver.Chrome(options=Chrome_options)
                break
            if arg=="Firefox":
                Firefox_options = webdriver.FirefoxOptions()
                self._webdriver = webdriver.Firefox(options=Firefox_options)
                #TODO Firefox.profile
                break
        self._action = Actions(self._webdriver)
        pass

    # upper actions
    def visit(self,url:str):
        try:
            self._webdriver.get(url)
        except Exception as e:
            raise Exception(f"Failed to visit {url} in function driver.visit(url)")

    def quit(self):
        self._webdriver.quit()

    def html(self) -> str:
         return self._webdriver.page_source

    def close(self) -> None:
         self._webdriver.close()

    #lower actions
    def add_actions(self,action)->None:
        pass
    def perform(self)->None:
        self._actions=[]
        pass
    def quick_type(self, xpath: str, content: str) -> None:
        element = self._webdriver.find_element(By.XPATH, xpath)
        element.send_keys(content)
    def humanoid_type(self, xpath: str, content: str) -> None:
        self.scroll_to(xpath=xpath)
        element = self._webdriver.find_element(By.XPATH, xpath)
        for c in content:
            self.random_delay(0.1, 1)
            element.send_keys(c)

    def click(self, xpath: str) -> None:
        element = self._webdriver.find_element(By.XPATH, xpath)
        element.click()

    def enter(self) -> None:
         action = ActionChains(self._webdriver)
         action.send_keys(Keys.ENTER)
         action.perform()

    def scroll_to(self, *args,**kwargs) -> None:
        '''
        xpath:
        element:
        :return:  None. scroll to the pointed position
        '''
        element=None
        xpath = kwargs.get("xpath")
        if xpath:
            element = self._webdriver.find_element(By.XPATH, xpath)
        else:
            element=kwargs.get("element")
        self._webdriver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_top(self):
        self._webdriver.execute_script("window.scrollTo(0, 0);")

    def delay(self, secs: float) -> None:
        sleep(secs)

    def random_delay(self, min_secs: float, max_secs: float) -> None:
         self.delay(secs=random.uniform(min_secs, max_secs))


    ########################
    # for uppest using
    #############
    def search_url(self,url)->dict:
        login_urls=[]
        signup_urls=[]
        self.crawl_init(starting_url=url,bfs=True)
        while self._crawl_next():
            login_forms,signup_forms=self.get_account_forms(login_only=True,signup_only=False)

            if login_forms: login_urls.append(self.current_url())

            if signup_forms : signup_urls.append(self.current_url())

            res={
                "login_urls":login_urls,
                "signup_urls":signup_urls
            }
            return res

    def get_account_forms(self,login_only=True,signup_only=False,*args,**kwargs):
        login_forms=[]
        signup_forms=[]
        displayed_forms=self.get_displayed_forms()
        displayed_forms.insert(0,None)

        for f in displayed_forms:
            if f:
                self.scroll_to(element=f)
            else:
                self.scroll_to_top()
            ret=self._webdriver
    def get_login_forms(self,*args,**kwargs):
        return self.get_account_forms(login_only=True,*args,**kwargs)
    def get_signup_forms(self,*args,**kwargs):
        return self.get_account_forms(signup_only=True,*args,**kwargs)
    def crawl_init(self,starting_url,bfs=False,dfs=False,depth=1,follow=[],nofollow=[],top=None,break_func= None,allow_fragments=True):
        '''

        :param starting_url:
        :param bfs:
        :param dfs:
        :param depth:
        :param follow:
        :param no_follow:
        :param top:
        :param break_func:
        :param allow_fragments:
        :return:
        '''
        if not bfs and not dfs:
            raise Exception("You should select one mode (bfs or dfs) in driver.crawl_init()")
        self._crawl_config = {
            "bfs": bfs,
            "dfs": dfs,
            "depth": depth,
            "cur_depth": 0,
            "follow": follow,
            "nofollow": nofollow,
            "top": top,
            "base_domain": URLUtils.get_main_domain(starting_url),
            "break_func": break_func,
            "allow_fragments": allow_fragments,
            "focused": follow or nofollow,
            "state": {0: [starting_url]},  # key is depth, value is list of lists
            "visited": set()
        }

        pass
    def current_url(self)->str:
        '''
        :return: the current visited url
        '''
        return self._webdriver.current_url
    def _get_current_crawl_depth(self)->int:
        '''
        return:
        '''
        cur_depth=None
        if self._crawl_config["bfs"]:
            cur_depth=min(self._crawl_config["state"].keys())
        elif self._crawl_config['dfs']:
            cur_depth=max(self._crawl_config["state"].keys())
        return cur_depth

    def _get_next_crawl_url(self)->tuple:
        '''
        :return:
        '''
        cur_depth=self._get_current_crawl_depth()
        next_url=self._crawl_config["state"][cur_depth].pop()
        if not self._crawl_config["state"][cur_depth]:
            self._crawl_config["state"].pop(cur_depth)

        return (next_url,cur_depth)

    def _crawl_next(self):
        if not self._crawl_config["state"]:  # If all depths have been explored, return False so the caller knows the crawl finished
            return False

        next_url, cur_depth = self._get_next_crawl_url()

        while next_url in self._crawl_config["visited"] or (self._crawl_config["focused"] and cur_depth != 0 and (self._crawl_config["follow"] and not any([True if re.search(regex, next_url, re.IGNORECASE) else False for regex in self._crawl_config["follow"]]) or self._crawl_config["nofollow"] and any([True if re.search(regex, next_url, re.IGNORECASE) else False for regex in self._crawl_config["nofollow"]]))):
            if not self._crawl_config["state"]:
                return False
            next_url, cur_depth = self._get_next_crawl_url()  # We initially did this recursively, but pages with A LOT of links caused a max recursion exception

        # In DFS mode ONLY, for unvisited URLs we need to traverse all stored URLs in higher layers so the crawl will be complete
        if self._crawl_config["dfs"]:
            for depth in sorted(self._crawl_config["state"].keys()):  # Traverse keys (seen depths/layers) in asc order
                if depth >= cur_depth:
                    break
                if next_url in self._crawl_config["state"][depth]:
                    return self._crawl_next()

        if not self.get(next_url):  # A redirection to a different domain occured, we don't want that
            return self._crawl_next()
        self._crawl_config["visited"].add(next_url)

        # Check if the final URL has been visited or store the final URL as well
        redirection_url = self.current_url()
        if redirection_url != next_url and redirection_url in self._crawl_config["visited"]:
            return self._crawl_next()
        if redirection_url != next_url:
            self._crawl_config["visited"].add(redirection_url)

        next_depth = cur_depth + 1
        if next_depth > self._crawl_config["depth"]:  # If the next layer exceeds the crawl depth, don't store the next links
            return next_url
        links = self.get_internal_links()
        if not links:  # No links? No dice
            return next_url

        if next_depth not in self._crawl_config["state"]:
            self._crawl_config["state"][next_depth] = []
        # Store the links in the order they were collected and the top X, if `top` was specified
        self._crawl_config["state"][next_depth] += links if not self._crawl_config["top"] else links[:self._crawl_config["top"]]
        return next_url
    def _crawl_exit(self):
        self._crawl_config={}

    def get(self,url,allow_redirections=False):
        if not url.startswith("http"):  # Handle single domains without scheme
            url = "http://%s" % url
        self._last_url = url  # Store the last URL that was explicitly visited. Might be needed if the driver hangs to restore state
        if not self._webdriver.get(url):
            return False  # If it timeouts, return False
        if not allow_redirections:
            redirection_url = self.current_url()
            if URLUtils.get_main_domain(url) != URLUtils.get_main_domain(redirection_url):
                # Logger.spit("%s redirected to: %s" % (url, redirection_url), warning=True,
                #             caller_prefix=self._caller_prefix)
                print(f"{url} redirected to :{redirection_url}")
                return False
        self.setup_page_scripts()
        self.store_reference_element(url)
        self.store_reference_element(self.current_url())  # also landing URL in case it differs from the passed URL; quite common

        return True
    def setup_page_scripts(self):
        self._webdriver.execute_script(self._config["Agent"]["scripts_after_load"])

    def store_reference_element(self,url:str):
        pass

    def get_internal_links(self)->list:
        domain = URLUtils.get_main_domain(self.current_url())
        hrefs = []
        for anchor in self._webdriver.find_elements_by_tag_name("a", timeout=0):
            try:
                href = anchor.get_attribute("href")  # Don't be strict in stale references here, just move on
            except Exception as e:
                continue
            if URLUtils.get_main_domain(href) == domain:
                # We don't want visiting and probably downloading any irrelevant file. Also don't consider fragments
                if re.search(self._forbidden_suffixes, href.split("#")[0], re.IGNORECASE):
                    continue
                hrefs.append(href)
        return hrefs

        pass
    def get_displayed_forms(self):
        pass

    def set_config(self,config):
        self._config=deepcopy(config)