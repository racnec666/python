import urllib.request
import urllib.parse
import socket


response = urllib.request.urlopen('http://www.python.org')  # 请求方式为GET
print(response.read().decode('utf-8')) #获取页面内容
print(type(response))  # <class 'http.client.HTTPResponse'>
print(response.status)  # 响应状态码
print(response.getheaders())  # 响应头信息
print(response.getheader('Content-Type'))  # 指定响应头参数


# data参数。请求方式为POST，将'word':'hello'，需要用bytes函数转化成字节流编码格式，发送给服务器，
data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())


# timeout参数，超时时间，超时会抛出超时异常urllib.error.URLError: <urlopen error timed out>
# timeout参数通常设定为1s，超过1s就跳过这个网页的数据抓取
# 需要用try except捕获异常来实现
response = urllib.request.urlopen('http://httpbin.org/post', timeout=0.1)
print(response.read())

try:
    response = urllib.request.urlopen('http://httpbin.org/post', timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print("TIME OUT")


# Request 利用Request类来构建完整的请求
request = urllib.request.Request('https://python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))

# urlopen()的参数不再是URL而是一个Request类型的对象
# 通过构造数据结构可以将请求独立成一个对象，更加丰富和灵活地配置参数
# urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
# 第一个参数url用于请求URL，必传参数
# 第二个参数data，必须是bytes类型，如果是字典，先用urllib.parse模块里的urlencode()编码
# 第三个参数headers是一个字典，是请求头，可以直接构造或者用add_header()方法添加，用于修改User-Agent来伪装浏览器。
# 第四个参数origin_req_host指请求方的host名称或IP地址
# 第五个参数unverifiable表示这个请求是否是无法验证的，默认False，用户没有足够权限接收这个请求的结果。
# 第六个参数method是一个字符串，用来指示请求使用的方法，GET,POST,PUT等
from urllib import parse,request
url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
# req = request.Request(url=url, data=data, headers=headers, method='POST')
req = request.Request(url=url, data=data, method='POST')
req.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)')
response = request.urlopen(req)
print(response.read().decode('utf-8'))


# BaseHandler类是其他Handler的父类，提供了最基本的方法，deault_open(),protocol_request()等
# 各种Handler子类集成这个BaeHandler类
# HTTPDefaultErrorHandler:处理HTTP响应错误
# HTTPRedirectHandler:用于处理重定向
# HTTPCookieProcessor:处理Cookies
# ProxyHandler: 设置代理，默认为空
# HTTPPasswordMgr:管理密码，维护用户名和密码表
# HTTPBasicAuthHandler:管理认证，解决认证问题
# 另一个重要的类OpenerDirector，利用Handler构建Opener

# 验证界面
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)

# 代理
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy_handler = ProxyHandler({
    'http': 'http://127.0.0.1:9743',
    'https': 'https://127.0.0.1:9743'
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('https://www.baidu.com')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

# Cookies
# 将Cookies保存为Mozilla型浏览器的Cookies格式
import http.cookiejar, urllib.request

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('https://www.baidu.com')
for item in cookie:
    print(item.name+"="+item.value)


filename = 'cookies.txt'
# # 生成一个cookies.txt文件
# # cookie = http.cookiejar.MozillaCookieJar(filename)
# # 保存成LWP格式的Cookies文件
cookie = http.cookiejar.LWPCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('https://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)


# 调用load()方法读取本地的Cookies文件，获取到了Cookies内容，前提是我们首先生成了LWPCookieJar格式的Cookies，并保存成文件，然后读取
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('https://www.baidu.com')
print(response.read().decode('utf-8'))  # 打印出了百度源码


# 处理异常
# URLError类来自urllib库的error模块，继承自OSError类
# 具有reason属性，返回错误的原因
from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.com/index.html')
except error.URLError as e:
    print(e.reason)

# HTTPError
# 处理HTTP请求错误，比如认证失败，3个属性
code:返回HTTP状态码，
reason:返回错误原因
headers:返回请求头
from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.com/index.html')
except error.HTTPError as e:
    print(e.reason, e.headers, e.code, sep='\n')

# 先捕获HTTPError,如果不是再捕获URLError异常，else处理正常逻辑
from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.com/index.html')
except error.HTTPError as e:
    print(e.reason, e.headers, e.code, sep='\n')
except error.URLError as e:
    print(e.reason)
else:
    print('Successfully')

# 有时候，reason属性可能返回一个对象，例如TIME OUT,可以利用isinstance()方法判断


# 解析链接
# urlparse() 实现URL的识别和分段
from urllib.parse import urlparse

result = urlparse('https://www.baidu.com')
print(type(result), result)  # 将URL拆分成了6个部分scheme,netloc,path,params,query,fragment

urllib.parse.urlparse(url, scheme='', allow_fragments=True)
# 三个参数 url scheme默认https，可选http  allow_fragments是否忽略fragment部分

# urlunparse()
# 接受可迭代对象，长度必须是6

# urlsplit()
# 只返回5个结果，params合并到path中，元组类型

# urljoin()
# 生成链接，分析base_url的scheme,netloc和path这3个内容并对新连接缺失的部分进行补充

# urlencode()
# 将字典参数序列化为GET请求参数

# parse_qs()
# 将GET请求反序列化

# parse_qsl()
# 将GET请求转化成元组组成的列表

# quote()
# 将内容转化成URL编码格式，讲中文转化成URL编码

# unquote()
# URL解码


# Robots协议
# robots.txt用来告诉爬虫和搜索引擎哪些可以爬取，哪些不能爬取
# 可爬User-agent:*  Disallow:
# 禁止所有Uer-agent:* Disallow:/

# robotparser
# 用来解析robots.txt
# set_url()用来设置robots.txt文件链接
# read()读取robots.txt进行分析
# parse()解析robots.txt，传入的参数是robot.txt某些行的内容
# can_fetch()传入两个参数。第一个User-agent，第二个是抓取的URL
# mtime()返回上次抓取和分析robots.txt时间
# modified() 将当前时间设置为上次抓取和分析robots.txt时间

from urllib.robotparser import RobotFileParser
# rp = RobotFileParser()
# rp.set_url('http://www.jianshu.com/robots.txt')
rp = RobotFileParser('http://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'https://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'https://www.jianshu.com/search?q=python&page=l&type=collections'))



















