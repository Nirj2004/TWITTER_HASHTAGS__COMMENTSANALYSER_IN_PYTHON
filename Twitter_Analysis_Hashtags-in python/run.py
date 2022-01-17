from CommentBot import CommentBot
import tweepy
import configparser
import os 

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/config/anecbotalNYT.conf")

account_password = config.get("TwitterConfig", "account_password")
account_secret = config.get("TwitterConfig", "account_secret")
access_token = config.get("TwitterConfig", "access_token")
access_token_secret = config.get("TwitterConfig", "access_secret_token")
auth = tweepy.QAuthHandler(account_password, account_secret)
auth.set_access_token(access_token, access_token_secret)
cb = CommentBot()
while 1 != 0:
    print("starting a new run .")
    cb.stream = tweepy.Stream(auth, cb)
    cb.stream.filter(track=cb.filter_object)
    