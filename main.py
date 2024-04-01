import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pytube import YouTube
from pytube import Search

# Set the path where the downloaded audio files will be saved
SAVE_PATH = ""

# Spotify API credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback"

# Initialize the Spotify client with the necessary OAuth credentials
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope='user-library-read'))


# Function to download audio from a YouTube URL
def download_audio(yt_url, destination='.'):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(yt_url)

        # Extract only audio stream from the video
        video = yt.streams.filter(only_audio=True).first()

        # If a valid audio stream is found
        if video:
            # Download the audio stream to the specified destination
            out_file = video.download(output_path=destination)

            # Convert the file to mp3 format
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

            # Confirm successful download
            print(f"{yt.title} has been successfully downloaded.")
        else:
            # Inform the user if no audio streams were found
            print(f"No audio streams found for {yt.title}.")
    except Exception as e:
        # Handle any exceptions that occur during download
        print(f"An error occurred: {e}")


# Function to retrieve the user's liked tracks from Spotify
def get_liked_tracks():
    liked_tracks = []

    # Request the current user's saved tracks from Spotify
    results = spotify.current_user_saved_tracks()

    # Continue to fetch tracks
    while results:
        liked_tracks.extend(item['track'] for item in results['items'])
        if results['next']:
            results = spotify.next(results)
        else:
            break

    # Return the list of liked tracks
    return liked_tracks


# Main logic to process each liked track
liked_tracks_url = []
tracks = get_liked_tracks()  # Get the first 5 liked tracks from Spotify

# Loop through the liked tracks to get the corresponding YouTube URLs
for current_track in tracks:
    s = Search(current_track['name'] + '-' + current_track['artists'][0]['name'] + "audio")
    v = s.results[0]
    liked_tracks_url.append(v.watch_url)
    print(f"{v.title}\n{v.watch_url}\n")

# Download the audio for each track found on YouTube
for url in liked_tracks_url:
    download_audio(url, SAVE_PATH)
