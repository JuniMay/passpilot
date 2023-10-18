import difflib
import zhipuai
from bs4 import BeautifulSoup
import re

zhipuai.api_key="78784cd771920e52d3f2bfafccc05df0.nRu9rbTR5uFgTYjd"
class recognizer:
    def __init__(self,html_before:str,html_after:str)->None:
        self.html_before=html_before
        self.html_after=html_after
        self.html_diff=difflib.HtmlDiff().make_file(html_before.splitlines(), html_after.splitlines(), context=True)
        pass
    def diffHTML(self,html_before:str,html_after:str)->str:
        return self.html_diff
    def reparseHTML(self,html:str)->str:
        #这是因为之前的html中会出现中文乱码
        soup=BeautifulSoup(html,"html.parser")
        decoded_html=soup.prettify()
        self.html_diff=decoded_html
        return decoded_html
    def checkCaptcha(self,html:str)->str:


        #先用re找，找不到了再用大模型
        #TODO 检测是否有+解决；解决的话，需要给模型传入图片？
        #TODO
        pass
    def detectFatalMsg(self,html_diff:str)->None:
        soup=BeautifulSoup(html_diff,"html.parser")
        elements=soup.select(".diff_add")
        ToAi="请以fatalMsg=<>的格式，根据我给你的html代码，填写可能作为登录反馈信息的文本。"
        for ele in elements:
            ToAi=ToAi+str(ele)


        response = zhipuai.model_api.invoke(
        model="chatglm_pro",
        prompt=[
        {"role": "user", "content": "你好,我正在做根据HTML文件识别登录报错信息的工作，请你帮助我。"},
        {"role": "assistant", "content": "好的，请问我可以帮助你哪些？"},
        {"role":"user","content":r"请以fatalMsg=<>的格式，根据我给你的html代码，填写登录反馈信息。[<html lang='en'><head><script src='https://www.douban.com/stat.html?&amp;action=login_click&amp;platform=phone&amp;login_click_time=1697534900672&amp;callback=jsonp_agzm4d6k1azmcro' async=""></script><script src='https://www.douban.com/stat.html?&amp;action=login_start&amp;platform=phone&amp;login_start_time=1697534888118&amp;login_browser=%7B%22browser%22%3A%22chrome%22%2C%22ver%22%3A%22118.0.0.0%22%7D&amp;callback=jsonp_d20z7eo28ejsdnp' async=''></script, show-error, 请正确填写手机号,  btn-active, Added]"},
        {"role":"assistant","content":"fatalMsg='请正确填写手机号'"},
        {"role": "user", "content": ToAi},
        ]
        )
        #TODO 上方还需要完善
        if response['msg']=='操作成功':
            if response['data']['task_status']=="SUCCESS":
                print( response['data']['choices']['content'])
                return None
        return



if __name__=="__main__":
    before_file=open("aQ.html",'r')
    before_html=before_file.read()

    after_file=open("bQ.html",'r')
    after_html=after_file.read()
    #以上是获取到了前后的网页
    r=recognizer(before_html,after_html)
    diff_html=r.reparseHTML(r.html_diff)
    r.detectFatalMsg(diff_html)


