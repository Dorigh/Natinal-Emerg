import csv
import pandas as pd
from twython import Twython

# Read credentials
with open('./cred.txt','r') as cr:
    cred = cr.read()[:-1].split('\n')

credentials = {'APP_KEY': cred[0], 'APP_SECRET': cred[1], 'ACCESS_TOKEN': cred[2], 'ACCESS_SECRET': cred[3]}
python_tweets = Twython(credentials['APP_KEY'],credentials['APP_SECRET'])

# Read state data
states = pd.read_csv('files/States.csv')
geo = states['Geo']
sta = states['State']

# Loop over states' capital and date 
dict_ = {'user': [], 'date': [], 'text': [], 'id':[], 'favorite_count': [], 'retweet_num': [], 'state': []} 
for i in range(0,len(geo)):
    for j in range(10,17):
        query = {'q': '#COVID-19 -filter:retweets AND -filter:replies',
                 'count': 200,
                 'lang': 'en',
                 'until': '2020-03-%s' % j,
                 'geocode': geo[i]}
    
        for status in python_tweets.search(**query)['statuses']:  
            dict_['user'].append(status['user']['screen_name'])
            dict_['date'].append(status['created_at'])
            dict_['text'].append(status['text'])
            dict_['id'].append(status['id'])
            dict_['favorite_count'].append(status['favorite_count'])
            dict_['retweet_num'].append(status['retweet_count'])
            dict_['state'].append(sta[i])

# Save outputs as CSV
df = pd.DataFrame(dict_)
df.to_csv ('twitter_query.csv', index = False, header = True, quoting = csv.QUOTE_NONNUMERIC)
