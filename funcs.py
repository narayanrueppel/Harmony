from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json 
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


#Returns access token for API requests
def get_token():
    auth_string = client_id+":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type":"client_credentials"}
    result = post(url,headers = headers,data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


#Returns Authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer "+token}


#Returns results for an artist search
def artist_search(token,artist_name):
    #Loads request url and obtains result from API
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)

    #Returns json, or prints message if no json can be found
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result

#Returns results for a track search
def track_search(token,track_name):
    #Loads request url and obtains result from API
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)

    #Returns json, or prints message if no json can be found
    json_result = json.loads(result.content)["tracks"]
    if len(json_result) == 0:
        print("No playlist with this name exists...")
        return None
    return json_result

#Returns results for a playlist search
def playlist_search(token,playlist_name):
    #Loads request url and obtains result from API
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={playlist_name}&type=playlist&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)

    #Returns json, or prints message if no json can be found
    json_result = json.loads(result.content)["playlists"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result

#Returns TrackID given API result
def track_id(track_result):
    return track_result["items"][0]["id"]

#Returns Artist ID given API result
def artist_id(artist_result):
    return artist_result[0]["id"]


#Returns Playlist ID given API result
def playlist_id(playlist_result):
    return playlist_result["items"][0]["id"]


#Returns all information associated with a spotify track
def track_info(token,track_name):
    #Loads request url and obtains result from API
    track = track_search(token,track_name)
    id = track_id(track)
    query_url = f"https://api.spotify.com/v1/audio-features/{id}"

    headers = get_auth_header(token)
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)
    return json_result

#Returns all information associated with a spotify playlist
def playlist_info(token,playlist_name):
    #Loads request url and obtains result from API
    playlist = playlist_search(token,playlist_name)
    id = playlist_id(playlist)
    query_url = f"https://api.spotify.com/v1/playlists/{id}"
    headers = get_auth_header(token)
    result = get(query_url,headers=headers)

    json_result = json.loads(result.content)
    return json_result   

#Returns list of spotify genres
def get_genres(token):
    query_url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

#Returns spotify track data associated with a track
def song_data(token,track_name):
    assert isinstance(track_name,str)

    #Relevant features
    audio_features = {"acousticness":0,"danceability":1,"duration_ms":2,"energy":3,"instrumentalness":4,"key":5,"liveness":6,"loudness":7,"mode":8,
    "speechiness":9,"tempo":10,"time_signature":11,"valence":12}
    data = [0]*13
    dict = track_info(token,track_name)

    #
    for key in dict:
        if key in audio_features.keys():
            data[audio_features[key]] = dict[key]
    return data

#Searches for tracks with similar characteristics using spotify serach
def similar_search(token,track_name):
    headers = get_auth_header(token)
    track = track_search(token,track_name)
    artist = track["items"][0]["artists"][0]["name"]
    artist_info = artist_search(token,artist)
    genres = artist_info[0]["genres"]
    info = track_info(token,track_name)
    genre_list = get_genres(token)

    #Adjusts string to match spotify api genre search
    gen = ""
    j = 0
    for i in genres:
        if j!=0:
            break
        if (i in genre_list):
            gen = i
            j = 1     
    gen = gen.replace(" ","+")
    gen = gen.replace("&","%26")

    #Sets genre to pop if none is found
    if (gen == ""):
        gen = "pop"

    #Searches for similar track
    query_url = f"https://api.spotify.com/v1/recommendations?limit=10&seed_genres={gen}"
    data = song_data(token,track_name)
    categories = ["target_acousticness","target_danceability","target_duration_ms","target_energy","target_instrumentalness",
        "target_key","target_liveness","target_loudness","target_mode","target_speechiness","target_tempo","target_time_signature","target_valence"]
    for i in range(len(categories)):
        query_url += "&"
        query_url += categories[i] + "=" + str(data[i])
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    result = json_result

    return json_result