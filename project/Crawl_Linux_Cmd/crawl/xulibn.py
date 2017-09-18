#coding=utf-8

from bs4 import BeautifulSoup


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body>
<a></a>
"""

soup=BeautifulSoup(html,"html.parser")
print soup.prettify()

# print soup.title
# print soup.html
# print soup.p
# print soup.name
# print soup.attrs
# print soup.title.name
# print soup.title.attrs
# print soup.p.name
# print soup.p.attrs
# print soup.p['name']
# print soup.p.get('name')
# soup.p['name']='nimabi'
# print soup.p.get('name')
# del soup.p['name']
# print soup.p.attrs
# print soup.p
# print soup.p.string
#
# print type(soup)
# print soup.name
# print soup.attrs
# print soup.string
#
# print soup.a.string

print len(soup.html.contents)
print soup.html.contents

# print soup.html.children
for i in soup.html.children:
    print "a"+str(i)+"a"



