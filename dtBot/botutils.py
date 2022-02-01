
import requests
from bs4 import BeautifulSoup
from threading import Thread
import re
import random
import time
class SubNotFoundException(Exception):
    pass


class BotUtils:
    def __init__(self):
        self.subs =  [
            "deepfriedmemes",
            "surrealmemes",
            'nukedmemes',
            'bigbangedmemes',
            'wackytictacs',
            'bonehurtingjuice'
        ]
        self.url = "https://www.twitchquotes.com/copypastas/labels/{}"
        self.topics = self.get_cats()
        self.base_url = "https://reddit.com/r/{}/hot.json"
       # self.memes = self.search_reddit()
        

    def remove_html(self, string):
        html_regex = re.compile(r'<.*?>')
        return html_regex.sub('', string)

    def get_quotes(self, topic):
        soup = BeautifulSoup(requests.get(
            self.url.format(topic)).text, features="lxml")
        return soup.find_all('div', attrs={"class": "-copypasta"})

    def rand_quote(self, topic):
        quotes = self.get_quotes(topic)
        if len(quotes) == 0:
            return ''
        return self.remove_html(str(random.choice(list(quotes))))

    def get_cats(self):
        topics = []
        cat_url = "https://www.twitchquotes.com/copypastas/labels"
        souper_duper = BeautifulSoup(requests.get(cat_url).text, features='lxml')
        attr = {"class": "-copypasta-tag-name"}
        for i in souper_duper.find_all('div', attr):
            cats = self.remove_html(
                str(i).replace(" ", '').replace("\n", ''))
            topics.append(cats)
        return topics

    def search_reddit(self):
        attempt_limit = 20
        attempts = 0
        while True:
            attempts += 1
            rand_sub = str(random.choice(self.subs))
            print("ok uh wtf {}".format(rand_sub))
            sub = self.base_url.format(rand_sub)
            request =  requests.get(sub, headers= {'User-agent': 'Mozilla/5.0'}) 
            if request.status_code == 404:
                raise SubNotFoundException("subreddit: {} not found".format(sub))
            reqjson = request.json()
            if 'data' in reqjson:
                top_posts = reqjson['data']['children']
                roll = random.randint(0, len(top_posts) -1)
                choices = []
                for post in top_posts:
                    choices.append(post)
                post = choices[roll]
                meme = post['data'].get("thumbnail", None)
                return meme
            time.sleep(0.1)
            if attempts >= attempt_limit:
                break
        return False
