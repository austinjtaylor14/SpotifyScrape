"""

@author: Austin Taylor
"""

import os
from spotdl import downloader
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import tpb
# from tpb import CATEGORIES, ORDERS

USERNAME = 'austinjtaylor14'
CLIENT_ID = 'f81e60fa2e3f4fd28c9ff883090fc2b3'
with open('C:/Users/austi/Desktop/spotify_secret.txt', 'r') as f:
    CLIENT_SECRET = f.read()

if os.name == 'nt':
    MP3_PATH = 'C:/Users/austi/Music/Playlists/'
else:
    MP3_PATH = '/Users/austin1taylor/Music/Playlists/'

public_playlists = ['Electro-Boogie / Sunrise', 'Depth', 'Distant Lands', 'Noir', 'Dirty Bird', 'Too Deep',
                     'Neo Tokyo', 'After Hours']
collab_playlists = {'Depth': '4tpgj1mUBSMEHKSHQKeSy0', 'After Hours': '3F4UjXLGnyxDXtc9l4xUur'}


def scrape_spotify_playlist(id):
    """
    Scrapes Spotify for a list of tracks from a playlist, based on the playlist's id
    """
    results = sp.user_playlist_tracks(user=USERNAME, playlist_id=id, fields='items,uri,name,id,total')
    results_items = results['items']

    track_list = [[(track['track']['artists'][0]['name'] + ' - ' +
                   track['track']['name']), track['track']['id']] for track in results_items]

    return track_list


def main():
    # Create a dict of {name: id} for every playlist that's in public_playlists
    playlist_results = sp.user_playlists(USERNAME)
    playlist_results_items = playlist_results['items']
    playlist_dict = {pl['name']: pl['id'] for pl in playlist_results_items if pl['name'] in public_playlists}
    playlist_dict.update(collab_playlists)

    # Created a dict of {name: track_list} called full_dict
    full_dict = {}
    for name, id in playlist_dict.items():
        track_list = scrape_spotify_playlist(id)
        full_dict.update({name: track_list})

    for name, track_list in full_dict.items():
        curr_path = MP3_PATH + name.replace('/ ', '').replace(' ', '_') + '/'
        if not os.path.isdir(curr_path):
            os.makedirs(curr_path)

        for track in track_list:
            print('\n\nDownloading:', track[0], '\n')
            string = 'spotdl --song https://open.spotify.com/track/{0} --folder {1} --manual --overwrite skip --search-format "{2}"'.format(track[1], curr_path, track[0])
            print(string)
            os.system(string)


if __name__ == '__main__':
    # Spotify authorization
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    main()