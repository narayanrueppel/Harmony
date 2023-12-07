import themes
import lyrics
import funcs
import spacy
from spacy.lang.en import English
import classy_classification
from collections import Counter
import math

def get_data():
    data = themes.get_data()
    return data

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

def top_themes(track_name,data):
    theme_dict = classify_song(track_name,data)
    k = Counter(theme_dict)
    top_10 = k.most_common(10)
    print(top_10)

def get_json(track_name):
    token = funcs.get_token()
    json = funcs.similar_search(token,track_name)
    return json

def get_recs(json):
    recs = []
    for i in range(10):
        recs.append(json[i]["name"])
    return recs

def artists(json):
    artist_dict = {}
    for i in range(10):
        artist_dict[json[i]["name"]] = json[i]["artists"][0]["name"]
    return artist_dict

def classify_recs(recs,data):
    recs_dict = {}
    for i in recs:
        recs_dict[i] = classify_song(i,data)
    return recs_dict


def best_rec(theme_dict,recs_dict):
    vals = {}
    keys = theme_dict.keys()
    recs_keys = recs_dict.keys()
    for i in recs_keys:
        vals[i] = 0
        for j in keys:
            vals[i] += (theme_dict[j]-recs_dict[i][j])**2
        vals[i] = vals[i]/10
    return vals

def songs(dict):
    k = Counter(dict)
    top_10 = k.most_common(10)
    return top_10

def driver(song):
    data = get_data()
    json = get_json(song)
    recs = get_recs(json)
    artists_dict = artists(json)
    recs_dict = classify_recs(recs,data)
    theme_dict = classify_song(song,data)
    new_recs = best_rec(theme_dict,recs_dict)
    top_songs = songs(new_recs)
    for i in top_songs:
        print(i + "by " + artists_dict[i])


if __name__ == "__main__":
    song = input("What song would you like recommendations for?")
    driver(song)