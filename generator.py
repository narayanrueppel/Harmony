import openai
from dotenv import dotenv_values
import time

config = dotenv_values("gpt.env")  
openai.api_key = config["API_KEY"]
import lyrics
import themes

def generate(content):
    completion = openai.ChatCompletion.create(
        model ="gpt-4",
        messages = [{"role":"user","content":content}]
    )
    reply = completion["choices"][0]["message"]["content"]
    return reply

def get_theme_sentences():
    theme_list = themes.get_themes()
    file = open("theme_sentences.txt","w")
    for i in range(len(theme_list)):
        sentence = f"write five one line poems about {theme_list[i]} which dont include the word {theme_list[i]}"
        answer = generate(sentence)
        file.write(answer)
        file.write("\n")
        time.sleep(5)
    file.close()
