# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


class HomeresourcePipeline:
    def open_spider(self, spider):
        self.fp = open('housing.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item

    def close_spider(self, spider):
        self.fp.close()


from scrapy.utils.project import get_project_settings
import pymysql


class MysqlPipline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.password,
                                    db=self.name,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()
        print("连接成功")

    def process_item(self, item, spider):
        sql = "insert into `outer` (`price`,`title`,`location`) values ('%s','%s','%s')" % \
              (item['price'], item['title'], item['location'])
        # sql1 = "insert into `inner` (`cp`,`information`,`picture`,`locat`) values ('%s','%s','%s','%s')" % \
        #        (item['cp'], item['information'], item['picture'], item['locat'])
        # 执行sql语句
        self.cursor.execute(sql)
        print('插入成功')
        # self.cursor.execute(sql1)
        # print('插入成功1')
        # 提交
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
