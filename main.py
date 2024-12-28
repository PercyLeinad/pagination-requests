
from bs4 import BeautifulSoup
import requests
from selectolax.parser import HTMLParser
import re
from urllib.parse import urljoin

def get_next_page(base):
    while True:
        try:
            #scraping current page -base
            print(f"Scraping page: {base}")
            s = requests.Session()
            res_base = s.get(base)
            soup = BeautifulSoup(res_base.text,'html.parser')
            get_data(soup)
            print(f"*"*100)
            #getting next page
            res = s.get(base)
            html = HTMLParser(res.text)
            next_page = html.css_first('li.next a').attributes['href']
            next_page_url = urljoin(base,next_page)
            base = next_page_url
        except AttributeError as At:
            print(f'End of pages {At}')
            break
        

def get_data(sup):
    for book in sup.find('ol',attrs = {'class':'row'}).find_all('li',attrs={'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        item = {
        'title'  :  book.find('h3').string,
        'price'  :  book.select_one('p.price_color').string.replace(u'Â',''),
        'rating' : book.find('p',re.compile("star-rating")).attrs['class'][1]
        }
        master.append(item)
    

master = []
get_next_page('https://books.toscrape.com/catalogue/page-48.html')

print(master)