import pandas as pd 
import json
import boto3
from datetime import datetime
from io import StringIO ## we are importing this because we need to store in csv format, i.e. we need to convert entire json format to string file


def album(data):
    album_list=[]
    for row in data['items']:
        album_id=row['track']['album']['id']
        album_name=row['track']['album']['name']
        album_ext_url=row['track']['album']['external_urls']['spotify']
        album_rel_date=row['track']['album']['release_date']
        album_tol_tracks=row['track']['album']['total_tracks']
        album_element={'album_id':album_id,'album_name':album_name,'album_ext_url':album_ext_url,
                       'album_rel_date':album_rel_date,'album_tol_tracks':album_tol_tracks}
        album_list.append(album_element)
    return(album_list)

def artist(data):
    artist_list=[]
    for row in data['items']:
        for key, value in row.items(): ##we are interating through dictionary
            if key == 'track':
                for artist in value['artists']:
                    artist_element= {'artist_id':artist['id'] , 'artist_name':artist['name'] , 'artist_ext_uri':artist['href']}
                    artist_list.append(artist_element)  
    return(artist_list)

def song(data):
    song_list=[]
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration_ms = row['track']['duration_ms']
        song_popularity = row['track']['popularity']
        song_url = row['track']['external_urls']['spotify']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        song_elements = {'song_id' : song_id, 'song_name' : song_name, 'song_duration_ms': song_duration_ms, 'song_popularity' : song_popularity ,
                        'song_url' : song_url , 'song_added' : song_added , 'album_id' : album_id , 'album_name' : album_name }
        song_list.append(song_elements)
    return(song_list)
    
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    Bucket = "spotify-etl-project-nirakar"
    Key = "raw_data/to_processed/"
    
    spotify_data=[]
    spotify_key=[]
    
    for file in (s3.list_objects(Bucket=Bucket,Prefix=Key)['Contents']):
        file_key = file['Key']
        #print(file_key.split('.')[-1])
        if file_key.split('.')[-1] == "json":
            print(file_key)
            response = s3.get_object(Bucket = Bucket, Key = file_key)
            content=response['Body']
            jsonObject=json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_key.append(file_key)
            
    for data in spotify_data:
        album_list=album(data)
        artist_list=artist(data)
        song_list=song(data)
        
        #print(album_list)
        
        album_df = pd.DataFrame.from_dict(album_list)
        album_df = album_df.drop_duplicates(subset=['album_id'])
        
        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])
        
        song_df = pd.DataFrame.from_dict(song_list)
        
        album_df['album_rel_date'] = pd.to_datetime(album_df['album_rel_date'])
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])
        
        song_key = "transformed_data/songs_data/song_transformed_data" + str(datetime.now()) + ".csv"
        
        #we have to follow below steps to store in string format.
        
        song_buffer=StringIO() #we are creating object here
        song_df.to_csv(song_buffer, index=False) #then we are passing this StingIO to csv function. We are writing data available in song_df to the song_buffer
        song_content = song_buffer.getvalue() #then we get value out of it.
        
        s3.put_object(Bucket=Bucket, Key=song_key, Body=song_content)
        
        ##Album Data Frame
        album_key = "transformed_data/album_data/album_transformed_data" + str(datetime.now()) + ".csv"
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
        
        ##Artist Data Frame
        artist_key = "transformed_data/artist_data/artist_transformed_data" + str(datetime.now()) + ".csv"
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)
    
    #Basically we are copying the data from to_processed to processed folder, and then we are deleting the to_processed folder.
    
    s3_resource = boto3.resource('s3')
    for key in spotify_key:
        copy_src = {
            'Bucket' : Bucket,
            'Key' : key
        }
        s3_resource.meta.client.copy(copy_src, Bucket, "raw_data/processed/" + key.split("/")[-1])
        s3_resource.Object(Bucket, key).delete()
        
