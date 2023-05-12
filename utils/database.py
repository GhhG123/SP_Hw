import sqlite3
import json

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    #once at the time of starting the program
    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS urls
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL UNIQUE, last_content TEXT,
                     last_modified TEXT, last_checked TEXT, last_update TEXT)''')
        self.conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS settings (
                            name TEXT PRIMARY KEY,
                            value TEXT NOT NULL
                        )''')
        self.conn.commit()
    # id：自增长的整数类型主键，用于唯一标识每一条记录。
    # url：文本类型，用于存储网页的URL地址，是一个必填字段，并且具有唯一性约束，保证不会出现重复的URL地址。
    # last_content：文本类型，用于存储最新的网页内容，如果是第一次爬取，则为NULL。-----类型要改吗？
    # last_modified：文本类型，用于存储最新的网页修改时间，如果未知则为NULL。
    # last_checked：文本类型，用于存储最新检查该网页的时间戳，如果未知则为NULL。
        

    def add_url(self, url):
        c = self.conn.cursor()
        c.execute('INSERT INTO urls (url) VALUES (?)', (url,))
        self.conn.commit()
        return c.lastrowid

    def get_urls(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM urls')
        return c.fetchall()

    # def get_url(self, url_id):
    #     c = self.conn.cursor()
    #     c.execute('SELECT * FROM urls WHERE id=?', (url_id,))
    #     return c.fetchone()
    
    def url_exists(self, url):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM urls WHERE url = ?', (url,))
        result = c.fetchone()
        return result[0] > 0    
    
    def add_content(self, html):
        c = self.conn.cursor()
        c.execute('INSERT INTO urls (last_content) VALUES (?)', (html,))
        self.conn.commit()
        return html
    
    def get_content_db(self, url):
        c = self.conn.cursor()
        c.execute('SELECT last_content FROM urls WHERE url=?', (url,))
        return c.fetchone()
    
    def update_content_and_modified(self, url, content, modified):
        c = self.conn.cursor()
        c.execute('UPDATE urls SET last_content=?, last_modified=?, last_checked=datetime() WHERE url=?',
                  (content, modified, url))
        self.conn.commit()

    def delete_url(self, url_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM urls WHERE id=?', (url_id,))
        self.conn.commit()

    def add_last_modified(self, url, modified):
        c = self.conn.cursor()
        c.execute('UPDATE urls SET last_content=? WHERE url=?', (modified, url))
        self.conn.commit()

    def add_last_content_upgrade(self, url, content_update):
        c = self.conn.cursor()
        c.execute('UPDATE urls SET last_update=? WHERE url=?', (content_update, url))
        self.conn.commit()
    
    def get_last_content_upgrade(self, url):
        c = self.conn.cursor()
        c.execute('SELECT last_update FROM urls WHERE url=?', (url,))
        links_json = c.fetchone()[0]
        links = json.loads(links_json)
        return links

    def set_refresh_time(self, refresh_time):
        c = self.conn.cursor()
        c.execute('INSERT OR REPLACE INTO settings (name, value) VALUES (?, ?)', ('refresh_time', refresh_time))
        self.conn.commit()

    def get_refresh_time(self):
        c = self.conn.cursor()
        c.execute('SELECT value FROM settings WHERE name=?', ('refresh_time',))
        row = c.fetchone()
        if row:
            return int(row[0])
        else:
            return 1

    def close(self):
        self.conn.close()