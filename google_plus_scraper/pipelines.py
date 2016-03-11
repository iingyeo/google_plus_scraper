# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os
from sqlite3 import IntegrityError

con = None

class GooglePlusScraperPipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createTables()
        
    def setupDBCon(self):
        self.con = sqlite3.connect(os.getcwd() + '/google_plus_scraper.db')
        self.cur = self.con.cursor()
    
    def createTables(self):
        self.createTable()
    
    def closeDB(self):
        self.con.close()
        
    def __del__(self):
        self.closeDB()
        
    def createTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS google_plus_scraper_items(id INTEGER PRIMARY KEY NOT NULL, \
            title TEXT, \
            link TEXT UNIQUE, \
            date TEXT \
            )")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_date ON google_plus_scraper_items(date)")
    
    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self,item):
        try:
            self.cur.execute("INSERT INTO google_plus_scraper_items(\
                title, \
                link, \
                date \
                ) \
            VALUES( ?, ?, ?)", \
            ( \
                item.get('title',''),
                item.get('link',''),
                item.get('date','')
            ))
            print '------------------------'
            print 'Data Stored in Database'
            print '------------------------'
            self.con.commit()
        except IntegrityError:
            print "Integrity Error when insert article to db : " + item.get('link')
            self.con.rollback()
