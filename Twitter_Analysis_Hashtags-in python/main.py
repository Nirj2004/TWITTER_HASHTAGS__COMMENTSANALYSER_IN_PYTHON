import tweepy 
import csv 
import pandas as pd 
account_key = 'Provide you account password here'
account_secret_answer = 'Provide your personal selected anser to the question asked on the app or website'
account_token = 'Provide your token number here'
account_secret_token = 'Provide your private token number here'
auth = tweepy.QAuthHandler(account_key, account_secret_answer)
auth.set_account_token(account_token, account_secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True)
csvFile = open('tweets.csv', 'w')
csvWriter = csv.writer(csvFile)
for tweet in tweepy.Cursor (api.search,w="#ExploreMLBLR",count=100,lang="en",since="2022-01-10").items():
    csvWriter.writerow([tweet.user.screen_name, tweet.text.encode('utf-8/BOM')])
csv = pd.read_csv('tweets.csv',names=["Username","Tweet"])
count = csv['Username'].value_counts()[:]
csv.head(20)
top2 = count.head(2)
top2
import matplotlib.pyplot as plt 
colors = ["#E13F29", "#D663B59", "#CB5C3B", "#EB8076", "#96224E"]
top2.plot.pie(y=top2.index, shadow=False,colors=colors,radius=1000,explode=(0, 0),startangle=90,autopct='%1.1f%%',textcrops={'fontsize': 10})
plt.axis('equal')
plt.tight_layout()
plt.show()