from lyricsgenius import Genius
from dotenv import dotenv_values
import spacy
from spacy.lang.en import English
import classy_classification

##Accesses Genius  lyrics databse
config = dotenv_values("genius.env")  
genius = Genius(config["ACCESS_TOKEN"])
genius.verbose = False #Shortens information given

#Loads spacy language model
nlp = spacy.load("en_core_web_sm")


#Takes input text and lemmatizes it using spacy
#Lemmatized text contains only word stems
def lemmatize(text):
    assert isinstance(text,str)
    doc = nlp(text)
    lem = ""
    for token in doc:
        lem += token.lemma_ + " "
    return lem

#Gets song lyrics of given track
def get_lyrics(track_name):
    assert isinstance(track_name,str)
    song = genius.search_song(track_name,get_full_info=True)
    return song.lyrics
