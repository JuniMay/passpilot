from bs4 import BeautifulSoup

class Solcha:
    def __init__(self,html:str):
        self.html=html
        self.type="None"
        self.soup=BeautifulSoup(self.html,"html.parser")
        pass
    def detect_captcha(self):
        pass
    def class_captcha(self):
        pass
    def solve_pic(self):
        pass
    def solve_click(self):
        pass
    def solve_slide(self):
        pass


import pytesseract
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4662.6 Safari/537.36'
}


def login():
    pytesseract.pytesseract.tesseract_cmd = r'D:\TesseractOCR\tesseract.exe'
    url = "http://www.daimg.com/member/index.php"
    s = requests.session()
    s.headers = headers
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    captcha = soup.select('#vdimgck')[0]['src']
    captcha_url = 'http://www.daimg.com' + str(captcha[2:])
    print(captcha_url)
    r = s.get(captcha_url)
    try:
        image = Image.open(BytesIO(r.content))
        # image.show()
        code = pytesseract.image_to_string(image)
        print("识别原图的验证码字符串：", code)
        image = image.convert('L')
        # image.show()
        code = pytesseract.image_to_string(image)
        print("识别灰度图的验证码字符串：", code)
        table = []
        threshold = 127  # 二进制阀值
        for j in range(256):
            if j < threshold:
                table.append(0)  # 填黑色
            else:
                table.append(1)  # 填白色
        # 对像素操作
        image = image.point(table, '1')
        image.show()
        code = pytesseract.image_to_string(image)
        url = "http://www.daimg.com/member/index_do.php"
        params = {
            'fmdo': 'login',
            'dopost': 'login',
            'gourl': '',
            'userid': '123456',
            'pwd': '123456',
            'vdcode': code.strip()
        }
        res = s.post(url, data=params, headers=headers)
        contents = re.findall('<h2>(.*?)</h2>', res.text, re.S)[0]
        print(contents)
        # if str(contents).find("验证码错误！") >= 0:
        #     login()
        # else:
        #     print(contents)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    login()