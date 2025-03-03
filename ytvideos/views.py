import boto3
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import feedparser
import json
from rest_framework.decorators import api_view


# Connect to local DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8080",
    region_name="us-west-2",
    aws_access_key_id="fakeKey",
    aws_secret_access_key="fakeSecret"
)

table = dynamodb.Table("youtube_metadata")


def is_valid_youtube_channel_id(channel_id):
    """
    Basic check for YouTube channel ID validity.
    Not exhaustive but filters out common mistakes.
    """
    if not isinstance(channel_id, str):
        return False
    if not channel_id.startswith("UC"):  # Most channel IDs start with UC
        return False
    if not (24 <= len(channel_id) <= 34):  # Channel id length is generally between 24-34
        return False
    return True


def get_videos_metadata_from_youtube(channel_id):
    """Retrieves recent videos for a channel from the YouTube channels RSS feed."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        feed = feedparser.parse(rss_url)
        videos_metadata = []
        for entry in feed.entries:
            videos_metadata.append({
                "video ID": entry.yt_videoid,
                "title": entry.title,
                "link": entry.link,
                "author": entry.author,
                "published": entry.published,
                "summary": entry.summary,
                "view count": entry.media_statistics["views"]
            })
        return videos_metadata

    except Exception as e:
        print(f"Error fetching from YouTube Channels RSS Feed: {e}")
        return None


def get_videos_metadata_from_db(channel_id):
    """Retrieves video metadata for a channel from the database."""
    try:
        response = table.get_item(Key={"video_id": channel_id})
        if "Item" in response:
            return json.loads(response["Item"]["videos_metadata"])
        else:
            return []
    except Exception as e:
        print(f"Error fetching from DynamoDB: {e}")
        return None


def store_videos_metadata_in_db(channel_id, videos_metadata):
    """Stores video metadata in DynamoDB."""
    try:
        table.put_item(Item={"video_id": channel_id, "videos_metadata": json.dumps(videos_metadata)})
    except Exception as e:
        print(f"Error storing in DynamoDB: {e}")


@api_view(['GET'])
def get_channel_videos_metadata(request, channel_id):
    """
    API endpoint to get recent videos for a YouTube channel.
    """
    if not is_valid_youtube_channel_id(channel_id):
        return HttpResponseBadRequest("Invalid YouTube channel ID.")

    videos_metadata = get_videos_metadata_from_db(channel_id)

    if not videos_metadata:
        print("Videos not found in database. Fetching from YouTube...")
        videos_metadata = get_videos_metadata_from_youtube(channel_id)
        if videos_metadata is None:
            return HttpResponseServerError("Error occurred fetching data from YouTube RSS Feed.")
        if videos_metadata:
            store_videos_metadata_in_db(channel_id, videos_metadata)
        else:
            return JsonResponse({"message": "No videos found for this channel."}, status=404)

    return JsonResponse({"channel_id": channel_id, "videos_metadata": videos_metadata})
