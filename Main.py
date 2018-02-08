from DBManager import DBManager
from read_wiz import  read_wiz
from SnoweCrawler import SnoweCrawler

DBManager()
crawler = SnoweCrawler()
crawler.setInfo('YOUR_ID','YOUR_PW')
urls = ['https://snowe.sookmyung.ac.kr/bbs5/boards/jobcareer','https://snowe.sookmyung.ac.kr/bbs5/boards/notice']
for url in urls:
    crawler.crawlAt(url)