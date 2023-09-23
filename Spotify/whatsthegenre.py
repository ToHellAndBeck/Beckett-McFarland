import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Set your Spotify API credentials here
SPOTIPY_CLIENT_ID = 'e8b0dc1e11a04a3ba55dfb30b42402cd'
SPOTIPY_CLIENT_SECRET = '2145bd4265484590bdd01ce7b195f454'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Initialize the Spotify API client with the specified credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read"))

def fetch_liked_songs(start_offset=0, limit=50):
    """
    Fetch the liked songs from Spotify.

    Args:
        start_offset (int): The starting offset for fetching liked songs.
        limit (int): The maximum number of songs to fetch in each request.

    Returns:
        list: List of liked songs.
        int: The updated offset for the next fetch.
    """
    print("Fetching liked songs...")
    results = []
    offset = start_offset
    
    while offset < 2000:  # Stop when 1000 songs are fetched
        tracks = sp.current_user_saved_tracks(limit=min(limit, 2000 - offset), offset=offset)
        if not tracks['items']:
            break
        results.extend(tracks['items'])
        offset += limit
    
    print(f"Total liked songs fetched: {len(results)}")
    return results, offset

def get_track_genres(track_id):
    """
    Get the genre tags attached to a track.

    Args:
        track_id (str): The Spotify track ID.

    Returns:
        list: List of genres for the track.
    """
    try:
        track = sp.track(track_id)
        if 'artists' in track and len(track['artists']) > 0 and 'genres' in track['artists'][0]:
            return track['artists'][0]['genres']
        else:
            return ["Genre information not available"]
    except spotipy.SpotifyException as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    # Check if there's a saved progress file and load the last processed offset
    progress_file = 'progress.json'
    start_offset = 0

    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            progress_data = json.load(file)
            start_offset = progress_data.get('last_processed_offset', 0)

    # Get the first 1000 of the user's liked songs starting from the last processed offset
    liked_songs, start_offset = fetch_liked_songs(start_offset)

    if not liked_songs:
        print("No liked songs found.")
    else:
        print("Collecting genre information for liked songs...")

        # Create a list to store the results
        results = []

        # Iterate through the liked songs and collect their information
        for index, item in enumerate(liked_songs, start=1):
            track = item['track']
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            genres = get_track_genres(track_id)
            
            # Retrieve additional information for the track
            result = sp.search(track_name)
            if result is None or not result['tracks']['items']:
                print(f"No information found for track: {track_name}")
                continue

            track_info = result['tracks']['items'][0]

            # Retrieve artist information
            artist = sp.artist(track_info["artists"][0]["external_urls"]["spotify"])
            if artist is None:
                print(f"No artist information found for track: {track_name}")
                continue

            artist_genres = artist["genres"]

            results.append({
                'Track Name': track_name,
                'Artist Name': artist_name,
                'Track Genres': ', '.join(genres),
                'Artist Genres': ', '.join(artist_genres)
            })

            print(f"Processed {index}/{len(liked_songs)} liked songs")

        # Create a DataFrame from the results
        df = pd.DataFrame(results)

        # Save the DataFrame to an Excel spreadsheet
        df.to_excel('Genres.xlsx', index=False)
        
        print("Results saved to Genres.xlsx")
