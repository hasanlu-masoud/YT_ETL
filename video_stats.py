import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
API_KEY =os.getenv("API_KEY")
def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=MrBeast&key={API_KEY}"
        respons = requests.get(url)
        print(respons)
        data = respons.json()
        #print(json.dumps(data,indent=4))

        channel_items= data["items"][0]
        channel_playlisId=channel_items["contentDetails"]["relatedPlaylists"] ["uploads"]
        print(channel_playlisId)
        return channel_playlisId

    except requests.exceptions.RequestException as e:
       raise e
    



if __name__ == "__main__":
    
    get_playlist_id()
