import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from bs4 import BeautifulSoup

AUTH_TOKEN = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""
USER_ID = ""


my_auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               redirect_uri=REDIRECT_URI,
                               scope="playlist-modify-private",
                               cache_path=".cache",
                               show_dialog=True
                               )


sp = spotipy.Spotify(auth_manager=my_auth_manager)


date = input("What year do you want to listen to? Must be in YYYY-MM-DD format:")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")


song_titles = soup.select(selector="li ul li h3")

song_titles_text = [song.getText(strip=True) for song in song_titles]


song_uris = []
split_year = date.split("-")[0]
for song in song_titles_text:
    results = sp.search(q=f"track:{song} year:{split_year}", type="track")
    # pprint.pprint(results)
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=USER_ID, name=f"{date} Billboard 100 playlist", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


