import requests

class Spider:
    def __init__(self, database):
        self.database = database

    def check_urls(self):
        urls = self.database.get_urls()
        for url in urls:
            url_id = url[0]
            last_modified = url[3]
            response = requests.head(url[1])
            if response.status_code != 200:
                continue
            modified = response.headers.get('last-modified')
            if modified and modified == last_modified:
                continue
            content = self.get_content(url[1])
            if content:
                self.database.update_content(url_id, content, modified)

    def get_content(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        content_type = response.headers.get('content-type')
        if not content_type or not content_type.startswith('text/html'):
            return None
        return response.text
