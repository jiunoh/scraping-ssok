from DBManager import DBManager
from read_wiz import  read_wiz
from SnoweCrawler import SnoweCrawler

DBManager()
crawler = SnoweCrawler()
url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice'
crawler.crawlAt(url)