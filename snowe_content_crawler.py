from bs4 import BeautifulSoup
import urllib.request as request
from Record import Record


def print_page(url):
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'lxml')
    article = soup.select_one('div.article')
    p_list = article.find_all('p')
    content = ""
    if p_list:
        for p in p_list:
                content = content + p.text + '\n'
    else:
        board = article.select_one('div#_ckeditorContents')
        content = board.text

    record = Record()
    record.content = ' '.join(content.split())
    record.view = soup.select_one('li.pageview').text[4:]
    record.date = soup.select_one('li.date').text[:10]
    return record

