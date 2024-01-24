import themes
import lyrics
import funcs
import spacy
from spacy.lang.en import English
import classy_classification
from collections import Counter
import math



#Returns theme and theme sentence data 
def get_data():
    data = themes.get_data()
    return data


#Identifies theme levels in song using spacy
def classify_song(track_name,data):
    nlp = spacy.blank("en")
    nlp.add_pipe(
        "classy_classification",
        config={
            "data": data,
            "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "device": "cpu"
        }
    )
    theme_dict = nlp(lyrics.get_lyrics(track_name))._.cats
    return theme_dict


#Gets top ten themes from a dictionary of themes and values
def top_themes(track_name,data):
    theme_dict = classify_song(track_name,data)
    k = Counter(theme_dict)
    top_10 = k.most_common(10)
    

#Finds similar songs using spotify search
def get_json(track_name):
    token = funcs.get_token()
    json = funcs.similar_search(token,track_name)
    return json


#Returns the track name of a recommendation
def get_recs(json):
    recs = []
    for i in range(10):
        recs.append(json[i]["name"])
    return recs


#Gets artist associated with recommendation track
def artists(json):
    artist_dict = {}
    for i in range(10):
        artist_dict[json[i]["name"]] = json[i]["artists"][0]["name"]
    return artist_dict


#Classifies rec tracks using spacy
def classify_recs(recs,data):
    recs_dict = {}
    for i in recs:
        recs_dict[i] = classify_song(i,data)
    return recs_dict


#Calculates best recommended tracks
def best_rec(theme_dict,recs_dict):

    #Obtains target track and recommended tracks data
    vals = {}
    keys = theme_dict.keys()
    recs_keys = recs_dict.keys()

    #Finds each rec track's difference 
    for i in recs_keys:
        vals[i] = 0
        for j in keys:
            vals[i] += (theme_dict[j]-recs_dict[i][j])**2
        vals[i] = vals[i]/10
    return vals

#Returns top ten track recommnedations
def songs(dict):
    k = Counter(dict)
    top_10 = k.most_common(10)
    return top_10


#Main function which takes in track, and prints out 10 ranked recommendations
def main(song):

    #Gets track data and track recommendation data
    data = get_data()
    json = get_json(song)
    recs = get_recs(json)

    #Finds recommendation track data and ranks them
    artists_dict = artists(json)
    recs_dict = classify_recs(recs,data)
    theme_dict = classify_song(song,data)
    new_recs = best_rec(theme_dict,recs_dict)
    top_songs = songs(new_recs)

    #Output ranked recommended track
    for i in top_songs:
        print(i[0] + "by " + artists_dict[i[0]])


if __name__ == "__main__":
    song = input("What song would you like recommendations for? ")
    main(song)