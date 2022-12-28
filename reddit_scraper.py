
#Reference: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

import praw
# # from praw.models import Reddit
from praw.models import MoreComments
from praw.models import Submission
from praw.models import Subreddit

import pandas as pd
import time

# import asyncpraw
# from asyncpraw.models import MoreComments
# from asyncpraw.models import Submission
# from asyncpraw.models import Subreddit

# reddit_read_only = praw.Reddit(client_id="4MgxPl_trktjfzL0s0Q-pQ",         # your client id
#                                client_secret="zt__lqVHeA-6l821H_oSENG4nGIN8g",      # your client secret
#                                user_agent="Automatic-Sky656")        # your user agent
 
#Authorized instance
reddit = praw.Reddit(client_id="4MgxPl_trktjfzL0s0Q-pQ",         # your client id
                                client_secret="zt__lqVHeA-6l821H_oSENG4nGIN8g",      # your client secret
                                user_agent="Automatic-Sky656_test_scrape",        # your user agent
                                username="Automatic-Sky656",        # your reddit username
                                password="-HZR6GchuidQC5a")  


# reddit = asyncpraw.Reddit(client_id="4MgxPl_trktjfzL0s0Q-pQ",         # your client id
#                                 client_secret="zt__lqVHeA-6l821H_oSENG4nGIN8g",      # your client secret
#                                 user_agent="Automatic-Sky656_test_scrape",        # your user agent
#                                 username="Automatic-Sky656",        # your reddit username
#                                 password="-HZR6GchuidQC5a")  

#%%
# if not post.author:
#     name = '[deleted]'
# else:
#     name = post.author.name

# if isinstance(top_level_comment, MoreComments):
#     continue

def scrape_subreddit(subreddit_name, limit):
    subreddit = reddit.subreddit(subreddit_name)
    #comments = subreddit.comments(limit=100)#None
    submissions = subreddit.hot(limit = limit)
    comment_data = []
    #for submission in subreddit.async_hot(limit=10) : #.hot
    for submission in submissions:
        submission_title = submission.title
        submission_body = submission.selftext
        if submission_body is None:
            submission_body = 'None'
        print(submission_title)
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
                    comment_dict = {
                        'subreddit': subreddit_name,
                        'submission_title': submission_title,
                        'submission_text': submission_body,
                        'username': comment.author.name,
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
                        comment_dict['replies'].append({
                            'username': reply.author.name,
                            'comment': reply.body,
                            'id': reply.id,
                        })           
            comment_data.append(comment_dict)
    return pd.DataFrame(comment_data)


#%%
subreddit_names = ['schizophrenia','bipolar','debt','GamblingAddiction', 'SuicideWatch', 'depression', 'depressed', 'Psychosis', 'antiwork',
               'MensRights', 'conspiracy', 'conspiracytheories', 'Bankruptcy', 'Firearms']

dfs = []
#print(dfs[0])
for subreddit_name in subreddit_names:
    comments_df = scrape_subreddit(subreddit_name,
                                   limit = 500)
    # Save the comments to a CSV file
    #comments_df.to_csv(f'{subreddit_name}_comments.csv', index=False)
    dfs.append(comments_df)
    # Pause the script for 10 seconds
    time.sleep(10)


all_data = pd.concat(dfs)


#%%




# Alternate or async here
async def scrape_comments(subreddit):
    comments = []
    subreddit = await reddit.async_subreddit(subreddit)
    submissions = await subreddit.async_hot(limit=100)
    for submission in submissions:
        submission_title = submission.title
        submission_url = submission.url
        submission_comments = await submission.async_comments()
        for comment in submission_comments:
            #ETC


#%%
# for top_level_comment in submission.comments:

# if isinstance(top_level_comment, MoreComments:)

# continue

# def scrape_comments(subreddit):
#     comments = []
#     subreddit = reddit.subreddit(subreddit)
#     for submission in subreddit.hot(limit=100):
#         submission_title = submission.title
#         submission_url = submission.url
#         for comment in submission.comments:
#             if not comment.author:
#                 comments.append({
#                     'submission_title': submission_title,
#                     'submission_url': submission_url,
#                     'username': '[deleted]', #
#                     'body': comment.body,
#                     'replies': [{'username': reply.author.name, 'body': reply.body} for reply in comment.replies]
#                 })
#             else:
#                 comments.append({
#                     'submission_title': submission_title,
#                     'submission_url': submission_url,
#                     'username': comment.author.name, #
#                     'body': comment.body,
#                     'replies': [{'username': reply.author.name, 'body': reply.body} for reply in comment.replies]
#                 })
#     return comments


# a = scrape_comments('depression')