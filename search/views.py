import requests
from django.shortcuts import render
from search.config import config


def index(request):
    videos = []

    if request.method == 'POST' and request.POST['search']:
        url = 'https://www.googleapis.com/youtube/v3/search'

        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        print(config["key"])
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'type': 'video',
            'key': config["key"],

        }

        r = requests.get(url, params=search_params)
    
        videoID = []
        results = r.json()['items']

        for result in results:
            videoID.append(result['id']['videoId'])

        video_params = {
            'key': config["key"],
            'part': 'snippet,contentDetails',
            'id': ','.join(videoID),
        }
        r = requests.get(video_url, params=video_params)
     
        results = r.json()['items']
        
        for result in results:
            videoDATA = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnails': result['snippet']['thumbnails']['high']['url']
            }
            videos.append(videoDATA)

    context = {
        'videos': videos
    }

    return render(request, 'search/index.html', context)
