import requests
from dotenv import load_dotenv
import os
load_dotenv() 

class Spotify: 
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        # self.getAPItoken()    
        self.playlist_id = os.getenv('PLAYLIST_ID')
        self.access_token = os.getenv("TEMP_TOKEN")
        self.tracks = []
        self.info = {}
        self.getPlaylist()
        self.getPlaylistInfo()
        print(self.info)
        # [print(i) for i in self.tracks]
        
        
    def getAPItoken(self):
        url = "https://accounts.spotify.com/api/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials", 
            "client_id": self.client_id, 
            "client_secret": self.client_secret
        }
        result = requests.post(url, headers=header, data=data)
        if result.status_code != 200:
            print(f"Error {result.status_code}: {result.json()}")
            raise InterruptedError
        self.access_token = result.json().get('access_token')
        print(self.access_token)
        

    def getPlaylist(self): 
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        params = {
            "market": "CA", 
            "fields": "items(added_by.id,track(name,id,artists(name)))", 
            "limit": 50 
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        result = requests.get(url, headers=headers, params=params)
        if result.status_code != 200:
            print(f"Error {result.status_code}: {result.json()}")
            raise InterruptedError
        
        result = result.json()
        for item in result.get("items", []):
            track = item.get("track", {})
            track_name = track.get("name", "Unknown Track")
            track_id = track.get("id", "No ID")
            artists = [artist.get("name", "Unknown Artist") for artist in track.get("artists", [])]
            new_track = Track(track_name, track_id, artists)
            self.tracks.append(new_track)
            # print(f"Track: {track_name} | ID: {track_id} | Artists: {', '.join(artists)}")
        
        
    def getPlaylistInfo(self): 
        url = f'https://api.spotify.com/v1/playlists/{self.playlist_id}'
        params = {
            'market': 'CA',
            'fields': 'name,owner(id,display_name)'  # Specify the fields to be fetched
        }
        headers = {
            'Authorization': f'Bearer {self.access_token}'  # Add Bearer token for authorization
        }
        
        result = requests.get(url, headers=headers, params=params)
        if result.status_code != 200:
            print(f"Error {result.status_code}: {result.json()}")
            raise InterruptedError
        
        result = result.json()
        self.info['owner_name'] = result.get('owner', '').get('display_name', 'Unknown')
        self.info['owner_id'] = result.get('owner', '').get('id', "Unknown")
        self.info['track_name'] = result.get('name', 'Unknown')
        
        
class Track: 
    def __init__(self, name: str, id: str, artists: list[str]):
        self.name = name 
        self.id = id, 
        self.artists = artists
    
    def __str__(self):
        return f"{self.name}"
        
test = Spotify()
"""
get playlist name 
for each item in playlist -> get name artists id 

logging into yt music without triggering authentication everytime 
create/edit a playlist
add each track to playlist
"""