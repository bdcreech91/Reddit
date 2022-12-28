# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:00:40 2022

@author: bdcre
"""
#Reddit scraping with PSAW (pushshift io)
#%%

from pmaw import PushshiftAPI
import datetime as dt
import pandas as pd
import time

api = PushshiftAPI()
start_epoch=int(dt.datetime(2019, 1, 1).timestamp())

#%%
def scrape_comments(subreddit):
    comments = []
    for comment in api.search_submissions(after=start_epoch,
                                          subreddit=subreddit, 
                                          limit=1000):
        comments.append({
            'username': comment.author,
            'body': comment.body,
            'replies': [{'username': reply.author, 'body': reply.body} for reply in comment.replies]
        })
    return comments

#%%

subreddits = ['mentalhealth', 'depression', 'anxiety']

comments = []
for subreddit in subreddits:
    comments += scrape_comments(subreddit)
df = pd.DataFrame(comments)
