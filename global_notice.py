from selenium import webdriver
import DBManager
from UnivDBManager import UnivDBManager

browser = webdriver.PhantomJS()
browser.get('http://cms.sookmyung.ac.kr/wiz5/contents/board/board_action.php?home_id=exchange&handle=7&page=4&scale=15&categoryId=1&categoryDepth=&parent=')

list_page_num = len(browser.find_elements_by_tag_name('li'))

num = 0
UnivDBManager()

for i in range(0, list_page_num):
    next_list_page = browser.find_element_by_css_selector('#board-container > div.list > div.leftBtn > div > a').get_attribute('href')
    element_list = browser.find_elements_by_css_selector('#board-container > div.list > form > table > tbody > tr > td.title > a')
    url_list = [element_list[i].get_attribute("href") for i in range(3, len(element_list))]
    for url in url_list:
        browser.implicitly_wait(3)
        browser.get(url)
        title = browser.find_element_by_class_name('tit').text
        content = browser.find_element_by_id('contentsDiv').text
        num = num+1
        UnivDBManager.insert(num, 'global', 'global', title, content)
#        print(title)
#        print(content)
    browser.get(next_list_page)

browser.quit()