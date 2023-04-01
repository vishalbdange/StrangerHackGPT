# import OS for environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# import requests
import requests

def youtube(query_text):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    search_params = {
        'key' : os.environ['YOUTUBE_API_KEY'],
        'q' : query_text,
        'part' : 'snippet',
        'maxResults' : 3,
        'type' : 'video'
    }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])


    video_params = {
        'key' : os.environ['YOUTUBE_API_KEY'],
        'id' : ','.join(video_ids),
        'part' : 'snippet,contentDetails',
        'maxResults' : 4
    }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']
 
    for result in results:
        video_data = {
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'duration' : 0,
            'title' : result['snippet']['title'],
        }
        videos.append(video_data)
        
    # print(videos)
    return videos