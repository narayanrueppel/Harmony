
#Returns all classification themes in list formå
def get_themes():
    file = open("themes.txt","r")
    theme_list = file.readlines()
    file.close()
    for i in range(len(theme_list)):
        theme_list[i] = theme_list[i][:-1]
    return theme_list

#Returns all theme sentences for spacy training 
def get_data():

    #Gets data
    data = {}
    themes = get_themes()
    file = open("theme_sentences.txt","r")
    sentences = file.readlines()
    file.close()

    #
    for i in range(len(sentences)):
        sentences[i] = sentences[i][3:-1] # Truncates start to get rid of numbers
        if(sentences[i][0] == "\""):
            sentences[i] = sentences[i][1:-1]
    
    #Adds sentences to list
    for i in range(len(sentences)//5):
        sentence_list = []
        for j in range(5):
            sentence_list.append(sentences[i*5+j])
        data[themes[i]] = sentence_list
    return data