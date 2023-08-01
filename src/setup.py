_fandom = "animalcrossing"
# _fandom = "hypixel-skyblock"
# _fandom = "celestegame"
# _fandom = "rlcraft"

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pan
import sqlite3
import json
import sys
from pathlib import Path
import string

_base_url = "https://" + _fandom + ".fandom.com"
_list_url = "/wiki/Special:AllPages"

_SWCP = Path("../data/" + _fandom + ".json")
if(_SWCP.is_file() == False):
  with open(_SWCP, "w") as _cache_file_object_write: json.dump({}, _cache_file_object_write)

with open(_SWCP, "r") as _cache_file_object_read:
  _cache = json.load(_cache_file_object_read)
  _full_list = []

  def url_get_function(url):
    global _cache
    if(_cache.keys().__contains__(url) == False):
      selected = req.get(_base_url + url).text.replace("/\n/g", '')
      _cache[url] = selected
    return _cache[url]

  def _run_list_url(_list_url):
    global _full_list

    _list_url_req = req.get(_base_url + _list_url)
    _list_url_req_soup = bs(_list_url_req.text)

    _list_url_req_soup_mwapc = _list_url_req_soup.select("ul.mw-allpages-chunk")[0]
    _list_url_req_soup_mwapc_links = _list_url_req_soup_mwapc.select("a:not(.mw-redirect)")
    for link_element in _list_url_req_soup_mwapc_links:
      link_href = link_element.get("href")
      print(link_href)
      if((link_href.__contains__(":") == False) & (link_href.__contains__("Gallery") == False)): _full_list.append({"link":link_href,"title":link_element.get_text()})

    _all_pages_navs = _list_url_req_soup.select("div.mw-allpages-nav")
    if(_all_pages_navs.__len__() > 0):
      _all_pages_nav = _all_pages_navs[0]
      links = _all_pages_nav.find_all("a", {'title':"Special:AllPages"})
      for link in links:
        if(link.get_text().__contains__("Next page")): _run_list_url(link.get("href"))

  _run_list_url("/wiki/Special:AllPages")

  for link_item in _full_list:
    print("PARSING:", link_item)
    url_get_function(link_item["link"])

  with open(_SWCP, "w") as _cache_file_object_write: json.dump(_cache, _cache_file_object_write, separators=(',\n', ': '))
