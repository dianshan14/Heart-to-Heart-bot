import requests
from bs4 import BeautifulSoup
import random

class riddle_maker():
  def __init__(self):
    self.domain_url = "http://kids.yam.com/riddle/"
    self.max_page = 1705
    self.max_raw = 15
    self.riddle_url = ""
    self.riddle = {}
  
  def get_riddle_url(self):
    page_str = str(random.randrange(1, self.max_page))
    page_url = self.domain_url + "newriddle.php?p=" + page_str

    req = requests.get(url=page_url)
    links = BeautifulSoup(req.text, "html.parser")
    links = links.find_all("a", class_="purple")
    self.riddle_url = self.domain_url + links[random.randrange(0,self.max_raw)].get("href")
    print("%s"%(self.riddle_url))

  def get_riddle(self):
    req = requests.get(url=self.riddle_url)
    text = BeautifulSoup(req.text, "html.parser")
    self.riddle['Riddle'] = text.find_all("td", class_="tableword2")[0].text.replace("ㄉ", "的").replace("ㄇ", "麼").replace("ㄋ", "你").replace("ㄍ", "個")
    self.riddle['prompt'] = text.find_all("td", class_="red")[1].text.replace("ㄉ", "的").replace("ㄇ", "麼").replace("ㄋ", "你").replace("ㄍ", "個")
    self.riddle['answer'] = text.find_all("td", class_="letter_t1")[0].text.replace("\n", "").replace("ㄉ", "的").replace("ㄇ", "麼").replace("ㄋ", "你").replace("ㄍ", "個")
    
    return self.riddle 