#coding=utf-8

import requests
url='http://cuiqingcai.com/1052.html'

r=requests.get(url)

print r.text

