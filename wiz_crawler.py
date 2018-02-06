from selenium import webdriver
from DepartmentDBManager import DepartmentDBManager
import time

class WizCrawler:
    browser = None
    domain = None
    type = None

    def __init__(self):
        WizCrawler.browser = webdriver.PhantomJS()
        WizCrawler.browser.implicitly_wait(3)
        return

    @classmethod
    def setFields(cls, domain,type):
        WizCrawler.domain = domain
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
                title_tr = titles.__getitem__(count*NUMBER_COLUMN+2)
                title_a = title_tr.find_element_by_css_selector('a')
                title = title_a.text
                print(str(count + 1) + "." + "제목: ", title)
                WizCrawler.print_link_content(title_a,number.text,title)
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
    def print_link_content(cls,a,number,title):
        a.click()
        time.sleep(5)
        content = WizCrawler.browser.find_element_by_id('contentsDiv').text
        content = ' '.join(content.split())
        print('content:\n',content)
        DepartmentDBManager.insert(number, WizCrawler.domain, WizCrawler.type, title, content)
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

