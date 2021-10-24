import spotipy
import os
from dotenv import load_dotenv
import re
import asyncio
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_URL_REG = re.compile(r'https?://open.spotify.com/(?P<type>album|playlist|track)/(?P<id>[a-zA-Z0-9]+)')

load_dotenv()
spsecret = os.getenv('SPOTIFY_SECRET')

spcreds = SpotifyClientCredentials(client_id='b0be3e4ae85a41d5baaaf5fb786d88f1', client_secret=spsecret)
sp = spotipy.Spotify(client_credentials_manager=spcreds)

def get_spotify_tracks(url):
    spoturl_check = SPOTIFY_URL_REG.match(url)
    search_type = spoturl_check.group('type')
    spotify_id = spoturl_check.group('id')
    
    if search_type == 'playlist':
        results = sp.playlist_tracks(playlist_id=spotify_id)['items']
        tracks = []
        for x in results:
            tracks.append(x['track'])
        return tracks
    if search_type == 'album':
        results = sp.album_tracks(album_id=spotify_id)['items']
        tracks = []
        for x in results:
            tracks.append(x['track'])
        return tracks
    if search_type == 'track':
        results = sp.track(track_id=spotify_id)
        results = [results]
        return results

