from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json 
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


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


def get_auth_header(token):
    return {"Authorization": "Bearer "+token}


def artist_search(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result


def track_search(token,track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)["tracks"]
    if len(json_result) == 0:
        print("No playlist with this name exists...")
        return None
    return json_result

def playlist_search(token,playlist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={playlist_name}&type=playlist&limit=1"
    query_url = url + query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)["playlists"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result

def track_id(track_result):
    return track_result["items"][0]["id"]


def artist_id(artist_result):
    return artist_result[0]["id"]

def playlist_id(playlist_result):
    return playlist_result["items"][0]["id"]

def track_info(token,track_name):
    track = track_search(token,track_name)
    id = track_id(track)
    query_url = f"https://api.spotify.com/v1/audio-features/{id}"
    headers = get_auth_header(token)
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)
    return json_result

def playlist_info(track,playlist_name):
    playlist = playlist_search(token,playlist_name)
    id = playlist_id(playlist)
    query_url = f"https://api.spotify.com/v1/playlists/{id}"
    headers = get_auth_header(token)
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)
    return json_result   


def get_genres(token):
    query_url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

def song_data(token,track_name):
    audio_features = {"acousticness":0,"danceability":1,"duration_ms":2,"energy":3,"instrumentalness":4,"key":5,"liveness":6,"loudness":7,"mode":8,
    "speechiness":9,"tempo":10,"time_signature":11,"valence":12}
    assert isinstance(track_name,str)
    data = [0]*13
    dict = track_info(token,track_name)
    for key in dict:
        if key in audio_features.keys():
            data[audio_features[key]] = dict[key]
    return data

def similar_search(token,track_name):
    headers = get_auth_header(token)
    track = track_search(token,track_name)
    artist = track["items"][0]["artists"][0]["name"]
    artist_info = artist_search(token,artist)
    genres = artist_info[0]["genres"]
    info = track_info(token,track_name)
    genre_list = get_genres(token)
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
    if (gen == ""):
        gen = "pop"
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
    for i in range(10):
        print(result[i]["name"] + " by " + result[i]["artists"][0]["name"])
    return json_result