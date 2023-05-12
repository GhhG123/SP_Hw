# 导入requests库和BeautifulSoup库
import requests
from bs4 import BeautifulSoup
import chardet

# 定义要爬取的网址
url = "https://www.ustc.edu.cn"

# 发送请求并获取响应
response = requests.get(url)
# encoding = chardet.detect(response.content.strip())['encoding']
# html = response.content.strip().decode(encoding)
encoding = chardet.detect(response.content.strip())['encoding']
html = response.content.strip().decode(encoding)

# 判断响应状态码是否为200，表示成功
if response.status_code == 200:
    # 解析响应内容为HTML文档
    soup = BeautifulSoup(html, "html.parser")
    
    # 找到所有的链接标签<a>
    # 遍历链接标签，并打印出链接的文本和地址
    for link in soup.find_all('a', {'title': True, 'href': True}):
        # 检查 href 属性是否存在
        if 'href' in link.attrs:
            print(link.text.strip(), link['href'].strip())
        else:
            continue

    # all = soup.select('a', {'title': True, 'href': True})
    # print(all)
    # tzggcontent.jsp?urltype=news.NewsContentUrl&wbtreeid=1059&wbnewsid=19007
    # https://www.ustc.edu.cn/tzggcontent.jsp?urltype=news.NewsContentUrl&wbtreeid=1059&wbnewsid=19007
else:
    # 如果响应状态码不为200，打印出错误信息
    print("请求失败，错误码：", response.status_code)
