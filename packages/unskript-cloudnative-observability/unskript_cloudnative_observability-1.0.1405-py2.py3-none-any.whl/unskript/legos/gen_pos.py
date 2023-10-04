import os
import json
import spacy
import sys
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

nlp_pos = spacy.load("en_core_web_sm")

#return pos tagging
def create_index(sentence):
    text = (sentence)
    doc = nlp_pos(text)
    tokens = []
    for token in doc:
     # print (token, token.pos_)  
      if (token.pos_ == "VERB" or token.pos_=="NOUN" or token.pos_ == "PROPN" or token.pos_ == "ADJ"):
        if (str(token) == "list"):
            tokens.append((token, "VERB"))
        else:    
            tokens.append((token, token.pos_))
    return tokens

def lemmatization(sentence):
    lemmatized_sentence = []
    pos = []
    noun = []
    verb = []
    for (word, tag) in sentence:
     #   print (word, tag)
        if (tag == "NOUN" or tag == "PROPN"):
            noun.append(str(word))
            tag_ = 'n'
        if (tag == "VERB"):
            verb.append(str(word))
            tag_ = 'v'
        if (str(word) == "list"):
            tag_ = 'v'
    return (verb, noun)


def pos(objs, filename):
    sentence = (objs['action_title'])
    sentence = sentence.lower()
    index = create_index(sentence)
    (verb, noun) = lemmatization(index)
    objs['action_verbs'] = verb
    objs['action_nouns'] = noun
    json_object = json.dumps(objs, indent = 2)
    with open(filename, "w") as fp:
       fp.write(json_object)
    

 
if __name__ == '__main__':
   #print (sys.argv[1])
   objs = json.load(open(sys.argv[1]))
   with open('../list_of_files_modified') as file:
    files = [line.rstrip() for line in file]
   if (sys.argv[1] in files):
     print ("hello", sys.argv[1])
   else:
     #print ("need", sys.argv[1])
      print (sys.argv[1])
      pos(objs, sys.argv[1])
