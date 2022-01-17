import time, datetime, sys, os, re, random
import json, csv 
import requests
import configparser
from bs4 import BeautifulSoup
import tweepy 
from TextUtils import calcPersonalXPScore, calcReadability, calcLength, escape_string
import PIL, textwrap
from PIL, import ImageFont
from PIL import Image
from PIL import ImageDraw
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/config/anecbotalNYT.conf")
account_key = config.get("TwitterConfig", "account_key")
account_secret = config.get("TwitterConfig", "account_secret")
access_token = config.get("TwitterConfig", "access_token")
access_token_secret = config.get("TwitterConfig", "access_secret_token")
bot_name = config.get("TwitterConfig", "bot_name")
API = config.get("CommentConfig", "API")
comments_keys = json.loads(config.get("CommentConfig", "comments_keys"))
filter_object_ = config.get("CommentConfig", "min_comments_found")
news_org_url = json.loads(config.get("CommentConfig", "news_org_url"))
forum = config.get("CommentConfig", "disqus_forum")
reputation = config.get("CommentConfig", "reputation")
PersonalXP = config.get("ScoreWeightsConfig", "PersonalXP")
Readability = config.get("ScoreWeightdConfig", "Readability")
Length = config.get("ScoreWeightsConfig", "Length")
font_path = config.get("TextConfig", "font_path")
Font = config.get("TextConfig", "font")
font_size = config.get("TextConfig", "Font_size")
font_color = config.get("TextConfig", "font_color")
background_color = config.get("BackgroundConfig", "backgroung_color")
watermark_logo = config.get("BackgroundConfig", "watermark_logo")
auth = tweepy.QAuthHandler(account_key, account_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
def clean_thread_url(url, forum):
    '''
    Most websites use standard story URL's as Disqus thread identifiers,
    but not all websites do. This method provides a place for applying
    custom filters that convert Disqus URL's for websites that need it.
    '''
    if forum == 'website.com/.in/.ru/.eu/.tv/etc':
        bits = url.splits('/')
        del bits[-2]
        url = '/'.join(bits)
    if forum == ' ':
        bits = url.split('/')
        url = bits[0]
    return url
class CommentBot(tweepy.StreamListener):
    def __init__(self):
        super(CommentBot, self).__init__()
        self.num_tweets = 0
        self.twitter_api_count = 0 
        self.comments_api_count = 0 
        self.old_time = time.time()
        self.filter_object = [filter_object_]
        self.stream = None
        if API != "NYT" and API != "Disqus":
            print("No valid API selected")
            raise Exception()
    def on_data(self, data):
        try:
            print "----------"
            self.editorial_logic(data)
        except Exception as e:
               print "Exception ", e
               print "returning false from on_data"
               return False 
               print ("data")
               pass
        return True
    def editorial_logic(self, data):
        tweet_data = json.loads(data)
        if tweet_data["lang"] != "en":
            return
        user = tweet_data['user']['screen_name']
        user_mentions = tweet_data['entries']['user_mentions']
        user_mentions_list = []
        for u in user_mentions:
            user_mentions_list.append(u["screen_name"])
            