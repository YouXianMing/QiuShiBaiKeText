from qiu_shi_bai_ke_text_35 import *
from file_manager import *
from regexp_string import *

# 开始抓
qiu_shi = QiuShiBaiKeText35().prepare().start()

# 获取数据
total_str = ""
for url, content in qiu_shi.items_list:

    string = """<li><a href="%s">%s</a></li><br/>\n""" % (url, content)
    total_str += string

# 打开本地pattern.html模板
all_the_data = open(Dir().file_name("pattern.html").path, 'rb').read().decode('utf-8')

# 进行文本替换
html_text = RegExpString(all_the_data).replace_with_pattern(r'######', total_str).replace_result

# 开始写文件
file = open(Dir().file_name('qiu_shi.html').path, 'w')
file.write(html_text)
file.close()



