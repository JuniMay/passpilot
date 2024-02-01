# import base64
# import openai
# import os
#
# import requests
#
#
#
#
# if __name__=="__main__":
#     openai.api_key = "sk-X7kAqvtBMDwa1t"
#     base64_image=encode_image("captcha_nku.png")
#     response = openai.ChatCompletion.create(
#     model="gpt-4-vision-preview",
#     messages=[
#     {
#     "role": "user",
#     "content": [
#     {
#     "type": "text",
#     "text": "现在，你是一个根据页面快照识别登录验证码类别的分类器。如果验证码涉及滑动，则该验证码就是sliding类型；如果验证码需要输入图片中的文字，则该验证码就是string类型的；如果该验证码涉及到寻找到正确且对应的图片，则该验证码就是finding类型的。"
#     }
#     ]
#     },
#     {
#     "role": "assistant",
#     "content": [
#     {
#     "type": "text",
#     "text": "好的。"
#     }
#     ]
#     },
#     {
#     "role": "user",
#     "content": [
#     {
#     "type": "text",
#     "text": "请你告诉我这张图片上有没有关于登录验证码的信息？如果有，请直接按照我给定的类型种类输出；如果没有，直接回复'None'。"
#     },
#     {
#     "type": "image_url",
#     "image_url": {
#     "url": f"data:image/jpeg;base64,{base64_image}"
#     }
#     }
#     ]
#     }
#     ],
#     temperature=0
#     )
#
#     if response['usage']:
#         print(response.choices[0].message.content)
#     else:
#         print("None")
from urllib.parse import urlparse
import requests
import re
from bs4 import BeautifulSoup as BS
from selenium import webdriver

from passpilot.agent import Agent
from selenium.webdriver.common.by import By
if __name__=="__main__":
    # h=webdriver.Chrome()
    # h.get("https://accounts.douban.com/passport/login")
    # html=h.page_source
    # print(html)
    # result=re.findall(".*<form (.*)</form>.*", html, re.S)
    # if result:
    #     form_data = '<form ' + result[0] + ' </form>'
    #     form_soup = BS(form_data, "lxml")
    #     print(form_data)
    # else:
    #     raise Exception("Can not get form")

    # a.visit("https://www.baidu.com")
    # ele_search=a.find_element(By.PATH,"//*[@id='kw']")
    # a.quick_type()
    agent=Agent()
    a=agent.launch(Chrome=1)
    AA=a.search_url("amazon.com")
    print(AA)
