from selenium import webdriver
import time

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

browser.implicitly_wait(3)
time.sleep(2)
last_page_num = int(browser.find_element_by_css_selector('#pagingBar > strong').text)
#마지막 페이지로 이동

notice_list = browser.find_elements_by_css_selector('#messageListBody > tr.notice')
notice_len = len(notice_list)

page_bundle = browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
#page_bundle = browser.find_elements_by_css_selector('#pagingBar > a')
current_in_bundle = len(page_bundle) - 1

page_num = last_page_num
for i in range(0, 2):
    time.sleep(5)
    element_list = browser.find_elements_by_css_selector('#messageListBody > tr')
    browser.implicitly_wait(3)
    time.sleep(2)
    url_list = [element_list[i].find_element_by_css_selector('td.title > a').get_attribute("href") for i in range(len(element_list)-1, notice_len-1, -1)]
    for url in url_list:
        browser.implicitly_wait(3)
        browser.get(url)
        title = browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/strong/span[1]').text
        content = browser.find_element_by_css_selector('#_ckeditorContents').text
        print(title)
#        print(content)
#    page_num = page_num - 1
    if current_in_bundle == 2:
        browser.find_element_by_css_selector('#listUrlButton').click()
        browser.find_element_by_xpath('//*[@id="pagingBar"]/a[2]').click()
        page_bundle = browser.find_elements_by_xpath('//*[@id="pagingBar"]/a')
        current_in_bundle = len(page_bundle) - 1
    else:
        browser.find_element_by_css_selector('#listUrlButton').click()
        current_in_bundle -= 1
        browser.find_element_by_xpath('//*[@id="pagingBar"]/a['+str(current_in_bundle)+']').click()
        #page_bundle[current_in_bundle].click() #stale exception
    print(i)


   #  browser.get(main_url+"#"+str(page_num))
   #  browser.find_element_by_css_selector('#listUrlButton').click()
   # browser.get(main_url)
   #  browser.implicitly_wait(3)
   #  browser.find_element_by_id('fnshVDT').click()
   #  browser.implicitly_wait(3)
   #  time.sleep(2)
   #  browser.find_elements_by_css_selector('#pagingBar > a')

print(title)
