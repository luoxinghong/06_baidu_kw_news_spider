# -*- coding: utf-8 -*-
from scrapy import cmdline


projcet_name = 'eventspider'
kws = ["中国平安", "中国软件"]

for kw in kws:
    print("1111", kw)
    cmdline.execute("scrapy crawl {0} -a keyword={1}".format(projcet_name, kw).split())



# for kw in cols[1:]:
#     os.system("scrapy crawl {0} -a keyword={1}".format(projcet_name, kw))
