import requests
from bs4 import BeautifulSoup
from threading import Thread
import re
import random


class RandQuote:
    def __init__(self):
        self.url = "https://www.twitchquotes.com/copypastas/labels/{}"
        self.get_cats()

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
        cat_url = "https://www.twitchquotes.com/copypastas/labels"
        souper_duper = BeautifulSoup(
            requests.get(cat_url).text, features='lxml')
        attr = {"class": "-copypasta-tag-name"}
        topics = [self.remove_html(str(i).replace(" ", '').replace("\n", ""))
                  for i in souper_duper.find_all('div', attr)]
        self.topics = topics