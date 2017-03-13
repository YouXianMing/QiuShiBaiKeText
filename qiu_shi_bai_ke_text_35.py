import sqlite3
import time
import requests
from regexp_string import *



class QiuShiBaiKeText35:

    db_name = 'qiu_shi_bai_ke_text35.db'
    conn = None

    def prepare(self):
        """
        开始准备数据库相关准备工作
        :return: PiuShiBaiKeText35对象本身
        """

        # 连接数据库,不存在则创建
        self.conn = sqlite3.connect(self.db_name)

        # 不存在表则创建表
        sql_str = """CREATE TABLE IF NOT EXISTS qiu_shi_bai_ke_text (articleId INT8 PRIMARY KEY NOT NULL,
        content TEXT, date TIMESTAMP); """
        self.conn.execute(sql_str)

        # 关闭数据库
        self.conn.close()
        self.conn = None

        return self

    def start(self, max_page=99999):
        """
        开始爬数据
        :param max_page: 最大页码,不设置则为99999
        :return: PiuShiBaiKeText35对象本身
        """

        self.conn = sqlite3.connect(self.db_name)
        self.__qiu_shi_text(max_page)
        self.conn.close()
        self.conn = None

        return self

    def __qiu_shi_text(self, max_page=99999):
        """
        开始扫描
        :param max_page: 最大页码,不设置则为99999
        :return: None
        """

        for i in range(1, max_page):

            url = "http://www.qiushibaike.com/text/page/%s/" % i
            print(url)
            time.sleep(0.5)

            request = requests.get(url)

            if i != 1:
                request = requests.get(url)
                if request.url != url:
                    break

            self.__convert_from_web_string(request.text)

    def __convert_from_web_string(self, web_string):
        """
        获取网页字符串,并用正则表达式进行解析
        :param web_string: 网页字符串
        :return: None
        """

        # 获取列表
        pattern = r"""\d+" target="_blank" class='contentHerf' >.+?</span>"""
        item_list = RegExpString(web_string).get_item_list_with_pattern(pattern)

        # 如果存在列表,则遍历列表
        if item_list:

            for item in item_list:

                # 内容id
                article_id = RegExpString(item).search_with_pattern(r'^\d+').search_result

                # 内容
                article_content = RegExpString(item).search_with_pattern(
                    r'(?<=<span>).+(?=</span>)').search_result
                article_content = RegExpString(article_content).replace_with_pattern(r'<br/>',
                                                                                     "\n").replace_result

                # 打印内容
                print("http://www.qiushibaike.com/article/%s\n%s\n\n" % (article_id, article_content))

                # 先查找有没有这个id的数据
                cursor = self.conn.execute("""SELECT COUNT(*) FROM qiu_shi_bai_ke_text WHERE articleId = '%s';""" % article_id)

                for row in cursor:

                    # 如果查不到数据,则插入数据
                    if row[0] == 0:
                        # 插入语句
                        sql_str = """INSERT INTO qiu_shi_bai_ke_text (articleId, content, date) VALUES ('%s', '%s', '%s');""" % (
                            article_id, article_content, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                        self.conn.execute(sql_str)

                self.conn.commit()


