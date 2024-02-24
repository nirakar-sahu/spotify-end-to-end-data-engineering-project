import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 #package created in AWS in order to programatically connect to S3 services
from datetime import datetime

def lambda_handler(event, context):
    Client_Id = os.environ.get('client_id')
    Client_Secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=Client_Id,client_secret=Client_Secret) #This basically used for authentication
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)#This basically used for authorisation
    playlist = sp.user_playlists('spotify')
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg"
    playlist_url= playlist_link.split("/")[-1]
    
    spotify_data = sp.playlist_tracks(playlist_url)
    
    #now wewant to dump data into S3 in json format.
    client = boto3.client('s3')
    
    filename = "spotify_raw" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket="spotify-etl-project-nirakar",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data) #dumping data converting to json format
        )
