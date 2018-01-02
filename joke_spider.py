from bs4 import BeautifulSoup
import requests
import random

class joke_maker():
  def __init__(self):
    self.domain_url = "http://kids.yam.com/joke"
    self.max_page = 7
    self.joke_url = ""
  
  def get_joke_url(self):
    page_str = str(random.randrange(1, self.max_page))
    page_url = self.domain_url + "/topjoke.php?page=" + page_str

    req = requests.get(url=page_url)
    links = BeautifulSoup(req.text, "html.parser")
    links = links.find_all("a", class_="purple")

    random_href = links[random.randrange(0,15 if page_str!="7" else 10)].get("href")[1:]

    self.joke_url = self.domain_url + random_href
    print("%s"%(self.joke_url))

  def get_joke(self):
    req = requests.get(url=self.joke_url)
    text = BeautifulSoup(req.text, "html.parser")
    return text.find_all("div", style="overflow: hidden; width: 420px;")[0].text.replace("\r\n", "").replace("\n", "")