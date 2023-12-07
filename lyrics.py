from lyricsgenius import Genius
from dotenv import dotenv_values
import spacy
from spacy.lang.en import English
import classy_classification

config = dotenv_values("genius.env")  
genius = Genius(config["ACCESS_TOKEN"])
#artist = genius.search_artist("Ariana Grande", max_songs=3, sort="title")
nlp = spacy.load("en_core_web_sm")
#doc3 = nlp(lemmatize(get_lyrics("Disturbia")))
#print("Noun phrases:", [chunk.text for chunk in doc3.noun_chunks])

def lemmatize(text):
    assert isinstance(text,str)
    doc = nlp(text)
    lem = ""
    for token in doc:
        lem += token.lemma_ + " "
    return lem

def get_lyrics(track_name):
    print(track_name)
    assert isinstance(track_name,str)
    song = genius.search_song(track_name,get_full_info=True)
    return song.lyrics
