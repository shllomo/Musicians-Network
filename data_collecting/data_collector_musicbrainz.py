import json
import pandas as pd

import utils

def extract_artist_from_country(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='UTF-8') as file:
        with open(output_file_path, 'w') as output_file:
            for line in file:
                try:
                    artist = json.loads(line.strip())
                    country = artist.get('area', {}).get('name') if artist.get('area') else 'Unknown'
                    if country in utils.countries_of_interest:    
                        json.dump(artist, output_file, ensure_ascii=False)
                        output_file.write('\n')
                        
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")



def extract_artist_with_genre(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='UTF-8') as file:
        with open(output_file_path, 'w') as output_file:
            for line in file:
                try:
                    artist = json.loads(line.strip())
                   
                    genres =  [genre['name'] for genre in artist.get('genres', []) if 'name' in genre]

                    if len(genres) >= 1 :    
                        json.dump(artist, output_file, ensure_ascii=False)
                        output_file.write('\n')
                        
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            


def process_artists(file_path):
    processed_data = []
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file:
            try:
                artist = json.loads(line.strip())
                country = artist.get('area', {}).get('name') if artist.get('area') else 'Unknown'
                aliases = [alias['name'] for alias in artist.get('aliases', []) if 'name' in alias]
                sort_name = artist.get('sort-name', '')
                if sort_name:
                    aliases.append(sort_name)

                # Ensure no duplicate names and sort them
                aliases = sorted(set(aliases))

                processed_data.append({
                    "name": artist.get('name', 'Unknown'),
                     "type": artist.get('type', 'Unknown'),
                    "active_years": f"{artist.get('life-span', {}).get('begin', 'N/A')} - {artist.get('life-span', {}).get('end', 'N/A')}",
                    "genres": [genre['name'] for genre in artist.get('genres', []) if 'name' in genre],
                    "country": country,
                    "aliases": aliases,
                })
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return processed_data
# extract_artist_from_country(utils.original_data, utils.artist_from_selected_countries)
# extract_artist_with_genre(utils.artist_from_selected_countries, utils.artist_with_genres)


# artist_data = process_artists(utils.artist_with_genres)
# artist_data =  pd.DataFrame(artist_data)
# artist_data.to_csv(utils.artist_data_csv, index=True)


