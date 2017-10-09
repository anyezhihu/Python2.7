#coding=utf-8

# import urllib
# import urllib2
#
# page=1
# url="http://www.qiushibaike.com/hot/page/"+str(page)
# Request=urllib2.Request(url)
# try:
#     print Request.headers
#     response=urllib2.urlopen(Request)
#     #print response.read()
# except urllib2.URLError as e:
#     print Request.headers
#     if hasattr(e,'code'):
#         print e.code
#     if hasattr(e,'reason'):
#         print e.reason

#上面的代码会报错'httplib.BadStatusLine: ''
#需要加上伪装的报文头

import urllib
import urllib2

page=1
url="http://www.qiushibaike.com/hot/page/"+str(page)

User_Agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Mobile Safari/537.36"
headers={"User-Agent":User_Agent}

try:
    Request=urllib2.Request(url,headers=headers)
    print Request.headers
    response=urllib2.urlopen(Request)
    print response.read()
except urllib2.URLError as e:
    if hasattr(e,'code'):
        print e.code
    if hasattr(e,'reason'):
        print e.reason
