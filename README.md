# Heart-To-Heart bot
#### Table of Contents
* [Install](#install)
* [Purpose](#purpose)
    * [Why this motivation](#why-this-motivation)
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
	* <img src="https://i.imgur.com/ocNeGSO.jpg" width="200" height="355" />
    * bot will show you its description first
	* <img src="https://i.imgur.com/f4wbxQq.jpg" width="200" height="355" />

2. Choose interaction with bot
    1. Joke
        * press **`Joke`** from **start**
		* <img src="https://i.imgur.com/wpQGlya.jpg" width="200" height="355" />
        * press comment (here is **`funny`**)
		* <img src="https://i.imgur.com/LO8XW4T.jpg" width="200" height="355" />
        * then, you can
            * press **`Next joke`** to get randomly new joke (from about 100 jokes)
            * press **`Back`** to back **start**
            * (here is **`Back`**)
    2. Riddle
        * press **`Riddle`** from **start**
		* <img src="https://i.imgur.com/K1pVRUE.jpg" width="200" height="355" />
        * answer this riddle (my answer is **`不知道`**)
		* <img src="https://i.imgur.com/GqJlXZF.jpg" width="200" height="355" />
        * bot reply answer to you
		* <img src="https://i.imgur.com/WGm615U.jpg" width="200" height="355" />
        * then, you can
            * press **`Next riddle`** to get randomly new riddle (from about 250000 riddles)
            * press **`Back`** to back **start**
            * (here is **`Back`**)
    3. Video
        * press **`Video`** from **start**
		* <img src="https://i.imgur.com/DLP5rvt.jpg" width="200" height="355" />
        * then, you can
            * press **`Suggestion from bot`**
            * press **`Search yourself`**
        * here press **`Suggestion from bot`** first
		* <img src="https://i.imgur.com/RYnHZt6.jpg" width="200" height="355" />
        * then, you can choose one mood (here is **`happy`**)
        * different mood will get different videos
		* <img src="https://i.imgur.com/n3gDb5H.jpg" width="200" height="355" />
        * then, you can
            * press **`Suggestion from bot again`**
            * press **`Back`** to back **start**
            * here is **`Back`**, because we should press the above mentioned **`Search yourself`**
        * press **`Search yourself`**
		* <img src="https://i.imgur.com/XyU0pOD.jpg" width="200" height="355" />
        * then you should give keyword to bot (here is **`倔強`**)
		* <img src="https://i.imgur.com/yaDYSWs.jpg" width="200" height="355" />
        * bot will reply one of result of search to you (from three result)
		* <img src="https://i.imgur.com/Uycbq1R.jpg" width="200" height="355" />
        * then, you can
            * press **`No, search again.`** to restart to serach
            * press **`Yes, got it`** to back **start**
    4. Chat
        * press **`Chat`** from **start**
        * after press **`Chat`**, the language will be in Chinese temporarily
        * then, bot will ask your mood now
		* <img src="https://i.imgur.com/2XiL7dL.jpg" width="200" height="355" />
        * press your mood (here is **`開心`**)
        * different mood will get different picture and one mood maybe get different picture(from 2)
        * then, bot will reply message "Waiting for sending picture"
		* <img src="https://i.imgur.com/UOAFOfT.jpg" width="200" height="355" />
        * after picture be sent, message will change to "Hope this picture can let you be more happy"
		* <img src="https://i.imgur.com/FX8pDWy.jpg" width="200" height="355" />
        * then, you can
            * press **`有`** to back **start**
            * press **`沒有`** to chat with bot deeply
            * here is **`沒有`**
		* <img src="https://i.imgur.com/dtH9T5D.jpg" width="200" height="355" />
        * then, you can chat with bot three times~
        * bot will try to judge what your semantic of words is, and give reply to you
		* <img src="https://i.imgur.com/prv4YTM.jpg" width="200" height="355" />
		* <img src="https://i.imgur.com/u02YuwE.jpg" width="200" height="355" />
		* <img src="https://i.imgur.com/Jygiblz.jpg" width="200" height="355" />

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
		* <img src="https://i.imgur.com/UaMYXMU.jpg" width="300" height="100" />
    * description
		* <img src="https://i.imgur.com/2c8gDXR.jpg" width="200" height="180" />

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
