import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import getenv
import pandas as pd

# User gives an spotify URL of one song


spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        getenv('CLIENT_ID'), 
        getenv('CLIENT_SECRET')
        )
    )

def input_track_uri(input_string):
    '''Takes a string performs a song search
    on Spotify API and returns the uri of that song'''
    song_uri = spotify.search(input_string, limit=1)['tracks']['items'][0]['uri']
    return song_uri

def get_30_tracks(input_track_uri):
    '''Pull the information of 30 songs from Spotify API
    # User-Imput-artist Top 10
    # 1 song from 10 related artists
    # 10 Spotify suggestions base on input song genre and artist '''

    # Get track info from API with uri                                                                           
    track_info = spotify.track(input_track_uri)

    # Get artist URI from track info
    artist_uri = track_info['artists'][0]['uri']

    # Get artist info from API with artist URI
    artist_info = spotify.artist(artist_uri)

    # Get artist genres list from artist info and taking one
    genre = artist_info.get('genres')[0]
    

    #   PULLING SONGS FROM API

    # Getting the User-Imput-artist Top 10 Tracks
    input_artist_top_10 = spotify.artist_top_tracks(artist_info.get('id'))['tracks']

    # Getting 1 song from 10 related artists
    related_artists = spotify.artist_related_artists(artist_info.get('id'))

    related_artists_ids = []
    for artist in related_artists['artists']:
        id = artist.get('id')
        related_artists_ids.append(id)

    related_artists_10 = []
    for id in related_artists_ids[:10]:
        track = spotify.artist_top_tracks(id)['tracks'][0]
        related_artists_10.append(track)

    # Selecting 10 from Spotify suggestions base on input song genre and artist
    suggested_list = spotify.recommendations([artist_uri], [genre])
    spotify_suggested_10 = suggested_list['tracks'][:10]

    # Joining the lists of 10 songs
    gathered_30 = input_artist_top_10 + related_artists_10 + spotify_suggested_10

    return gathered_30


def analize_tracks(gathered_tracks):
    '''Takes a list of tracks and all their general information
    and pull the audio feature analisis for each track from the Spotify API'''

    # Extracting and making a list with tracks IDs
    all_tracks_ids = []
    for track in gathered_tracks:
        all_tracks_ids.append(track['id'])

    # Pulling audio features analisis for each track
    gathered_30_analisis = spotify.audio_features(all_tracks_ids)
    
    return gathered_30_analisis


def get_all_data(input_string):
    '''Takes an user input string search for a matching song
    in the Spotify API and return a dictionary with
    gathered information about 30 posible suggestions
    to play next base on that song's info'''

    # Search starting point
    input_song_uri = input_track_uri(input_string)

    # Gathered information from search
    gathered_30 = get_30_tracks(input_song_uri)
    gathered_30_analisis = analize_tracks(gathered_30)

    # Creating dfs (Preparing to Merge gathered information)
    general_data = pd.DataFrame(
        gathered_30,
        columns=['id','uri', 'artists','album','name','popularity']
        )

    features_data = pd.DataFrame(
        gathered_30_analisis,
        columns=['id','danceability', 'energy', 'key', 'loudness',
                'mode', 'speechiness', 'acousticness','instrumentalness',
                'liveness', 'valence', 'tempo', 'duration_ms']
                )

    final_df = pd.merge(general_data, features_data, on='id')


    # CLEANING STRINGS FROM UNWANTED CHARACTERS

    #   Strip unwanted characters in name column strings
    # remove parenthesis and all inside them
    final_df['name'] = final_df['name'].str.replace(r" \(.*\)","")
    # splits strings using "-" and takes first half
    clean_names = []
    for name in final_df['name']:
        clean_name = name.split("-", 1)[0]
        clean_names.append(clean_name)

    final_df['name'] = clean_names

    #  REPLACING DICTIONARIES WITH NAMES

    # Artists column
    artists_names = []
    for track in gathered_30:
        artists_names.append(track['artists'][0]['name'])
    final_df['artists'] = artists_names

    # Album Column
    albums_names = []
    for track in gathered_30:
        albums_names.append(track['album']['name'])
    final_df['album'] = albums_names


    return dict(final_df)



