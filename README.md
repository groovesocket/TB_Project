# TubeBuddy code project

## Description:
This is a basic Django REST Framework API that returns metadata for recent videos for any arbitrary YouTube channel. 
This API retrieves video metadata from a Dynamodb database table. 
In the event that no videos for a channel are found, the video metadata is retrieved from a 3rd party, 
free public data source, the YouTube Channels RSS feed, and then stored for later retrieval. 
In no circumstance, excepting invalid channel ids, does the API return no video metadata. This API runs entirely locally.

## Resources:
### 3rd Party Data source: 
I used the YouTube Channels RSS feed as a free, public data source that provides basic metadata that describes recently 
published videos for any channel. I avoided any data source that requires scraping or API keys.
### YouTube channel ids: 
All channels have a unique id provided by YouTube. Example (Mr Beast): UCX6OQ3DkcsbYNE6H8uQQuVA

## Prerequisites:
1. Local Dynamodb instance with table named "videos_metadata" installed on port 8080
2. Python

## To Run:
Open a browser or use curl or Postman to test:
http://127.0.0.1:8000/api/channels/UCX6OQ3DkcsbYNE6H8uQQuVA/videos/ (Example: MrBeast)
http://127.0.0.1:8000/api/channels/invalid-channel-id/videos/ (For testing the validation)
Note the channel ID needs to start with UC to be considered valid.