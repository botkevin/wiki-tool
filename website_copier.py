import website_connection as wc
import re
import requests
from bs4 import BeautifulSoup as bs

class website_copier:

    def __init__(self, user, password, source, destination_urls = [], destination_wikis = []):
        self.s = source
        source_path, source_page_name = link_parse(source)
        self.source_website = wc.website_connection(user, password, source_path, source_page_name)
        assert(destination_urls != [] or destination_wikis != [])
        if destination_wikis == []:
            wiki_page = [link_parse(url) for url in destination_urls]
            self.destination_sites = [wc.website_connection(user, password, x[0], x[1]) for x in wiki_page]
        else:
            self.destination_sites = [wc.website_connection(user, password, x, source_page_name) for x in destination_wikis]

    def copy(self):
        text = self.source_website.get_text()
        for site in self.destination_sites:
            site.save_text(text, "Copy from " + self.s)

    #returns wiki name, page name
def link_parse(url):
    info = re.split('/', url)
    return '/'+info[-3], info[-1]

def get_wikis():
    page = requests.get('http://wafwikifarm.hgst.com/farm/index.php/Main_Page')
    soup = bs(page.content, 'html.parser')
    links = [k for k in soup.find_all('a') if 'WIKI' in k.get_text()]
    wiki_dic = {}
    for link in links:
        href = link['href']
        if href.count('/') == 1:
            wiki_dic[link.get_text()] = href
    return wiki_dic
