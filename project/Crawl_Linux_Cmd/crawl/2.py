#定义通用下载模块
def Get_Url_Results(url,pattern,current_excute_time=10):
    try:
        Request=urllib2.Request(url)
        response=urllib2.urlopen(Request)
        context=response.read()
        results=re.findall(pattern,context)
        current_excute_time=current_excute_time - 1
    except urllib2.HTTPError as e:
        print "下载错误：%s" % e.reason
        results=None
        if current_excute_time > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                print "出现错误，错误代码：%s" % e.code
                print "开始重试，重试次数：%s" % current_excute_time
                return Get_Url_Results(url,pattern,current_excute_time-1)

    return results

#定义获取主目录的函数
def Get_First_Layer():
    Base_Url="http://man.linuxde.net/"
    #Base_Url = "http://httpstat.us/500"
    Base_Path=raw_input(r"请输入存储目录：")
    #print Base_Path
    try:
        if not os.path.exists(Base_Path):
            os.makedirs(Base_Path)
            print "已成功创建路径：%s" % Base_Path
        else:
            print "已发现路径：%s" % Base_Path
    except WindowsError as e:
        print "路径不存在，创建路径%s失败。" % Base_Path
        print e

    try:
        pattern=re.compile(r'<li id="menu-item-[0-9]" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[0-9]"><a href="(.*?)</a></li>')
        aaa=Get_Url_Results(Base_Url,pattern)
    except urllib2.HTTPError as e:
        print "获取网页信息失败"
        print e.reason
    print aaa
