import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
spotify_username = os.environ.get("SPOTIFY_USERNAME")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")
spotify_scope = "playlist-modify-public"

date = input("Which date do you want to travel to?(YYYY-MM-DD) ")

#Authentication

token = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                     client_secret=SPOTIPY_CLIENT_SECRET,
                     redirect_uri=SPOTIPY_REDIRECT_URI,
                     state=None,
                     scope=spotify_scope,
                     username=spotify_username)

spotifyObject = spotipy.Spotify(auth_manager=token)

# Creating the playlist

spotifyObject.user_playlist_create(user=spotify_username, name=f"{date} Playlist", public=True, collaborative=False, description='Automated playlist creator using python.')
allplaylists = spotifyObject.user_playlists(user=spotify_username)
new_playlist_id = allplaylists["items"][0]["id"]


# Searching for the top 100 songs in date

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select("li #title-of-a-story")
singer = soup.find_all(name="span", class_="a-no-trucate")

errors = []
spotify_tracks = []
for n in range(0, len(songs)):
    songs[n] = f"{songs[n].getText().strip()} {singer[n].getText().strip()}"
    result = spotifyObject.search(q=songs[n])
    try:
        spotify_tracks.append(result["tracks"]["items"][0]["uri"])
    except:
        errors.append(f"{songs[n]}, position: {n+1}.")

# Adding the 100 musics to the playlist

spotifyObject.playlist_add_items(playlist_id=new_playlist_id, items=spotify_tracks)

if errors != []:
    print(f"Couldn't find the following tracks: {errors}")
