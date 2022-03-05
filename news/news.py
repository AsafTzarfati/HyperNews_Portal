from datetime import datetime
from django.conf import settings
import json
from collections import OrderedDict
import random


class Links:
    """
    Links class created to manage fast actions with links using a dictionary (hash table).
    """
    free_links = dict()

    def __init__(self):
        # create 10 million free links
        self.free_links = {i: i for i in range(10000000)}

    def get_uniq_link(self):
        link = random.choice(self.free_links)
        # update free links dict
        return self.free_links.pop(link, 'Link not exist')

    def update(self, links):
        # pop out occupied links
        for link in links:
            self.free_links.pop(link, 'Link not exist')

    def is_occupied(self, link):
        return link not in self.free_links.values()


def group_by_date(news_list):
    news_by_date_dict = dict()
    for news in news_list:
        created = news.get("created")
        # Extracting the date form the date and time string to be the key
        # of new dictionary
        key = str(datetime.strptime(created, "%Y-%m-%d %H:%M:%S").date())

        if key in news_by_date_dict:
            news_by_date_dict[key].append(news)
        else:
            # if key (date) doesn't exist add a this key with value of list
            # each value in the list is news
            news_by_date_dict[key] = list()
            news_by_date_dict[key].append(news)
    return news_by_date_dict


def sort_by_date(links, news_list):
    links.update(split_links(news_list))
    ordered_dict = build_ordered_dict(news_list)
    return {"context": ordered_dict}


def search_news(search, news_list):
    context = dict()
    matching_titles = [news for news in news_list if search in news["title"]]
    if matching_titles:
        context["context"] = group_by_date(matching_titles)
        return context
    return None


def split_links(news_list):
    all_links = list()
    for news in news_list:
        all_links.append(news["link"])
    return all_links


def write_json(dict_to_write):
    with open(settings.NEWS_JSON_PATH, "w") as json_file:
        json.dump(dict_to_write, json_file)


def read_json():
    with open(settings.NEWS_JSON_PATH, "r") as json_file:
        return json.load(json_file)


def update_json(article, news_list):
    news_list.append(article)
    write_json(news_list)


def build_ordered_dict(news_list):
    news_by_date_dict = group_by_date(news_list)
    return OrderedDict(sorted(news_by_date_dict.items(), reverse=True))
