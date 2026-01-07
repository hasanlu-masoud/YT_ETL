import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
API_KEY =os.getenv("API_KEY")
max_result =50
def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=MrBeast&key={API_KEY}"
        respons = requests.get(url)
       
        respons.raise_for_status()
        data = respons.json()
        #print(json.dumps(data,indent=4))

        channel_items= data["items"][0]
        channel_playlisId=channel_items["contentDetails"]["relatedPlaylists"] ["uploads"]
        print(channel_playlisId)
        return channel_playlisId

    except requests.exceptions.RequestException as e:
       raise e
    


playlistId = get_playlist_id()
def get_video_ids(playlistId):
    videos_ids = []
    pageToken = None
    # آدرس پایه
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_result}&playlistId={playlistId}&key={API_KEY}'

    try:
        while True:
            url = base_url
            if pageToken:
                # اینجا علامت & اضافه شد تا آدرس درست کار کند
                url += f"&pageToken={pageToken}"
            
            respons = requests.get(url)
            respons.raise_for_status()
            data = respons.json()
        
            # اینجا هم s به آخر items اضافه شد
            for item in data.get("items", []):
                video_id = item['contentDetails']['videoId']
                videos_ids.append(video_id)
            
            pageToken = data.get("nextPageToken")
            if not pageToken:
                break

        return videos_ids # اینجا باید لیست رو برگردونی، نه اسم تابع رو!
    except requests.exceptions.RequestException as e:
        raise e



if __name__ == "__main__":
    
   playlistId= get_playlist_id()

   print(get_video_ids(playlistId))