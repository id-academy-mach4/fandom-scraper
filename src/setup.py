_fandom = "animalcrossing"
# _fandom = "hypixel-skyblock"
# _fandom = "celestegame"

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

_SWCP = Path("../data/_saved_web_cache.json")
if(_SWCP.is_file() == False):
  with open(_SWCP, "w") as _cache_file_object_write: json.dump({}, _cache_file_object_write)

with open(_SWCP, "r") as _cache_file_object_read:
  _cache = json.load(_cache_file_object_read)

  def url_get_function(url):
    global _cache
    if(_cache.keys().__contains__(url) == False):
      selected = req.get(_base_url + url).text.replace("/\n/g", '')
      _cache[url] = selected
    return _cache[url]

  _full_list = []

  _list_url_req = req.get(_base_url + _list_url)
  _list_url_req_soup = bs(_list_url_req.text)

  _list_url_req_soup_mwapc = _list_url_req_soup.select("ul.mw-allpages-chunk")[0]
  _list_url_req_soup_mwapc_links = _list_url_req_soup_mwapc.select("a:not(.mw-redirect)")
  for link_element in _list_url_req_soup_mwapc_links:
    link_href = link_element.get("href")
    if((link_href.__contains__(":") == False) & (link_href.__contains__("Gallery") == False)): _full_list.append({"link":link_href,"title":link_element.get_text()})

  for link_item in _full_list:
    print("PARSING:", link_item)
    url_get_function(link_item["link"])

  with open(_SWCP, "w") as _cache_file_object_write: json.dump(_cache, _cache_file_object_write)

  wordsNotToUse = ["of", "the", "a", "when", "it", "if", "are", "so", "why", "how", "do", "to", "should", "i", "?", "!",
                   ".", ","]

  def findKeywords(startingString):
    i = startingString.lower().translate(str.maketrans('', '', string.punctuation))
    for word in wordsNotToUse:
      i = i.replace(word + " ", "")

    return i

  wordsNotToUse = ["of", "the", "a", "when", "it", "if", "are", "so", "why", "how", "do", "to", "should", "i", "game"]

  def findKeywords(startingString):
    i = startingString.lower().translate(str.maketrans('', '', string.punctuation))
    for word in wordsNotToUse:
      i = i.replace(word + " ", "")

    return i
