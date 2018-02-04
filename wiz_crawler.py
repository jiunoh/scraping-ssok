from selenium import webdriver
from DBManager import DBManager
from Record import Record
from datetime import datetime
import time
import re


class WizCrawler:
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
        titles = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
        NUMBER_COLUMN = 5
        list_len = len(titles)//NUMBER_COLUMN
        count =0
        while count < list_len:
            titles = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
            number = titles.__getitem__(count*NUMBER_COLUMN)
            if(number.text!='공지'):
                record = Record()
                title_tr = titles.__getitem__(count*NUMBER_COLUMN+2)
                title_a = title_tr.find_element_by_css_selector('a')
                record.title = title_a.text
                print(str(count + 1) + "." + "제목: ", record.title)
                record.id = number.text
                date = titles.__getitem__(count * NUMBER_COLUMN + 3).text
                p = re.compile('\d{4}-\d{2}-\d{2}')
                if not p.match(date):
                    date = str(datetime.today().year) + '-' + date
                record.date = date
                record.view = titles.__getitem__(count*NUMBER_COLUMN + 4).text
                WizCrawler.print_link_content(title_a, record)
            count+=1
        return

    @classmethod
    def move_to_next_page(cls):
        WizCrawler.print_list()
        total_tr = WizCrawler.browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]')
        page_location = str(len(total_tr) - 2)
        page_table = WizCrawler.browser.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[' + page_location + ']/td/table/tbody/tr/td[2]')
        page_list = page_table.find_elements_by_css_selector('*')
        current_page = page_table.find_element_by_css_selector('b')
        CURRENT_NUMBER = current_page.text
        last_page = page_list.__getitem__(len(page_list) - 1)
        LAST_NUMBER = last_page.text
        print('page:', CURRENT_NUMBER + '/' + LAST_NUMBER)
        if(LAST_NUMBER !='[다음]' and CURRENT_NUMBER==LAST_NUMBER):
            print("END OF PAGE")
        else:
            current_item_count = page_list.index(current_page)
            next_page = page_list.__getitem__(current_item_count+1)
            next_page.click()
            time.sleep(5)
            WizCrawler.move_to_next_page()
        return

    @classmethod
    def print_link_content(cls, a, record):
        a.click()
        time.sleep(5)
        content = WizCrawler.browser.find_element_by_id('contentsDiv').text
        content = ' '.join(content.split())
        print('content:\n',content)
        record.category = WizCrawler.department
        record.division = WizCrawler.type
        record.content = content
        DBManager.insert(record)
        WizCrawler.browser.execute_script("window.history.go(-1)")
        time.sleep(5)
        return

    @staticmethod
    def crawl_site(url):
        WizCrawler.browser.get(url)
        time.sleep(5)
        WizCrawler.move_to_next_page()
        return

    @staticmethod
    def quit():
        WizCrawler.browser.quit()
        return

