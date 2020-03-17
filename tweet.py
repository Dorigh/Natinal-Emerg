import json
import csv
import pandas as pd
from twython import Twython

with open('./cred.txt','r') as cr:
    cred = cr.read()[:-1].split('\n')

states = pd.read_csv('files/States.csv')

credentials = {}  
credentials['APP_KEY'] = cred[0] 
credentials['APP_SECRET'] =  cred[1] 
credentials['ACCESS_TOKEN'] = cred[2] 
credentials['ACCESS_SECRET'] = cred[3]

with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)
    
with open("twitter_credentials.json", "r") as file:  
    creds = json.load(file)

python_tweets = Twython(creds['APP_KEY'], creds['APP_SECRET'])

geo = states['Geo']
sta = states['State']
par = states['Political Party']

dict_ = {'user': [], 'date': [], 'text': [], 'id':[], 'favorite_count': [], 'retweet_num': [], 'state': [], 'party': []} 
for i in range(0,len(geo)):
    for j in range(10,17):
        query = {'q': '#COVID-19 -filter:retweets AND -filter:replies',
                 'count': 200,
                 'lang': 'en',
                 'until': '2020-03-%s' % j,
                 'exclude_replies': 'true',
                 'geocode': geo[i]}
    
        for status in python_tweets.search(**query)['statuses']:  
            dict_['user'].append(status['user']['screen_name'])
            dict_['date'].append(status['created_at'])
            dict_['text'].append(status['text'])
            dict_['id'].append(status['id'])
            dict_['favorite_count'].append(status['favorite_count'])
            dict_['retweet_num'].append(status['retweet_count'])
            dict_['state'].append(sta[i])
            dict_['party'].append(par[i])

df = pd.DataFrame(dict_)
df.to_csv ('twitter_query.csv', index = False, header = True, quoting = csv.QUOTE_NONNUMERIC)

writer = pd.ExcelWriter('twitter_query.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name = 'Sheet1')
writer.save()
