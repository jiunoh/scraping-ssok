from DBManager import DBManager
from read_wiz import  read_wiz
from SnoweCrawler import SnoweCrawler

DBManager()
crawler = SnoweCrawler()
crawler.check_out_process()