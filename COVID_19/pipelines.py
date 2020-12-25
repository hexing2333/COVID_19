# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import datetime

class Covid19Pipeline:
    def __init__(self):
        filename= 'COVID_19-'+str(datetime.date.today())+'.csv'
        self.file = open(filename, 'w', newline='', encoding='utf-8-sig')
        self.fieldnames = ["country", "increased","total","cure","dead"]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()


    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close_spider(self,spider):
        self.file.close()

