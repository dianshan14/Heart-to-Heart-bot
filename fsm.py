from transitions.extensions import GraphMachine
from pygraphviz import * 
from riddle_spider import riddle_maker
from joke_spider import joke_maker
from user import user_msg
from cutter import jieba_er
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import urllib.request
import urllib.parse
import re
import random

video_list = {'Happy':    [["https://www.youtube.com/watch?v=gJhpYPECs40","t.A.T.u.-Gomenasai"],
                           ["https://www.youtube.com/watch?v=TBXQu8ORnBQ","Charlie Puth-Dangerously"],
                           ["https://www.youtube.com/watch?v=f0ZDypwI1Gc","黃明志-搞笑快行動"]],
              'Angry':    [["https://www.youtube.com/watch?v=BsVq5R_F6RA","Anger Management Techniques"],
                           ["https://www.youtube.com/watch?v=YwlwSByGOWY","9 Tips To Control your Anger"],
                           ["https://www.youtube.com/watch?v=GzliJGwIEV8","宮崎駿 鋼琴音樂 BGM"]],
              'Sad':      [["https://www.youtube.com/watch?v=3U5Pd6XVJAY","元衛覺醒-夏天的風"],
                           ["https://www.youtube.com/watch?v=IteE-HMVJ1M","周杰倫-世界未末日"],
                           ["https://www.youtube.com/watch?v=e0g4ouvZi44","高進-有太多人"]],
              'Depressed':[["https://www.youtube.com/watch?v=WVI26f0diYs","夢想．激勵人心的演說"],
                           ["https://www.youtube.com/watch?v=0Am3C-KH8RE","翁立友 & 蕭煌奇-堅持"],
                           ["https://www.youtube.com/watch?v=UHBqEn93NlI","光良 & 曹格-少年"],
                           ["https://www.youtube.com/watch?v=UYkHC8Sf4dY","34bit-You Should Try"]],
              'Homesick': [["https://www.youtube.com/watch?v=Yqw6c5R_KAs","李榮浩-歌謠"],
                           ["https://www.youtube.com/watch?v=B_WyWC1WXPw","黃美珍-只怕想家"],
                           ["https://www.youtube.com/watch?v=FG9M0aEpJGE","G-Eazy & Kehlani-Good Life"],],
              'Tired':    [["https://www.youtube.com/watch?v=nBK9z5XbKKQ","李玖哲-Right Here Waiting"],
                           ["https://www.youtube.com/watch?v=Pk770hiuaoU","何耀珊-你的肩膀"]],
              'Bored':    [["https://www.youtube.com/watch?v=0yXDtzrAT8o","慘叫雞秒變唱將"],
                           ["https://facebook.com/kaichedashen/videos/1356600014449070/","小三輪一路狂飆，搶月餅紛紛亮招！"],
                           ["https://facebook.com/kaichedashen/videos/1322237531218652/","路虎加塞變路狗，司機當街出了醜！"],
                           ["https://www.facebook.com/boss198473/videos/197675567368649/","到底是誰配的音阿!!"],
                           ["https://facebook.com/shewolf.com.my/videos/1758866424359808/","就好好唱啊.."],
                           ["https://www.youtube.com/watch?v=cxSe-avMgLg","搞笑配音，奧運會跳水隊"]],
              'Stressed': [["https://www.youtube.com/watch?v=DahDsnn_Hpc","王力宏-需要人陪"],
                           ["https://www.youtube.com/watch?v=e0g4ouvZi44","高進-有太多人"],
                           ["https://www.youtube.com/watch?v=Sl8TA9r7-SU","頑童MJ116-SOUTH SIDE"]]
             }

text_list = {
    "開心" : ["聽起來你很高興，只要你開心我就開心", "希望你的快樂能一直延續下去"],
    "生氣" : ["不要生氣 試試調整你的呼吸\n會有很好的效果", "想想自己生氣的事情是不是值得生氣，\n不值得的話就忘記吧"],
    "難過" : ["不要覺得難過，我都會在這裡陪著你\n與你同在", "告訴自己難過不要超過一天，\n一天過後又是更堅強的自己"],
    "沮喪" : ["想想你的目標，你需要藉由堅持來靠近它！", "我們生活中充滿不如意的事情，\n想想那些你擁有的，\n你會感到幸福"],
    "疲累" : ["什麼事讓你感到疲憊呢？\n給自己一個休息的時間，\n你將會充滿力氣！", "疲累的時候，\n想想你的夢想，想想你的目標，\nJust do it!"],
    "無聊" : ["那就參考一些我推薦你的影片或是圖片吧～", "利用我的搜尋功能，\n關鍵字:『搞笑』，你就會解決你的無聊～"],
    "有壓力" : ["什麼事讓你感到有壓力呢？\n試著用不同的角度思考吧～你會得到解答", "去一個人煙稀少的地方，\n吶喊吧！\n或是你可以考慮繼續跟我聊天～"]
}


class TocMachine(GraphMachine):
    
    user_list = []

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs,
            title="Heart-to-Heart-bot"
        )
        
        self.answer = ""
        self.msg = None
        self.user = ""
        self.chat_times = 0
        self.mood = ""
        self.jiebaer = jieba_er()
        self.be_token = []

# start
    def start_msg(self, update):
        if self.msg != None and self.chat_times <= 1:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        self.chat_times = 0

        keyboard = [[InlineKeyboardButton("Joke", callback_data='Joke'), InlineKeyboardButton("Riddle", callback_data='Riddle')],
                    [InlineKeyboardButton("Video", callback_data='Video'), InlineKeyboardButton("Chat", callback_data='Chat')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query == None:
            self.user = update.message.from_user.first_name+" "+update.message.from_user.last_name
            if self.user not in self.user_list:
                self.user_list.append(self.user)
            self.msg = update.message.reply_text("Hello, welcome to Heart-to-Heart-bot, %s.\nI can do some interaction with you 😀.\nYou can enter /restart to restart this bot.\nPlease choose one interaction below"%self.user, reply_markup=reply_markup)
        else:
            self.msg = update.callback_query.message.reply_text("Hello, welcome to Heart-to-Heart-bot, %s.\nI can do some interaction with you 😀.\nYou can enter /restart to restart this bot.\nPlease choose one interaction below"%self.user, reply_markup=reply_markup)


        
# joke
    def give_joke(self, update):

        if self.msg != None:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        marker = joke_maker()
        marker.get_joke_url()
        joke = marker.get_joke()

        keyboard = [[InlineKeyboardButton("Bad", callback_data='Bad')],
                    [InlineKeyboardButton("Normal", callback_data='Normal')],
                    [InlineKeyboardButton("Funny", callback_data='Funny')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.callback_query != None:
            self.msg = update.callback_query.message.reply_text(joke + "\n\nComment this joke 😊", reply_markup=reply_markup)
        else:
            self.msg = update.message.reply_text(joke + "\n\nComment this joke 😊", reply_markup=reply_markup)
        print("\njoke:\n" + joke)

        return
    
    def comment_joke(self, update):
        # after inline keyboard reply
        if update.callback_query != None:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)
            ask = "\n\nNow, you want ?"
            if update.callback_query.data == 'Bad':
                text = "Sorry! I will not give this joke for you next time!🤫" + ask
            elif update.callback_query.data == 'Normal':
                text = "Hope you can get more joy from me😃" + ask
            elif update.callback_query.data == 'Funny':
                text = "Great! Let's laugh🤩🤣" + ask

            keyboard = [[InlineKeyboardButton("Next joke", callback_data="Next joke"),
                         InlineKeyboardButton("Back", callback_data="Back")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            self.msg = update.callback_query.message.reply_text(reply_markup=reply_markup, text=text)
            return True
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nPlease press inline keyboard~")
            return False

    def question_joke(self, update):
        # check the reply from user -> Next joke or Back
        if update.callback_query != None:
            if update.callback_query.data == "Next joke":
                return True # next joke
            elif update.callback_query.data == "Back":
                return False
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False

# riddle
    def give_riddle(self, update):
        if self.msg != None:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        maker = riddle_maker()
        maker.get_riddle_url()
        riddle = maker.get_riddle()

        if update.callback_query != None:
            self.msg = update.callback_query.message.reply_text("Riddle: %s\n\nprompt: %s"%(riddle['Riddle'], riddle['prompt']) + "\n\nAnswer this riddle 😁")
        else:
            self.msg = update.message.reply_text("Riddle: %s\n\nprompt: %s"%(riddle['Riddle'], riddle['prompt']) + "\n\nAnswer this riddle 😁")
        
        self.answer = riddle['answer']
        print("\nRiddle:'%s'\nPrompt:'%s'"%(riddle['Riddle'], riddle['prompt']))
        print("Ans:'%s'\n"%(self.answer))

    def answer_riddle(self, update):
        keyboard = [[InlineKeyboardButton("Next riddle", callback_data="Next riddle"),
                     InlineKeyboardButton("Back", callback_data="Back")]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = update.message.text
        if msg == "":
            self.msg = update.message.reply_text("Don't give up, you will guess right next!🗿\n\nThe answer is '%s'"%(self.answer), reply_markup=reply_markup)
            return
        if msg in self.answer or msg.lower() == self.answer.lower():
            self.msg = update.message.reply_text("Correct. You are the best!👍\n\nThe answer is '%s'"%(self.answer), reply_markup=reply_markup)
        else:
            self.msg = update.message.reply_text("Don't give up, you will guess right next!🗿\n\nThe answer is '%s'"%(self.answer), reply_markup=reply_markup)

    def question_riddle(self, update):
        # check the reply from user -> Next riddle or Back
        if update.callback_query != None:
            if update.callback_query.data == "Next riddle":
                return True # next riddle
            elif update.callback_query.data == "Back":
                return False
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False

# music
    # suggest
    def question_music(self, update):
        if self.msg != None:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        keyboard = [[InlineKeyboardButton("Suggestion from bot", callback_data="Suggestion from bot"),
                     InlineKeyboardButton("Search yourself", callback_data="Search yourself")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query != None:
            self.msg = update.callback_query.message.reply_text("Where is video you would like to listen?", reply_markup=reply_markup)
        else:
            self.msg = update.message.reply_text("Where is video you would like to listen?", reply_markup=reply_markup)

    def where_music(self, update):
        if update.callback_query != None:
            if update.callback_query.data == "Suggestion from bot":
                return True # suggestion 
            elif update.callback_query.data == "Search yourself":
                return False # search
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False

    def question_mood(self, update):
        if self.msg != None: # 回到這裡可以清掉 回到 start 也被清掉
            self.msg = self.msg.edit_reply_markup(reply_markup=None)
        keyboard = [[InlineKeyboardButton("Happy", callback_data="Happy"),
                     InlineKeyboardButton("Angry", callback_data="Angry"),
                     InlineKeyboardButton("Sad", callback_data="Sad"),
                     InlineKeyboardButton("Depressed", callback_data="Depressed")],
                    [InlineKeyboardButton("Homesick", callback_data="Homesick"),
                     InlineKeyboardButton("Tired", callback_data="Tired"),
                     InlineKeyboardButton("Bored", callback_data="Bored"),
                     InlineKeyboardButton("Stressed", callback_data="Stressed")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query != None:
            self.msg = update.callback_query.message.reply_text("How are you feeling now?", reply_markup=reply_markup)
        else:
            self.msg = update.message.reply_text("How are you feeling now?", reply_markup=reply_markup)


    def mood_music(self, update):
        # this is song my suggestion ^^
        if self.msg != None:
            self.msg = self.msg.edit_reply_markup(reply_markup=None)
        
        text = "These videos are my suggestion😉\n"

        for i, content in enumerate(video_list[update.callback_query.data]):
            text = text +"\n" + str(i+1) + ". [" + content[1] + "](" + content[0] + ")"
        text = text + "\n"
        print(text)

        keyboard = [[InlineKeyboardButton("Suggestion from bot again", callback_data="Suggestion from bot again")],
                    [InlineKeyboardButton("Back", callback_data="Back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        self.msg = update.callback_query.message.reply_text(text=text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

    def suggest_next(self, update): # 也是直接跳 但是會發生
        # 不用清掉 因為只是決定去哪裡 去的地方會清掉
        if update.callback_query != None:
            if update.callback_query.data == "Suggestion from bot again":
                return True # suggestion again
            elif update.callback_query.data == "Back":
                return False # back to start
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False

    # search
    def search(self, update):
        if self.msg != None: # 回到這裡可以清掉 回到 start 也被清掉
            self.msg = self.msg.edit_reply_markup(reply_markup=None)
        
        self.msg = update.callback_query.message.reply_text("Tell me keyword 💪🏻\nI will search this keyword on YouTube")

    def result_and_question(self, update):
        # must from normal message
        keywords = urllib.parse.urlencode({"search_query" : update.message.text })
        text = urllib.request.urlopen("http://www.youtube.com/results?" + keywords)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', text.read().decode())

        result = []
        for i in range(len(search_results)):
            site = "http://www.youtube.com/watch?v=" + search_results[i]
            if site not in result:
                result.append(site)

        print("")
        for x in result:
            print(x)
        print("")

        text = "Here is one of result of search \n" + result[random.randrange(0, 3)]

        keyboard = [[InlineKeyboardButton("No, search again.", callback_data="No, search again.")],
                    [InlineKeyboardButton("Yes, got it.", callback_data="Yes, got it.")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        self.msg = update.message.reply_text(text=text, reply_markup=reply_markup)
        
        pass

    def happy_result(self, update):
        # 回去的地方會清掉
        if update.callback_query != None:
            if update.callback_query.data == "No, search again.":
                return True # search again
            elif update.callback_query.data == "Yes, got it.":
                return False # back to start
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False
        
# chat
    def chat_question_mood(self, update):
        if self.msg != None: # 回到這裡可以清掉 回到 start 也被清掉
            self.msg = self.msg.edit_reply_markup(reply_markup=None)
        keyboard = [[InlineKeyboardButton("開心", callback_data="開心"),
                     InlineKeyboardButton("生氣", callback_data="生氣"),
                     InlineKeyboardButton("難過", callback_data="難過"),
                     InlineKeyboardButton("沮喪", callback_data="沮喪")],
                    [InlineKeyboardButton("疲累", callback_data="疲累"),
                     InlineKeyboardButton("無聊", callback_data="無聊"),
                     InlineKeyboardButton("有壓力", callback_data="有壓力")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        self.msg = update.callback_query.message.reply_text(text="你現在的心情是？🙂", reply_markup=reply_markup)


    def pic_or_text(self, update):
        '''if self.msg != None: # 回到這裡可以清掉 回到 start 也被清掉
            self.msg = self.msg.edit_reply_markup(reply_markup=None) '''
        
        #pic_name = update.callback_query.data + str(random.randrange(1,3)) + ".png"
        
        keyboard = [[InlineKeyboardButton("有", callback_data="有"),
                     InlineKeyboardButton("沒有", callback_data="沒有"),]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        self.msg = update.callback_query.message.reply_text(text="你的心情有更好嗎？", reply_markup=reply_markup)

    def be_better(self, update):
        if self.msg != None and update.callback_query.data != "沒有":
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        if update.callback_query != None:
            if update.callback_query.data == "有":
                return True # question better
            elif update.callback_query.data == "沒有":
                return False # chat deeply
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return True

    def question_better(self, update):
        keyboard = [[InlineKeyboardButton("Chat again", callback_data="Chat again"),
                     InlineKeyboardButton("Back", callback_data="Back"),]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        self.msg = update.callback_query.message.reply_text(text="Now, you want?", reply_markup=reply_markup)

    def pic_again(self, update):
        if update.callback_query != None:
            if update.callback_query.data == "Chat again":
                return True # pic again
            elif update.callback_query.data == "Back":
                return False # back to start
        else:
            update.message.reply_text("Sorry! I don't know what you mean ...\nBack to start ...")
            return False

    def chat_deeply(self, update):
        if self.msg != None and self.chat_times == 0: # 刪掉 有 和 沒有
            self.msg = self.msg.edit_reply_markup(reply_markup=None)

        if update.callback_query != None:
            if self.chat_times >= 3:
                self.msg = update.callback_query.message.reply_text(text="你可以跟我再說一句話🤗\n我將結束這次的聊天，謝謝你告訴我有關你的事情😋")
            elif 0 < self.chat_times <= 1:
                update.callback_query.message.reply_text(text="hahahaha 不會發生？ 假如看到這一句話請通知我 謝謝")
            else:
                self.msg = update.callback_query.message.reply_text(text="可以告訴我更多關於你心情的事情嗎？🤗\n多一點情緒形容詞的話，我能更理解你所說的話💪🏻")
        else:
            if self.chat_times >= 3:
                self.msg = update.message.reply_text(text="你可以跟我再說一句話🤗\n我將結束這次的聊天，謝謝你告訴我有關你的事情😋")
            elif 0 < self.chat_times <= 2:
                self.be_token.append(update.message.text)
                segments = self.jiebaer.token_er(update.message.text)
                # times - 1
                semantic = self.jiebaer.check_semantic(segments, self.mood)
                print("Semantic: %s"%(semantic))
                if self.chat_times == 2:
                    texts = text_list[semantic][self.chat_times-1] + "\n\n你可以跟我再說一句話🤗\n我將結束這次的聊天，謝謝你告訴我有關你的事情😋"
                else:
                    texts = text_list[semantic][self.chat_times-1] + "\n\n可以告訴我更多關於你心情的事情嗎？🤗\n多一點情緒形容詞的話，我能更理解你所說的話💪🏻"
                self.msg = update.message.reply_text(text=texts)
            else:
                self.msg = update.message.reply_text(text="可以告訴我更多關於你心情的事情嗎？🤗\n多一點情緒情容詞的話，我能更理解你所說的話💪🏻")
        
        pass

def init(update, machine):
    machine.answer = ""
    machine.msg = None
    machine.user = ""
    machine.chat_times = 0
    machine.mood = ""
    machine.to_start(update)
    if update.callback_query != None:
        update.callback_query.message.edit_reply_markup(reply_markup=None)

def reply_msg(update, machine):
    pass

def print_something(something):
    print(something)
