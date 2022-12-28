# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 12:23:31 2022

@author: bdcre
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 00:05:29 2022

@author: bdcre
"""

#Final reddit script

#Make account here:
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
#Authorized instance information
reddit = praw.Reddit(client_id="",         # your client id
                                client_secret="",      # your client secret
                                user_agent="",        # your user agent
                                username="",        # your reddit username
                                password="",
                                check_for_async=False)  


#%%
#Hash function to anonymize the usernames.
    
def id_hash(username, salt):    
    
    # Add salt at the last of the password
    hashed_user = username+salt
    
    # Encoding the password
    ret = hashlib.md5(hashed_user.encode())
  
    # Return the Hash
    return(ret.hexdigest())

#%%
#Main function

def scrape_subreddit(subreddit_name, limit):
    
    subreddit = reddit.subreddit(subreddit_name)     # Init the subreddit method.
    submissions = subreddit.hot(limit = limit) # Get the top n posts sorting from Hot.
    comment_data = [] # Create empty list to store data in.
    
    for submission in tqdm(submissions): # Start loop.
        submission_title = submission.title # Get title.
        submission_body = submission.selftext # Get text under the post title.

        if submission_body is None: # If there is no text under post, Change to none. This is error handling.
            submission_body = 'None'
            
        for comment in submission.comments:
            if isinstance(comment, MoreComments) or comment.author is None: # Error handling to skip empty data.
                continue
            
            else: #If data is not empty...
            
                if comment.author is not None: # If the comment has an author(username is not empty)
                    comment_user_id = id_hash(comment.author.name, '5gz') # Create encrypted usernames
                    comment_dict = {        # Create data and store in a dict.
                        'subreddit': subreddit_name,
                        'submission_title': submission_title,
                        'submission_text': submission_body,
                        #'real_user': comment.author.name,
                        'username': comment_user_id,
                        'comment': comment.body,
                        'replies': [],
                        'id': comment.id,
                    }
                    
            if comment.replies: #If comment has replies...
                replies = comment.replies
                
                for reply in replies:
                    if isinstance(reply, MoreComments) or reply.author is None:
                        continue       
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

#Run script in loop and save to Pandas dataframe.
subreddit_names = ['wow','Overwatch']
dfs = []
#print(dfs[0])
for subreddit_name in subreddit_names:
    comments_df = scrape_subreddit(subreddit_name,
                                   limit = 5000)
    
    # Append data to list of dataframes to later join.
    dfs.append(comments_df)
    
    # Pause the script for 10 seconds between subreddits.
    time.sleep(10)


all_data = pd.concat(dfs)
all_data.to_csv('ALL_REDDIT_DATA2.csv')
all_data.to_pickle('ALL_REDDIT_PKL2.pkl')

#%%
#Read pickle file (test)
test = pd.read_pickle('ALL_REDDIT_PKL2.pkl')