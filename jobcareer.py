from selenium import webdriver
import time
from DBManager import DBManager
from Record import Record

DBManager()
record = Record()
main_url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/jobcareer'

browser = webdriver.Chrome()
browser.implicitly_wait(3)
browser.get(main_url)
time.sleep(3)

browser.find_element_by_id('userId').send_keys('')
browser.find_element_by_id('userPassword').send_keys('')
browser.find_element_by_id('loginButton').click()
browser.implicitly_wait(3)
browser.get(main_url)

browser.implicitly_wait(3)
browser.find_element_by_id('fnshVDT').click()
browser.implicitly_wait(3)
time.sleep(2)
browser.find_element_by_css_selector('#pagingBar > a.next_end').click()
# go to last list page

browser.implicitly_wait(3)
time.sleep(2)
last_page_num = int(browser.find_element_by_css_selector('#pagingBar > strong').text)   # set last page to current (194)

notice_list = browser.find_elements_by_css_selector('#messageListBody > tr.notice')
notice_len = len(notice_list)

page_bundle = browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
current_in_bundle = len(page_bundle) - 1

for i in range(0, last_page_num):
    time.sleep(5)
    element_list = browser.find_elements_by_css_selector('#messageListBody > tr')
    browser.implicitly_wait(3)
    time.sleep(2)
    url_list = [element_list[j].find_element_by_css_selector('td.title > a').get_attribute("href") for j in range(len(element_list)-1, notice_len-1, -1)]
    num_list = browser.find_elements_by_css_selector('#messageListBody > tr > td.num')
    nums = [num_list[j].text for j in range(len(num_list)-1, -1, -1)]
    titles = [element_list[j].find_element_by_css_selector('td.title').text for j in range(len(element_list)-1, notice_len-1, -1)]
    k = 0   # index of article numbers and titles

    for url in url_list:
        browser.implicitly_wait(3)
        browser.get(url)
        page_view = browser.find_element_by_css_selector('#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li.pageview').text
        page_view = page_view.replace('조회수 ', '')
        page_view = int(page_view)
        division = browser.find_element_by_css_selector('#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > strong > span.title_head > span').text
        division = division.replace('[', '')
        division = division.replace(']', '')
        date = browser.find_element_by_css_selector('#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li:nth-child(4)').text
        date = date[0:10]
        title = titles[k]
        content = browser.find_element_by_css_selector('#_ckeditorContents').text
        article_num = int(nums[k])
        k = k+1
        record.content = content
        record.title = title
        record.id = article_num
        record.category = '취업'
        record.division = division
        record.view = page_view
        record.date = date
        DBManager.insert(record)

    browser.find_element_by_css_selector('#listUrlButton').click()  # back to list
    if current_in_bundle == 3:
        browser.find_element_by_xpath('//*[@id="pagingBar"]/a[2]').click()  # click pre button
        page_bundle = browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
        current_in_bundle = len(page_bundle) - 1
    else:
        current_in_bundle -= 1
        browser.find_element_by_xpath('//*[@id="pagingBar"]/a['+str(current_in_bundle)+']').click()

browser.quit()
