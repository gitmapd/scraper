# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import dotenv
import os
dotenv.load_dotenv()

class BasicScraperPipeline:
    def process_item(self, item, spider):
        return item

class DB:    
    def __init__(self):
         
         ## Create/Connect to database
         HOSTNAME = 'localhost'
         USERNAME = 'scrape'
         PASSWORD = 'jw8s0F4'
         DATABASE = 'scraper'
         self.connection = psycopg2.connect(
             host = HOSTNAME, 
             user = USERNAME, 
             password = PASSWORD, 
             dbname = DATABASE
             )
#         ## Create cursor, used to execute commands
         self.cur = self.connection.cursor()
#         ## Create quotes table if none exists
         self.cur.execute("""
             CREATE TABLE IF NOT EXISTS scraper(
             job_id text,
             job_title text,
             job_detail_url text,
             job_listed text,
             company_name text,
             company_link text,
             company_location text
         )
         """)
    def process_item(self, item, spider):

         ## Define insert statement
        self.cur.execute(""" insert into scraper (job_id, job_title, job_detail_url, job_listed, company_name, company_link, company_location) values (%s,%s,%s,%s,%s,%s,%s)""",
        (
                item['job_id'],
                item['job_title'],
                item['job_detail_url'],
                item['job_listed'],
                item['company_name'],
                item['company_link'],
                item['company_location']
            ))

#         ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

#         ## Close cursor & connection to database 
         self.cur.close()
         self.connection.close()