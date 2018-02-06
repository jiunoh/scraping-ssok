import json
from wiz_crawler import WizCrawler

def read_wiz():
    data = json.load(open('wiz_departments.json'))

    print('url개수 : ',len(data))
    crawler = WizCrawler()
    for count in range(0,len(data)):
        domain_name = data[count]['domain_name']
        home_id = data[count]['home_id']
        handle = str(data[count]['handle'])
        type = data[count]['type']
        crawler.setFields(domain_name,type)
        url = 'http://' + domain_name + '.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=' + home_id + '&handle=' + handle
        crawler.crawl_site(url)
    crawler.quit()
    exit()
    return

