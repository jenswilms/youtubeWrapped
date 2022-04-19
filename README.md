# YouTube Wrapped
Python scripped for analyzing youtube data

### Some caution
Unfortunately, YouTube does not let you know how long you have watched a video. This is causing a major bias in the data. How it works in this analysis is that you check the videos you watched, get the amount of duration of that video from the YouTube API, and then store it. Now, let's say you have been searching for a lecture to watch: maybe you checked out 5 lectures of 3 hours each, and only watched 2 minutes from the first 4, and 30 minutes from the last. The analysis will say you watched 15 hours of lectures, while in reality it is less then an hour. One check would be to compare the duration of a video with 'dateWatched' and especially with 'dateWatched' of the next video.

### How to use
1. Get your data from Google Takeout. https://takeout.google.com/settings/takeout
2. Get a YouTube API key: https://blog.hubspot.com/website/how-to-get-youtube-api-key
3. Add Google Takeout data and API key to the script
4. Set desired categories
5. Enjoy your YoutubeWrapped


### Other notes
Right now, there is just a section where you transform the YouTube tags into categories, so you can only see the "Wrapped" of the desired videos... no need to see the amount of nonsense videos we watched...

Also, right now it is only a YouTube Wrapped for ALL years; dateWatched is included, so making use of "datetime" you could easily created a Wrapped per year.

Final note, this scripts create a single request for every individual video on the YouTube API. It seems unlikely that one can watch so many videos that it will exceed the YouTube API limit. However, YouTube allows up to 50 video_ids in 1 request. 





