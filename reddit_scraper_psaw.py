# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 16:56:04 2022

@author: bdcre
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:24:30 2022

@author: brandon.creech
"""


#Reddit scraping with PSAW (pushshift io)
#%%

from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import time

api = PushshiftAPI()


#%%
# subreddits = ['schizophrenia','bipolar','debt','GamblingAddiction', 'SuicideWatch', 'depression', 'depressed', 'Psychosis', 'antiwork',
#               'MensRights', 'conspiracy', 'conspiracytheories', 'Bankruptcy', 'Firearms']
subreddits = ['debt']
num_subreddits = (len(subreddits)*5000)
#%%
#Search submissions
start = time.time()

start_epoch=int(dt.datetime(2019, 1, 1).timestamp())

gen = api.search_submissions(after=start_epoch,
                            subreddit=subreddits,
                            filter=['title', 'selftext','comments', 'subreddit'],
                            limit=num_subreddits)


post_df = pd.DataFrame([thing.d_ for thing in gen])

end = time.time()

elapsed = int(end-start)/60
print(str(elapsed) + " minutes to scrape " + str(len(subreddits)) + " subreddits.")

#post_df.to_csv("Desktop/reddit_data.csv")

#Remove blank or removed posts:

#%%
#Try  looping to get equal groups (if possible)

appended_data = []
start_epoch=int(dt.datetime(2018, 1, 1).timestamp())

start = time.time()

for sbrdt in subreddits:

    gen = api.search_submissions(after=start_epoch,
                                subreddit=sbrdt,
                                filter=['title', 'selftext','comments', 'subreddit'],
                                limit=7500)


    post_df = pd.DataFrame([thing.d_ for thing in gen])
    appended_data.append(post_df)
    
    
elapsed = int(end-start)/60
print(str(elapsed) + " minutes to scrape " + str(len(subreddits)) + " subreddits.")

total_data = pd.concat(appended_data)


#%%

total_data.groupby(['subreddit']).size()

dep = total_data[total_data['subreddit'] == 'depression']

clean_data = total_data[total_data['selftext'].str.contains('[removed]', regex = False) == False]
dep = clean_data[clean_data['subreddit'] == 'depression']



clean_data.groupby(['subreddit']).size()

clean_data.to_csv("Desktop/filtered_reddit_data.csv")


#%%
#Search comments
start_epoch=int(dt.datetime(2015, 1, 1).timestamp()) # Could be any date
    
comments_gen = api.search_comments(after=start_epoch, subreddit='schizophrenia', limit=1000) # Returns a generator object
comments_df = pd.DataFrame([comm.d_ for comm in comments_gen])


#%%
#All AskReddit comments containing the text “OP”

gen = api.search_comments(q='OP', subreddit='askreddit')

max_response_cache = 1000
cache = []

for c in gen:
    cache.append(c)

    # Omit this test to actually return all results. Wouldn't recommend it though: could take a while, but you do you.
    if len(cache) >= max_response_cache:
        break

# If you really want to: pick up where we left off to get the rest of the results.
if False:
    for c in gen:
        cache.append(c)