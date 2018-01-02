# Heart-To-Heart bot
#### Table of Contents
* [Install](#install)
* [Purpose](#purpose)
    * [Why this purpose](#why-this-purpose)
* [Launch](#launch)
* [Functionality](#functionality)
* [Usage and Scene](#usage-and-scene)
* [FSM](#fsm)
* [Advantage](#advantage)
* [Disadvantage](#disadvantage)
* [Files description in this repo](#description-of-files-in-this-repo)

## Install
1. clone this repository
```
$ git clone https://github.com/e652424342007/Heart-to-Heart-bot 
```
2. install prior required Python3 package with `pip`
```
$ pip install -r requirements.txt
```
Note: you can use `virtualenv` to create a virtual environment for this bot
## Purpose
* The purpose of this telegram bot is that make your mood become better, No matter you are happy or unhappy now.

#### Why this motivation
* I thought that many people beside us are often in a bad mood in their lives. As a result, in order to express their mood, these people may need other people to talk with. However, most people in the modern society are busy all over time. This kind of phonomanon will cause that someone needs to company, but nobody can accompany with him or her. Therefore, people who feel bad at that time may be more homesick, sad, angry, depressed, tired and stressed.
* As mentioned reason above, so this bot is born!

## Launch
If run on local device:
```
$ ./ngrok http 5000
```
and copy forwarding address to `bot_.py`
```python
WEBHOOK_URL = 'forwarding address/hook'
```

then, run the bot
```
$ python bot_.py
```
Note: the version of `python` should be Python3.

## Functionality
1. Give you some jokes.
2. Give you some riddles.
3. Suggest you some videos or search videos on online
4. Simply chat with you

## Usage and Scene
1. Start interacting with HTH-bot
    * ***search `familysbot` on telegram***
    * ![](https://i.imgur.com/ocNeGSO.jpg =200x)
    * bot will show you its description first
    * ![](https://i.imgur.com/f4wbxQq.jpg =200x)

2. Choose interaction with bot
    1. Joke
        * press **`Joke`** from **start**
        * ![](https://i.imgur.com/wpQGlya.jpg =200x)
        * press comment (here is **`funny`**)
        * ![](https://i.imgur.com/LO8XW4T.jpg =200x)
        * then, you can
            * press **`Next joke`** to get randomly new joke (from about 100 jokes)
            * press **`Back`** to back **start**
            * (here is **`Back`**)
    2. Riddle
        * press **`Riddle`** from **start**
        * ![](https://i.imgur.com/K1pVRUE.jpg =200x)
        * answer this riddle (my answer is **`不知道`**)
        * ![](https://i.imgur.com/GqJlXZF.jpg =200x)
        * bot reply answer to you
        * ![](https://i.imgur.com/WGm615U.jpg =200x)
        * then, you can
            * press **`Next riddle`** to get randomly new riddle (from about 250000 riddles)
            * press **`Back`** to back **start**
            * (here is **`Back`**)
    3. Video
        * press **`Video`** from **start**
        * ![](https://i.imgur.com/DLP5rvt.jpg =200x)
        * then, you can
            * press **`Suggestion from bot`**
            * press **`Search yourself`**
        * here press **`Suggestion from bot`** first
        * ![](https://i.imgur.com/RYnHZt6.jpg =200x)
        * then, you can choose one mood (here is **`happy`**)
        * different mood will get different videos
        * ![](https://i.imgur.com/n3gDb5H.jpg =200x)
        * then, you can
            * press **`Suggestion from bot again`**
            * press **`Back`** to back **start**
            * here is **`Back`**, because we should press the above mentioned **`Search yourself`**
        * press **`Search yourself`**
        * ![](https://i.imgur.com/XyU0pOD.jpg =200x)
        * then you should give keyword to bot (here is **`倔強`**)
        * ![](https://i.imgur.com/yaDYSWs.jpg =200x)
        * bot will reply one of result of search to you (from three result)
        * ![](https://i.imgur.com/Uycbq1R.jpg =200x)
        * then, you can
            * press **`No, search again.`** to restart to serach
            * press **`Yes, got it`** to back **start**
    4. Chat
        * press **`Chat`** from **start**
        * after press **`Chat`**, the language will be in Chinese temporarily
        * then, bot will ask your mood now
        * ![](https://i.imgur.com/2XiL7dL.jpg =200x)
        * press your mood (here is **`開心`**)
        * different mood will get different picture and one mood maybe get different picture(from 2)
        * then, bot will reply message "Waiting for sending picture"
        * ![](https://i.imgur.com/UOAFOfT.jpg =200x)
        * after picture be sent, message will change to "Hope this picture can let you be more happy"
        * ![](https://i.imgur.com/FX8pDWy.jpg =200x)
        * then, you can
            * press **`有`** to back **start**
            * press **`沒有`** to chat with bot deeply
            * here is **`沒有`**
        * ![](https://i.imgur.com/dtH9T5D.jpg =200x)
        * then, you can chat with bot three times~
        * bot will try to judge what your semantic of words is, and give reply to you
        * ![](https://i.imgur.com/prv4YTM.jpg =200x)
        * ![](https://i.imgur.com/u02YuwE.jpg =200x)
        * ![](https://i.imgur.com/Jygiblz.jpg =200x)

## FSM
[FSM picture link](https://i.imgur.com/k1wNsh1.png)
![](https://i.imgur.com/k1wNsh1.png)

## advantage
* I think this bot is practical 😀
* web crawler
* web searching
* Sending images
* Simple natural language processing with [Jieba](https://github.com/fxsjy/jieba)
* Use *InlineKeyboardButton* to interact with user and dynamicly update message
* Set description and command list
    * command list
        * ![](https://i.imgur.com/UaMYXMU.jpg =300x)
    * description
        * ![](https://i.imgur.com/2c8gDXR.jpg =200x)

## disadvantage
* No database
* Bot cannot serve two or more users simultaneously
    * It can use this method to solve
        * One user, one machine
* When bot chat with user, it will try to judge semantic of words of user's input. About **'judge'**, bot is sometimes weak.
    * We can add more and more word to bot, and then bot will **judge** more precise

## Description of files in this repo
* directory
    * ***`img`*** : store some images
    * ***`words`*** : store words about specific mood
        * These words are used by [Jieba](https://github.com/fxsjy/jieba)
* file
    * **`bot_.py`** : judge what state now, and what transition be triggered
    * **`fsm.py`** : all of callback function about specific transition
    * **`cutter.py`** : `class jieba_er`
        * used to judge semantic of words
    * **`joke_spider.py`** : `class joke_maker`
        * used to get joke from [here](http://kids.yam.com/joke/topjoke.php)
    * **`riddle_spider.py`** : `class riddle_maker`
        * used to get riddle from [here](http://kids.yam.com/riddle/newriddle.php)
    * **`stop.txt`** and **`userdic.txt`** :
        * used by jieba
    * **`Procfile`**, **`runtime.txt`**: 
        * used by heroku 
