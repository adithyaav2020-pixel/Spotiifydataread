import base64
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials =base64.b64encode(credentials.encode()).decode()
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={'Authorization': f"Basic {encoded_credentials}"},
            data={'grant_type': 'client_credentials'}
        )
        # print(response.json())
        # print(response.json()['access_token'])

        # print("Token generated successfully...")
        return response.json()['access_token']
    except Exception as e:
        print("Error in Token Generation..",e)  

# print(access_token())


# # latest release in spotify

def get_new_release():
    try:
        token = access_token()
        header = {'Authorization': f'Bearer {token}'}
        Param = {'limit':50}
        response = requests.get('https://api.spotify.com/v1/browse/new-releases',headers=header,params=Param)

        if response.status_code == 200:
            # print(response.json())
            data = response.json()
            albums = data['albums']['items']
            for album in albums:
                # print(album)
                info = {
                    'album_name': album['name'],
                    'artist_name' : album['artists'][0]['name'],
                    'release_date' : album['release_date'],
                    'album_type' : album['album_type'],
                    'total_tracks' : album['total_tracks'],
                    'spotify_url' : album['external_urls']['spotify'],
                    'album_image' : album['images'][0]['url'] if album['images'] else None 
                }
                print(json.dumps(info,indent=2))
                print("*" * 30)          
    except Exception as e:
        print("Error in latest relesed data fetching..",e)
#     print(response)
#     print(response.json())

get_new_release()       