from selenium import webdriver
from Record import Record
from DBManager import DBManager
import time


class SnoweCrawler:
    browser = None
    url_list = None
    titles = None
    nums = None

    def __init__(self):
        SnoweCrawler.browser = webdriver.Chrome()
        SnoweCrawler.browser.implicitly_wait(3)
        time.sleep(5)
        return

    @classmethod
    def setInfo(cls,ID,PW):
        SnoweCrawler.browser.get('https://snowe.sookmyung.ac.kr/bbs5/users/login')
        time.sleep(3)
        SnoweCrawler.browser.find_element_by_id('userId').send_keys('')
        SnoweCrawler.browser.find_element_by_id('userPassword').send_keys('')
        SnoweCrawler.browser.find_element_by_id('loginButton').click()
        SnoweCrawler.browser.implicitly_wait(3)
        return

    @classmethod
    def crawlAt(cls, url):
        SnoweCrawler.browser.get(url)
        SnoweCrawler.browser.implicitly_wait(3)
        time.sleep(3)
        SnoweCrawler.crawl_pages()
        SnoweCrawler.browser.find_element_by_xpath('//*[@id="fnshVDT"]/a').click()
        SnoweCrawler.browser.implicitly_wait(3)
        time.sleep(3)
        SnoweCrawler.crawl_pages()
        return

    @classmethod
    def crawl_pages(cls):
        SnoweCrawler.browser.find_element_by_css_selector('a.next_end').click()
        SnoweCrawler.browser.implicitly_wait(3)
        time.sleep(2)
        last_page_num = int(
            SnoweCrawler.browser.find_element_by_css_selector('#pagingBar > strong').text)  # set last page to current (194)

        notice_list = SnoweCrawler.browser.find_elements_by_css_selector('#messageListBody > tr.notice')
        notice_len = len(notice_list)
        page_bundle = SnoweCrawler.browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
        current_in_bundle = len(page_bundle) - 1

        for i in range(0, last_page_num):
            time.sleep(5)
            element_list = SnoweCrawler.browser.find_elements_by_css_selector('#messageListBody > tr')
            SnoweCrawler.browser.implicitly_wait(3)
            time.sleep(2)
            SnoweCrawler.url_list = [element_list[j].find_element_by_css_selector('td.title > a').get_attribute("href") for j in
                        range(len(element_list) - 1, notice_len - 1, -1)]
            num_list = SnoweCrawler.browser.find_elements_by_css_selector('#messageListBody > tr > td.num')
            SnoweCrawler.nums = [num_list[j].text for j in range(len(num_list) - 1, -1, -1)]
            SnoweCrawler.titles = [element_list[j].find_element_by_css_selector('td.title').text for j in
                      range(len(element_list) - 1, notice_len - 1, -1)]

            SnoweCrawler.extract_data()

            SnoweCrawler.browser.find_element_by_css_selector('#listUrlButton').click()  # back to list
            if current_in_bundle == 3:
                SnoweCrawler.browser.find_element_by_xpath('//*[@id="pagingBar"]/a[2]').click()  # click pre button
                page_bundle = SnoweCrawler.browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
                current_in_bundle = len(page_bundle) - 1
            else:
                current_in_bundle -= 1
                SnoweCrawler.browser.find_element_by_xpath('//*[@id="pagingBar"]/a[' + str(current_in_bundle) + ']').click()

        return

    @classmethod
    def extract_data(cls):
        k = 0  # index of article numbers and titles
        for url in SnoweCrawler.url_list:
            SnoweCrawler.browser.implicitly_wait(3)
            SnoweCrawler.browser.get(url)
            page_view = SnoweCrawler.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li.pageview').text
            page_view = page_view.replace('조회수 ', '')
            page_view = int(page_view)
            division = SnoweCrawler.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > strong > span.title_head > span').text
            division = division.replace('[', '')
            division = division.replace(']', '')
            date = SnoweCrawler.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li:nth-child(4)').text
            date = date[0:10]
            title = SnoweCrawler.titles[k]
            content = SnoweCrawler.browser.find_element_by_css_selector('#_ckeditorContents').text
            article_num = int(SnoweCrawler.nums[k])
            k = k + 1
            record = Record()
            record.content =  ' '.join(content.split())
            record.title = title
            record.id = article_num
            record.category = '취업'
            record.division = division
            record.view = page_view
            record.date = date
            DBManager.insert(record)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        SnoweCrawler.browser.quit()
        return

