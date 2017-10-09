#coding=utf-8

import urllib2
import urllib

Base_Url='http://httpstat.us/404'
try:
    request=urllib2.Request(Base_Url)
    response=urllib2.urlopen(request)
# except urllib2.HTTPError as e:
#     print e.code
except urllib2.URLError as e:
    if hasattr(e,'reason'):
        print e.reason
        print e.message

finally:
    print "OK"


