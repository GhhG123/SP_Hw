import requests
from bs4 import BeautifulSoup
import difflib
import html
import json

class Spider:
    def __init__(self, database):
        self.database = database
        # urls = self.database.get_urls()
        # for url in urls:
        #     url_id = url[0]
        #     #初始化时保存一次、添加网页时保存一次，都不作为更新内容展示
        #     content = self.get_content(url[1])
    
    def check_urls(self):
        return

    def get_content_internet(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        content_type = response.headers.get('content-type')
        if not content_type or not content_type.startswith('text/html'):
            return None
        else:
            html = response.text
        return html
    
    def get_content_db(self, url):
        content_db = self.database.get_content_db(url)
        return content_db
    
    def compare_content(self, url):
        previous_content = self.get_content_db(url)
        content = self.get_content_internet(url)
        d = difflib.Differ()
        diff = d.compare(previous_content.splitlines(), content.splitlines())
        new_lines = [line for line in diff if line.startswith('+')]
        if new_lines:
            modified_time = requests.get(url).headers.get('Last-Modified')
            self.database.update_content_and_modified(url, content, modified_time)
            new_html = ''.join([line[2:] for line in new_lines])
            soup = BeautifulSoup(new_html, 'html.parser')
            # 获取所有带有title和href属性的a标签，并将它们以title+href的方式呈现给用户
            for a in soup.find_all('a', {'title': True, 'href': True}):
                print("<a href='{0}'>{1}</a>", a.get('title'), a.get('href'))
            #把列表转位json的形式存储
            links = [(a.get('title'), a.get('href')) for a in soup.find_all('a', {'title': True, 'href': True})]
            self.save_content(links)
            return links

    def save_content(self, url, links):
        links_json = json.dumps(links)
        self.database.add_last_content_upgrade(url, links_json)
        return

