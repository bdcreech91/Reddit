# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:25:04 2022

@author: bdcre
"""
#Reddit scraping with PSAW (pushshift io)
#%%
from pmaw import PushshiftAPI    #library Pushshift
import datetime as dt            #library for date management
import pandas as pd                    #library for data manipulation
#import matplotlib.pyplot as plt  #library for plotting


api = PushshiftAPI()
#start_epoch=int(dt.datetime(2019, 1, 1).timestamp())

#%%
def data_prep_posts(subreddit, start_time, end_time, filters, limit):
    if(len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'domain', 'url',
                   'title', 'num_comments']                 
                   #We set by default some useful columns

    posts = list(api.search_submissions(
        subreddit=subreddit,   #Subreddit we want to audit
        after=start_time,      #Start date
        before=end_time,       #End date
        filter=filters,        #Column names we want to retrieve
        limit=limit))          ##Max number of posts

    return pd.DataFrame(posts) #Return dataframe for analysis


"""FOR COMMENTS"""
def data_prep_comments(term, start_time, end_time, filters, limit):
    if (len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'body', 'permalink', 'subreddit']
                   #We set by default some usefull columns 

    comments = list(api.search_comments(
        q=term,                 #Subreddit we want to audit
        after=start_time,       #Start date
        before=end_time,        #End date
        filter=filters,         #Column names we want to retrieve
        limit=limit))           #Max number of comments
    return pd.DataFrame(comments) #Return dataframe for analysis



def main():
    subreddit = "Darkestdungeon"     #Subreddit we are auditing
    start_time = int(dt.datetime(2021, 1, 1).timestamp())  
                                     #Starting date for our search
    end_time = int(dt.datetime(2021, 1, 31).timestamp())   
                                     #Ending date for our search
    filters = []                     #We don´t want specific filters
    limit = 1000                     #Elelemts we want to recieve
    
    """Here we are going to get subreddits for a brief analysis"""
    #Call function for dataframe creation of comments
    df_p = data_prep_posts(subreddit,start_time,
                         end_time,filters,limit) 
    
    #Drop the column on timestamp format
    df_p['datetime'] = df_p['created_utc'].map(
        lambda t: dt.datetime.fromtimestamp(t))
    df_p = df_p.drop('created_utc', axis=1) 
    #Sort the Row by datetime               
    df_p = df_p.sort_values(by='datetime')  
    #Convert timestamp format to datetime for data analysis               
    df_p["datetime"] = pd.to_datetime(df_p["datetime"])
    """Here we are going to get comments for a brief analysis"""
    term = 'bitcoin'            #Term we want to search for
    limit = 10                  #Number of elelemts 
    df_c = data_prep_comments(term, start_time,
                     end_time, filters, limit)
                                #Call function for dataframe creation of comments
                                
                                
#%%

main()