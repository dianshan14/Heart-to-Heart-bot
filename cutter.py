import jieba
import jieba.analyse
import random

class jieba_er():
  def __init__(self):
    jieba.initialize()
    jieba.analyse.set_stop_words("./stop.txt")
    jieba.load_userdict("./userdic.txt")
    self.weighted = {}

    self.mood_text_list = {"開心":[], "生氣":[], "難過":[], "沮喪":[], "疲累":[], "無聊":[], "有壓力":[]}

    for key, items in self.mood_text_list.items():
      f = open("./words/"+key+".file", "r")
      words = f.readline().split(",")[0:-1]
      print(words)
      self.mood_text_list[key] = words
      f.close()

    must_text_list = []

    for key, words in self.mood_text_list.items():
      for word in words:
        must_text_list.append(word)

    for x in must_text_list:
      jieba.suggest_freq(x, True)

  def token_er(self, text):

    segments = jieba.lcut(text)

    for x in segments:
      print(x)

    return segments

  def check_semantic(self, segments, mood):

    self.weighted = {x:0 for x, words in self.mood_text_list.items()}

    for token in segments:
      for key, words in self.mood_text_list.items():
        if token in words:
          self.weighted[key] = self.weighted[key] + 1
     
    candidate = []
    weighted_result = [value for key, value in self.weighted.items()]
    max_weighted = max(weighted_result)

    # no match text
    if max_weighted == 0:
      return mood

    for key, value in self.weighted.items():
      if value == max_weighted:
        candidate.append(key)

    if len(candidate) == 1: # only one mood
      return candidate[0]
    else:
      if mood in candidate: # if mood in candidate, return it.
        return mood
      else:
        return candidate[random.randrange(0, len(candidate))]