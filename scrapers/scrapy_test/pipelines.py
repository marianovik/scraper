import datetime
import sqlite3


class FairePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("brands.db")
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT OR REPLACE INTO brands_tb (name, desc, img, main_brand_url, HTML) 
                                VALUES (?,?,?,?,?)""", (
            item['name'],
            item['desc'],
            item['img'],
            item['main_brand_url'],
            None
        ))
        self.curr.execute(
            """INSERT OR REPLACE INTO inst_tb (handler, name, img, followers, date) VALUES (?, ?, ?, ?, ?)""", (
                item['inst_handler'],
                None,
                None,
                None,
                None
            ))
        self.conn.commit()


class HTMLPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("brands.db")
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""UPDATE brands_tb SET HTML=? WHERE main_brand_url=?""",
                          (str(item['HTML']), item['main_brand_url']))
        self.conn.commit()


class SalesPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("brands.db")
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        item['etcy_sales'] = int(item['etcy_sales'].split(" ")[0])
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute(
            """INSERT OR REPLACE INTO sales_tb (brand_id, etcy_name, amazon_url, etcy_url, etcy_sales) VALUES \
            ((select id from brands_tb where id = ?), ?, ?, ?, ?)""",
            (
                item['name'],
                item['etcy_name'],
                item['amazon_url'],
                item['etcy_url'],
                item['etcy_sales']
            ))
        self.conn.commit()


class InstagramPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("brands.db")
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        item['date'] = datetime.date.today()
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute(
            """INSERT OR REPLACE INTO inst_tb (brand_id)followers, img, date, name,  handler) VALUES \
            ((select id from brands_tb where id = ?), ?, ?, ?, ?, ?)""",
            (
                item['ints_inst_followers'],
                item['inst_img'],
                item['date'],
                item['inst_name'],
                item['inst_handler']
            ))
        self.conn.commit()
