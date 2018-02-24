from selenium import webdriver
from DBManager import DBManager
from Record import Record
from datetime import datetime
import re
from selenium.common.exceptions import NoSuchElementException
import time


class WizCrawler:
    record_list = []
    browser = None
    department = None
    type = None

    def __init__(self):
        WizCrawler.browser = webdriver.Chrome()
        WizCrawler.browser.implicitly_wait(3)
        return

    @classmethod
    def setFields(cls, department, type):
        WizCrawler.department = department
        WizCrawler.type = type
        return


    @classmethod
    def print_list(cls):
        row_col = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
        NUMBER_COLUMN = len(WizCrawler.browser.find_elements_by_css_selector('td.title_bg1'))
        list_len = len(row_col)//NUMBER_COLUMN
        for count in range(0, list_len):
            try:
                row_col = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
                number = row_col.__getitem__(count*NUMBER_COLUMN)
                if number.text != '공지':
                    record = Record()
                    title_tr = row_col.__getitem__(count*NUMBER_COLUMN + 2)
                    title_a = title_tr.find_element_by_css_selector('a')
                    record.title = title_a.text
                    record.id = number.text
                    date = row_col.__getitem__(NUMBER_COLUMN*(count + 1) - 2).text
                    if not re.match('\d{4}-\d{2}-\d{2}',date):
                        now = datetime.now()
                        date = str(now.year)+"-"+date
                    record.date = date
                    record.view = row_col.__getitem__(NUMBER_COLUMN*(count + 1) - 1).text
                    WizCrawler.print_link_content(title_a, record)
            except IndexError:
                print(str(count)+" "+record.title )
        return


    @classmethod
    def move_to_next_page(cls):
        WizCrawler.print_list()
        WizCrawler.storeToDB()
        bott_line0 = WizCrawler.browser.find_element_by_css_selector('td.bott_line0')
        try:
            next_page = bott_line0.find_element_by_xpath('//b//following-sibling::a')
            print(next_page.text)
            next_page.click()
            WizCrawler.browser.implicitly_wait(3)
            time.sleep(2)
            WizCrawler.move_to_next_page()
        except NoSuchElementException:
            print("END OF PAGE")

        return


    @classmethod
    def print_link_content(cls, a, record):
        a.click()
        WizCrawler.browser.implicitly_wait(3)
        time.sleep(2)
        content = WizCrawler.browser.find_element_by_id('contentsDiv').text
        record.category = WizCrawler.department
        record.division = WizCrawler.type
        record.content = ' '.join(content.split())
        WizCrawler.record_list.append(record)
        WizCrawler.browser.execute_script("javascript:jf_list()")
        WizCrawler.browser.implicitly_wait(3)
        time.sleep(2)
        return

    @staticmethod
    def crawl_site(url):
        WizCrawler.browser.get(url)
        WizCrawler.browser.implicitly_wait(3)
        time.sleep(2)
        WizCrawler.move_to_next_page()
        return

    @staticmethod
    def storeToDB():
        for record in WizCrawler.record_list:
            DBManager.insert(record)
        WizCrawler.record_list.clear()
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        WizCrawler.browser.quit()
        return

