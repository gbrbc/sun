import cStringIO



def curl_get(self, url, refUrl="api.openweathermap.org/data/2.5/weather?box=-73.977162,40.749796,-73.976347,40.749934&APPID=140a1ce7c56c3319a157b6692e013917"):
        buf = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        #curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        #curl.setopt(pycurl.HEADERFUNCTION, self.headerCookie)
        curl.setopt(pycurl.VERBOSE, 0)
        curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0')
        #curl.setopt(pycurl.HTTPGET,1)
        #curl.setopt(pycurl.COOKIE, Cookie)
        #curl.setopt(pycurl.POSTFIELDS, 'j_username={ngnms_user}&j_password={ngnms_password}'.format(**self.ngnms_login))
        curl.setopt(pycurl.COOKIEJAR, '/htdocs/logs/py_cookie.txt')
        curl.setopt(pycurl.COOKIEFILE, '/htdocs/logs/py_cookie.txt')
        if refUrl:
            curl.setopt(pycurl.REFERER, refUrl)
        #curl.setopt(c.CONNECTTIMEOUT, 5)
        #curl.setopt(c.TIMEOUT, 8)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = buf.getvalue()
        curl.close()
        return backinfo 

a = curl_get("api.openweathermap.org/data/2.5/weather?box=-73.977162,40.749796,-73.976347,40.749934&APPID=140a1ce7c56c3319a157b6692e013917","api.openweathermap.org/data/2.5/weather?box=-73.977162,40.749796,-73.976347,40.749934&APPID=140a1ce7c56c3319a157b6692e013917")
