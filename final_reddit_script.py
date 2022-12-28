# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 00:05:29 2022

@author: bdcre
"""

#Final reddit script


#Reference: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

import praw
# # from praw.models import Reddit
from praw.models import MoreComments
from praw.models import Submission
from praw.models import Subreddit

import pandas as pd
import time
import os
import hashlib
from tqdm import tqdm
#%%
#Authorized instance
reddit = praw.Reddit(client_id="4MgxPl_trktjfzL0s0Q-pQ",         # your client id
                                client_secret="zt__lqVHeA-6l821H_oSENG4nGIN8g",      # your client secret
                                user_agent="Automatic-Sky656_test_scrape",        # your user agent
                                username="Automatic-Sky656",        # your reddit username
                                password="-HZR6GchuidQC5a",
                                check_for_async=False)  



#Hash func:
    
def id_hash(username, salt):    
          
      
    # Adding salt at the last of the password
    hashed_user = username+salt
    # Encoding the password
    ret = hashlib.md5(hashed_user.encode())
  
    # return the Hash
    return(ret.hexdigest())

#%%
#Main function

def scrape_subreddit(subreddit_name, limit):
    subreddit = reddit.subreddit(subreddit_name)
    #comments = subreddit.comments(limit=100)#None
    submissions = subreddit.hot(limit = limit)
    comment_data = []
    #for submission in subreddit.async_hot(limit=10) : #.hot
    for submission in tqdm(submissions):
        submission_title = submission.title
        submission_body = submission.selftext
        if submission_body is None:
            submission_body = 'None'
        #print(submission_title)
        for comment in submission.comments:
            #comment.refresh()
            if isinstance(comment, MoreComments) or comment.author is None:
                continue
                # comment_dict = {
                #     'submission_title': submission_title,
                #     'submission_url': submission_url,
                #     'username': '[deleted]',
                #     'comment': comment.body,
                #     'replies': [],
                #     'id': comment.id,
                # }
            else:
                if comment.author is not None:
                    comment_user_id = id_hash(comment.author.name, '5gz')
                    comment_dict = {
                        'subreddit': subreddit_name,
                        'submission_title': submission_title,
                        'submission_text': submission_body,
                        #'real_user': comment.author.name,
                        'username': comment_user_id,
                        'comment': comment.body,
                        'replies': [],
                        'id': comment.id,
                    }
            if comment.replies:
                replies = comment.replies
                for reply in replies:
                    if isinstance(reply, MoreComments) or reply.author is None:
                        continue
                    # print(reply.body)
                    # print(reply.author.name)          
                    else:
                        reply_user_id = id_hash(reply.author.name, '5gz')
                        comment_dict['replies'].append({
                            'username': reply_user_id,
                            'comment': reply.body,
                            'id': reply.id,
                        })           
            comment_data.append(comment_dict)
    return pd.DataFrame(comment_data)


#%%
import pickle
# subreddit_names = ['schizophrenia','bipolar','debt','GamblingAddiction', 'SuicideWatch', 'depression', 'depressed', 'Psychosis', 'antiwork',
#                 'MensRights', 'conspiracy', 'conspiracytheories', 'Bankruptcy', 'Firearms']
# subreddit_names = ['traumatoolbox','socialanxiety','Anger','offmychest', 'mentalhealth','depression_help',
#                    'Antipsychiatry','BipolarReddit','domesticviolence','mentalillness']

subreddit_names = ['schizophrenia','bipolar','debt','GamblingAddiction', 'SuicideWatch', 'depression', 'depressed', 'Psychosis', 'antiwork',
                   'MensRights', 'conspiracy', 'conspiracytheories', 'Bankruptcy', 'Firearms',
                   'traumatoolbox','socialanxiety','Anger','offmychest', 'mentalhealth','depression_help',
                   'Antipsychiatry','BipolarReddit','domesticviolence','mentalillness']
dfs = []
#print(dfs[0])
for subreddit_name in subreddit_names:
    comments_df = scrape_subreddit(subreddit_name,
                                   limit = 5000)
    # Save the comments to a CSV file
    #comments_df.to_csv(f'{subreddit_name}_comments.csv', index=False)
    dfs.append(comments_df)
    # Pause the script for 10 seconds
    time.sleep(10)


all_data2 = pd.concat(dfs)
# all_data2.to_csv('ALL_REDDIT_DATA2.csv')
# all_data2.to_pickle('ALL_REDDIT_PKL2.pkl')

# #%%
# #pkl test

# test2 = pd.read_pickle('ALL_REDDIT_PKL2.pkl')