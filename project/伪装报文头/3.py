#coding=utf-8

import urllib
import urllib2
import cookielib

# postdata=urllib.urlencode({
#     'username':'1',
#     'password':'password'
# })
#
# Request=urllib2.Request('http://pythonscraping.com/pages/cookies/login.html',data=postdata)
# response=urllib2.urlopen(Request)
#
# print response.read()

import requests
params={'username':'1','password':'password'}
r=requests.post('http://pythonscraping.com/pages/cookies/login.html',data=params)

print 'Cookie is set to:'
print r.cookies.get_dict()
print '-'*300
r=requests.get('http://pythonscraping.com/pages/cookies/profile.php',cookies=r.cookies)
print r.text
