import json
from wiz_crawler import WizCrawler


def read_wiz():
    data = json.load(open('wiz_departments.json'))

    crawler = WizCrawler()
    for count in range(0,len(data)):
        department = data[count]['department']
        domain_name = data[count]['domain_name']
        home_id = data[count]['home_id']
        handle = str(data[count]['handle'])
        type = data[count]['type']
        crawler.setFields(department,type)
        wiz = '.sookmyung.ac.kr/wiz/contents/board/board.php?home_id='
        url = 'http://' + domain_name + wiz + home_id + '&handle=' + handle
        crawler.crawl_site(url)
        crawler.storeToDB()

    exit()
    return

