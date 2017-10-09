#coding=utf-8

import cookielib
import urllib2

filename='cookie.txt'
cookie=cookielib.MozillaCookieJar(filename)
handler=urllib2.HTTPCookieProcessor(cookie)

opener=urllib2.build_opener(handler)
response=opener.open('https://www.baidu.com')

for item in cookie:
    print 'Name:=' + item.name
    print 'Value=' + item.value


cookie.save(ignore_discard=True, ignore_expires=True)