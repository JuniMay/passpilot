import urllib.parse
import tldextract as tld

class URLUtils():
    @classmethod
    def get_domain(cls,url,del_www=False,del_port=True):
        '''
        :param url: the original url like:'https://www.baidu.com:8099?sdasdasij=wqedqwdh&qwdsqw=scas'
        :param del_www: if remain `www.` or not
        :param del_port: if remain port or not
        :return:  `www.baidu.com`\`www.baidu.com：8099`
        '''
        if url is None:
            return None
        domain=urllib.parse.urlparse(url).netloc
        domain=domain.split(":")[0] if del_port else domain
        domain if not del_www else domain.replace("www.", "")
        return domain
    @classmethod
    def get_main_domain(cls,url,suffix=False):
        '''
        :param url: the url you want to extract
        :param suffix: if remain suffix or not
        :return:

        A example:
        Input:URLutils.get_main_domain("https://www.example.com/path/to/some")
        Output:example
        '''
        if url is None:
            return None
        res=tld.extract(url)
        return res.domain if not suffix else res.domain + "." + res.suffix

    @classmethod
    def get_full_domain(cls, url):
        '''
        :param url:
        :return: the full domain

        A example:
        Input: https://www.example.com/path/to
        Output:www.example
        '''
        if url is None:
            return None
        ret = tld.extract(url)
        if ret.subdomain:
            return "%s.%s.%s" % (ret.subdomain, ret.domain, ret.suffix)
        else:
            return "%s.%s" % (ret.domain, ret.suffix)

    @classmethod
    def get_subdomain(cls, url):
        '''
        :param url:
        :return: subdomain

        A example:
        Input:https://www.subdomain.example.net/
        Output: www.subdomain
        '''
        if url is None:
            return None
        ret = tld.extract(url)
        return ret.subdomain

    def get_path(url, full_path=False):
        '''
        :param full_path: if remain the full path or not
        :return:

        Two examples:
        Input: "http://subdomain.example.co.uk/path/to/something?q=abc",False
        Output: /path/to/something

        Input: "http://subdomain.example.co.uk/path/to/something?q=abc",True
        Output: /path/to/something?{'q'='abc'}
        '''
        if url is None:
            return None
        path = urllib.parse.urlparse(url).path
        if not full_path:
            return path
        else:
            return "%s?%s" % (path, urllib.parse.parse_qs(urllib.parse.urlparse(url).query))

    @classmethod
    def get_query(clas, url):
        res=urllib.parse.urlparse(url).query if url else None
        return res if len(res)!=0 else None
    @classmethod
    def get_scheme(cls, url):
        return urllib.parse.urlparse(url).scheme if url else None

    @classmethod
    def join(cls, domain, path):
        return "%s%s" % (domain, path) if domain.endswith("/") or path.startswith("/") else "%s/%s" % (domain, path)

    @classmethod
    def join_scheme(cls, scheme, url):
        return scheme + "://" + url

    @classmethod
    def del_scheme(cls, url):
        if url is None:
            return None
        scheme = URLutils.get_scheme(url)
        return url.replace(scheme + "://", "")

    @classmethod
    def main_url(cls, url):
        '''
        :param url: the url must contain scheme like "http://","https://"
        :return:
        '''
        domain = URLutils.get_domain(url)

        path = URLutils.get_path(url)

        scheme = URLutils.get_scheme(url)

        return URLutils.join_scheme(scheme, URLutils.join(domain, path))


if __name__=="__main__":
    A=URLutils.main_url('https://www.subdomain.example.co.uk/path/to/something')
    print(A)
    pass