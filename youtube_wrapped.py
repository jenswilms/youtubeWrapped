# Import libraries

from bs4 import BeautifulSoup

import json
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors

import pandas as pd
import isodate

import urllib.parse

# configure YouTube API
import os
from dotenv import load_dotenv

load_dotenv()

api_service_name = "youtube"
api_version = "v3"
API_KEY = os.getenv('API_KEY')

# Get credentials and create an API client
youtube = build(
    api_service_name, api_version, developerKey=API_KEY)

# data extraction


# create empty DF
df = pd.DataFrame()

# Open YouTube takeout file and convert to BS
with open("/TakeOut/YouTube and YouTube Music/history/watch-history.html") as html:
    soup = BeautifulSoup(html, 'html.parser')

rows = soup.find_all("div", {"class": "outer-cell"})

for row in rows:
    content_data = row.find("div", {"class": "content-cell"})
    date_watched = str(content_data).split("<br/>")[-1][:-6]
    item_data = row.find_all('a')
    if len(item_data) > 0:
        title = item_data[0].get_text()
        link = item_data[0]['href']
        url = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)

        # set default to overwrite
        channel = "NA"
        tags = "NA"
        duration = 0

        if(params):
            # small check so it won't try to make a request for empty data
            youtubeId = params["v"][0]

        if(youtubeId):
            # small check so it won't try to make a request for empty data

            # make youtube API request to get video informatin
            # note that you make a single request for every individual video
            request = youtube.videos().list(
                part="snippet,contentDetails",
                id=youtubeId
            )
            response = request.execute()
            if(len(response['items']) > 0):
                # note: duration is in SECONDS
                duration = isodate.parse_duration(
                    response['items'][0]['contentDetails']['duration']).total_seconds()

                if('tags' in response['items'][0]['snippet']):
                    tags = response['items'][0]['snippet']['tags']

        # add data to DF
        rowJson = [{
            'title': title,
            'link': link,
            'dateWatched': date_watched,
            'channel': channel,
            'tags': tags,
            'duration': duration
        }]
        rowDf = pd.DataFrame(data=rowJson)
        df = pd.concat([df, rowDf])

# you can export your data to a CSV or TSV for manually analysis, or to save some time with the requests later
# df.to_csv("durationAndTags.csv")

# data anlysis

# FROM TAGS TO CATEGORIES

# Check your tags manualy and check which words could classify categories
# Note, that the order is important; as videos can have multiple tags, the last line will always prevail

# Some examples
df.loc[(df.tags.str.contains("meditation"), 'category')] = 'meditation'
df.loc[(df.tags.str.contains("Y Combinator"), 'category')] = 'YC'
df.loc[(df.tags.str.contains("chinese"), 'category')] = 'Chinese'

# FUNCTIONS

# get minutes watched by category


def get_minutes(category):
    allCatVids = df.loc[df['category'] == category]
    totalWatched = str(round(allCatVids['duration'].sum() / 60, 1)) + "min"
    return totalWatched


def get_count(category):
    allCatVids = df.loc[df['category'] == category]
    return str(len(allCatVids)) + " videos"


def get_summary(category):
    return "Of the category " + category + ", you watched " + get_count(category) + ", with a total of " + get_minutes(category) + " watched."

# CLEAN UP DATA SET
# remove duplicates from certain categories
# some categories, you want to only count the "unique videos"


def dropDuplicates(categoryList, dataframe):
    for category in categoryList:
        dataframe.loc[(dataframe.category == category)] = dataframe.loc[(
            dataframe.category == category)].drop_duplicates(subset=['link'])


singleEntryCategories = ['YC', 'Chinese']
dropDuplicates(singleEntryCategories, df)

g = round(df.groupby(['channel'])['duration'].sum() / 60,  1)
j = df.groupby(['channel']).size().to_frame('count')
channelDf = pd.merge(g, j, left_index=True, right_index=True).reset_index(
).sort_values(by=['count'], ascending=False)

wantToKnowCats = ["Chinese", "meditation"]
for cat in wantToKnowCats:
    print(get_summary(cat))
