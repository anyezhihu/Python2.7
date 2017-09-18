import urllib2
import re
from bs4 import BeautifulSoup
import chardet


url="http://m.meijutt.com/"
Request=urllib2.Request(url)
response=urllib2.urlopen(Request)
content=response.read()
print chardet.detect(content)
content=content.decode('GB2312')
print content