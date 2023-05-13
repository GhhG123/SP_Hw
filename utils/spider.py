import requests
from bs4 import BeautifulSoup
import difflib
import html
import json
import chardet


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
            encoding = chardet.detect(response.content)['encoding']
            html = response.content.decode(encoding)
            print(html)
        return html

    def get_content_db(self, url):
        content_db = self.database.get_content_db(url)
        #new_content_db = content_db.decode('utf-8')
        return content_db

    def compare_content(self, url):
        previous_content = self.get_content_db(url)
        content = self.get_content_internet(url)
        print(type(content))
        print(type(previous_content))
        d = difflib.Differ()
        diff = d.compare(previous_content.splitlines(), content.splitlines())
        new_lines = [line for line in diff if line.startswith('+')]
        if new_lines:
            modified_time = requests.get(url).headers.get('Last-Modified')
            new_content = (content.encode('utf-8'),)
            self.database.update_content_and_modified(
                url, content, modified_time)
            new_html = ''.join([line[2:] for line in new_lines])
            soup = BeautifulSoup(new_html, 'html.parser')
            # 获取a标签的title和href属性
            for link in soup.find_all('a', {'title': True, 'href': True}):
                # 检查 href 属性是否存在
                if 'href' in link.attrs:
                    print(link.text.strip(), link['href'].strip())
                else:
                    continue
            # for a in soup.find_all('a', {'title': True, 'href': True}):
            #     print("<a href='{0}'>{1}</a>", a.get('title'), a.get('href'))

            links = [(a.text.strip(), a['href'].strip())
                     for a in soup.find_all('a', {'title': True, 'href': True})]
            if links:
                self.save_content_upgrade(url, links)
                return links
            else:
                return None
        else:
            links_json = None
            self.database.add_last_content_upgrade(url, links_json)

    def save_content_upgrade(self, url, links):
        links_json = json.dumps(links)
        self.database.add_last_content_upgrade(url, links_json)
        return

    def check_all(self, database):
        urls = database.get_urls()
        exits_true = False
        for url in urls:
            if self.compare_content(url[1]):
                exits_true = True
        if exits_true:
            return True
        else:
            return False
