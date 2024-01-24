import funcs

#Dictionary of relevant song data tracked by Spotify
audio_features = {"acousticness":0,"danceability":1,"duration_ms":2,"energy":3,"instrumentalness":4,"key":5,"liveness":6,"loudness":7,"mode":8,
    "speechiness":9,"tempo":10,"time_signature":11,"valence":12}


#Returns song data associated with a particular track
def song_data(track_name):
    assert isinstance(track_name,str)
    data = [0]*13
    token = funcs.get_token()
    dict = funcs.track_info(token,track_name)
    for key in dict:
        if key in audio_features.keys():
            data[audio_features[key]] = dict[key]
    return data

#Searches for songs by genre using Spotify API
def song_by_genre(genre_name):
    assert isinstance(genre_name,str)
    token = funcs.get_token()
