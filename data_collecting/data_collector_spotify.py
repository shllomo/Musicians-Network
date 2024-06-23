import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import utils
import json
import pandas as pd
import logging

client_credentials_manager = SpotifyClientCredentials(client_id=utils.client_id_shlomo, client_secret=utils.client_secret_shlomo)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_data(artist_name, aliases):
    try:
        results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
        if results['artists']['items']:
            artist = results['artists']['items'][0]
          
            if artist['name'].lower() == artist_name.lower() or artist['name'].lower() in (alias.lower() for alias in aliases):
                return {
                    "spotify_id": artist['id'],
                    "popularity": artist['popularity'],
                    "followers": artist['followers']['total'],
                    "genres": ', '.join(artist['genres'])
                }
            
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        if e.http_status == 429:
            retry_after = 10
            try: 
                retry_after = int(e.headers['Retry-After'])
            except: 
                retry_after = 10
                pass    

            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return get_artist_data(artist_name, aliases)  # Recursive call after waiting
        
    except Exception as e:
        print(f"An error occurred: {e}")
       


def update_artists_csv(input_file, output_file, start_raw):
    df = pd.read_csv(input_file, encoding='utf-8')
    df = df[start_raw:]
    df['spotify_id'] = None
    df['popularity'] = None
    df['total_followers'] = None
    df['spotify_genres'] = None

    try:
        for index, row in df.iterrows():
                print(index)
                artist_data = get_artist_data(row['name'], row['aliases'])
                df.at[index, 'spotify_id'] = artist_data['spotify_id']
                df.at[index, 'popularity'] = artist_data['popularity']
                df.at[index, 'total_followers'] = artist_data['followers']
                df.at[index, 'spotify_genres'] = artist_data['genres']
                time.sleep(0.2) 

    except KeyboardInterrupt:
        df.to_csv(interrupt_save_path = f'interrupted_{output_file}', index=False)
        raise
    
    except:
        df.to_csv(f'execp_{output_file}', index=False)
    
    df.to_csv(output_file, index=False)

start_raw = 19676
update_artists_csv(utils.artist_data_csv, utils.artist_extended_data_csv, start_raw)
#update_artists_csv(utils.artist_data_sample_csv, utils.artist_extended_data_sample_csv)