link = "https://animalcrossing.fandom.com/wiki/Special:AllPages"

all_pages_links = [link]

def get_next_link(link):
  page = requests.get(link)

  soup = BeautifulSoup(page.content,'html.parser')

  links = []

  for div in soup("div", {'class':"mw-allpages-nav"}):
    links = div.find_all("a", {'title':"Special:AllPages"})

  for link in links:
    if "Next page" in link.get_text():
      link_to_string = str(link)
      start_of_link = link_to_string.find(r'href="/wiki')
      link_formatted = "https://animalcrossing.fandom.com" + link_to_string[start_of_link + 6:]
      link_formatted = link_formatted[:link_formatted.find("\"")]

      all_pages_links.append(link_formatted)

      get_next_link(link_formatted)


get_next_link(link)


links_new = []

for ap_link in all_pages_links:
  page = requests.get(ap_link)

  soup = BeautifulSoup(page.content,'html.parser')

  for div in soup("div", {'class':"mw-allpages-body"}):
    links = div.find_all("li")

  for link in links:
    link_to_string = str(link)
    is_link = link_to_string.find(r'href="/wiki')
    if is_link != -1:
      link_formatted = "https://animalcrossing.fandom.com" + link_to_string[is_link + 6:]
      link_formatted = link_formatted[:link_formatted.find("\"")]

      if(link_formatted not in links_new) and ("/UI" not in link_formatted):
        links_new.append(link_formatted)

print(len(links_new))
print(links_new)
