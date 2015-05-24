import requests
import bs4
import json

from db import ted_kv
from werobot.utils  import  to_binary

ted_popular_url = 'http://www.ted.com/talks?page=1&sort=popular'
ted_newest_url = 'http://www.ted.com/talks?page=1'

TED_POPULAR = 'ted_popular'
TED_NEWEST = 'ted_newest'


'''
TED web html
<h4 class="h12 talk-link__speaker">Ken Robinson</h4>
'''
def get_ted_page_name():
    print ted_popular_url
    response = requests.get(ted_popular_url)
    print response
    soup = bs4.BeautifulSoup(response.text)
    ted_name_list = []
    for tag in soup.find_all("h4"):
        if None != tag.string:
            ted_name_list.append(tag.string) 
    ted_name_str = json.dumps(ted_name_list)
    if 0 != len(ted_name_list):
        ted_kv.set(to_binary(TED_POPULAR), ted_name_str)
    return ted_name_str

