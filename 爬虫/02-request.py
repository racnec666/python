import requests
import re


# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


# 基本用法
r = requests.get('https://www.baidu.com')
print(type(r))
print(r.status_code)
print(r.text)
print(type(r.text))
print(r.cookies)

# GET请求
r = requests.get('http://httpbin.org/get')
print(r.text)

# 利用params传递字典数据
data = {
    'name': 'Germey',
    'age': 22
}
r = requests.get("http://httpbin.org/get", params=data)
print(r.text)  # "url": "http://httpbin.org/get?name=Germey&age=22"

# 利用json()方法，将返回结果是JSON格式的字符串转化成字典
r = requests.get("http://httpbin.org/get")
print(type(r))
print(r.json())
print(type(r.json()))

# 抓取网页,不添加hearders信息的话无法浏览一些网页
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
titles = re.findall(pattern, r.text)
print(titles)

# 抓取二进制数据 图片，音频，视频等
r = requests.get("https://github.com/favicon.ico")
with open('favincon.ico', 'wb') as f:
    f.write(r.content)

# POST请求
data = {
    'name': 'Germey', 'age':'22'
}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)

# 响应
r = requests.get("http://www.jianshu.com", headers=headers)
print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)


# 文件上传
files = {'file': open('favincon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=files)
print(r.text)


# Cookies
r = requests.get('https://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
    print(key+'='+value)

# 利用cookies登录自己的知乎
headers = {
    'Cookies': 'd_c0="ABDC2LzcLQuPToTMJnzMqQAQa-RG6HtwaPg=|1484836324"; _zap=e1b63caa-60a3-4e2a-b97e-6481d2c50c8f; q_c1=6cf00ae426174eb795cf4b74cbd9ace9|1508645796000|1484836324000; __DAYU_PP=aaIVfi7Vnz7UY2ZBNfVM292ec90eb810; z_c0="2|1:0|10:1532161680|4:z_c0|92:Mi4xRGtHREF3QUFBQUFBRU1MWXZOd3RDeVlBQUFCZ0FsVk5rRHhBWEFBOGVNZmtQYW1CTFFnQmJXNDN3d3BDMFlzT2dn|35b7dde54a3c98e1a0215193ca7ebf99a763aca46dd73c2ab30040684f598b67"; __utmv=51854390.100--|2=registration_date=20160929=1^3=entry_date=20160929=1; _xsrf=ApPJmlr0k1W13ZQ03iyMa5mgj8J50slB; __utma=51854390.250049722.1484836326.1532945550.1533818126.11; __utmz=51854390.1533818126.11.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/51148142; tgw_l7_route=69f52e0ac392bb43ffb22fc18a173ee6; q_c1=6cf00ae426174eb795cf4b74cbd9ace9|1535764273000|1484836324000',
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

}
r = requests.get('http://www.zhihu.com',headers=headers)
print(r.text)


# 会话维持 Session对象
s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)


# SSL证书验证
response = requests.get('https://www.12306.cn')
print(response.status_code)  # 证书验证错误
# 解决方案verify参数设置为False
response = requests.get('https://www.12306.cn',verify=False)
print(response.status_code)
# 会提示一个警告，建议我们给它指定证书，可以忽略或者捕获
from requests.packages import urllib3
urllib3.disable_warnings()
response = requests.get('https://www.12306.cn',verify=False)
print(response.status_code)

import logging
logging.captureWarnings(True)
response = requests.get('https://www.12306.cn',verify=False)
print(response.status_code)

# 也可以指定本地证书作为客户端证书，添加个cert参数
cert=('path/server.crt','/path/key')


# 代理设置 proxies参数
proxies = {
    'http': 'http://10.10.1.10:3333',
    'https': 'http://10.10.1.10:3222'
}
requests.get('https://www.taobao.com', proxies=proxies)

# HTTP Basic Auth
proxies={"http":"http://user:password@10.10.1.10:3333/"}

# SOCKS代理
proxies={'http':'socks5://user:password@10.10.1.10:3333'}


# 超时设置 timeout参数 timeout参数是连接和读取二者timeout的总和
r = requests.get("https://www.taobao.com", timeout=1)
print(r.status_code)


# 身份认证 验证成功状态码200，失败401
# 方法一：
from requests.auth import HTTPBasicAuth
r = requests.get('http://localhost:5000',auth=HTTPBasicAuth('username', 'password'))
print(r.status_code)

# 方法二：将上面的写法简写
r = requests.get("http://localhost:5000", auth=('username', 'password'))

# 方法三：OAuth认证


# Prepare Request 将请求表示为数据结构
from requests import Request, Session

url = 'http://httpbin.org/post'
data = {'name': 'germey'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
s = Session()
req = Request('POST', url, data=data,headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)

