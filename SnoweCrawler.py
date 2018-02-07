from selenium import webdriver
from snowe_content_crawler import *
from DBManager import DBManager
import time


class SnoweCrawler:
    browser = None
    url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice'

    def __init__(self):
        SnoweCrawler.browser = webdriver.PhantomJS()
        SnoweCrawler.browser.implicitly_wait(3)
        SnoweCrawler.browser.get(SnoweCrawler.url)
        time.sleep(5)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        SnoweCrawler.browser.quit()
        return

    @classmethod
    def check_out_process(cls):
        SnoweCrawler.set_page_crawling()
        SnoweCrawler.crawl_pages()
        return

    @classmethod
    def check_out_finished(cls):
        SnoweCrawler.browser.find_element_by_xpath('//*[@id="fnshVDT"]/a').click()
        SnoweCrawler.browser.implicitly_wait(3)
        time.sleep(3)
        SnoweCrawler.set_page_crawling()
        SnoweCrawler.crawl_pages()
        return

    @classmethod
    def set_page_crawling(cls):
        global page_max
        page_end = SnoweCrawler.browser.find_element_by_css_selector('a.next_end')
        page_max = page_end.get_attribute('href')[len(SnoweCrawler.url) + 1:]
        page_max = int(page_max)
        return

    @classmethod
    def crawl_pages(cls):
        for count in range(1, page_max):
            print('page: ',str(count))
            SnoweCrawler.browser.get(SnoweCrawler.url+'#'+str(count))
            time.sleep(5)
            SnoweCrawler.call_list()
        return

    @classmethod
    def call_list(cls):
        board = SnoweCrawler.browser.find_element_by_xpath('//*[@id="messageListBody"]')
        tr_list = board.find_elements_by_css_selector('tr')
        for tr in tr_list:
            if tr.get_attribute('class')!='notice':
                num = tr.find_element_by_css_selector('td.num')
                category = tr.find_element_by_css_selector('td.title_head')
                a = tr.find_element_by_css_selector('a')
                href = a.get_attribute('href')
                title = tr.find_element_by_css_selector('span')

                record = print_page(href)
                record.id = int(num.text)
                record.category = category.text
                record.division = category.text
                record.title = title.text
                DBManager.insert(record)
        return

