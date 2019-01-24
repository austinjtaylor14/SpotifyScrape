"""

@author: Austin Taylor
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tpb
from tpb import CATEGORIES, ORDERS

USERNAME = 'austinjtaylor14'
CLIENT_ID = 'f81e60fa2e3f4fd28c9ff883090fc2b3'
CLIENT_SECRET = 'a58fe19450ef4d52b1ce08ac22117567'
MP3_PATH = '/Users/austin1taylor/Music/mp3s/'

public_playlists = ['Electro-Boogie / Sunrise', 'Depth', 'Distant Lands', 'Noir', 'Dirty Bird', 'Too Deep',
                     'Neo Tokyo', 'After Hours']
collab_playlists = {'Depth': '4tpgj1mUBSMEHKSHQKeSy0', 'After Hours': '3F4UjXLGnyxDXtc9l4xUur'}


def scrape_spotify_playlist(id):
    """
    Scrapes Spotify for a list of tracks from a playlist, based on the playlist's id
    """
    results = sp.user_playlist_tracks(user=USERNAME, playlist_id=id, fields='items,uri,name,id,total')
    results_items = results['items']

    track_list = [(track['track']['artists'][0]['name'] + ' ' +
                   track['track']['name']) for track in results_items]

    return track_list


def pirate_bay_search(search_str):
    """
    Function to search ThePirateBay for a string
    """
    tpb_conn = tpb.TPB('https://thepiratebay.org') # Create a TPB object
    search = tpb_conn.search(search_str, category=CATEGORIES.AUDIO)

    return search[0]


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

    print(full_dict)

    # Check to see if the track has an mp3. If not, search ThePirateBay, download, and copy into folder
    for name, track_list in full_dict.items():
        curr_path = MP3_PATH + name.replace('/ ', '') + '/'
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

        for track in track_list:
            if not os.path.isfile(curr_path + track + '.mp3'):  # TODO: Use regex or fuzzywuzzy
                pass
                # TODO: Figure out ThePirateBay API


if __name__ == '__main__':
    # Spotify authorization
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    main()
