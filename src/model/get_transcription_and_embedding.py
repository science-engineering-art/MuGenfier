from dataclasses import replace
import os
import subprocess
import json
import re
from textblob import TextBlob
import requests

SETS = ['training', 'validation', 'tests']
GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']


def clean(jsondata : str):
    jsondata = jsondata.replace("{\"text\":", "")
    jsondata = jsondata.replace("}", "")
    jsondata = jsondata.replace("\"", "")

    not_allowed = r"[!@#$%^&*-+=<>/\\|'\"`~]"

    jsondata = re.sub(not_allowed, "" , jsondata)

    for i in range(1,len(jsondata)):
        if jsondata[i].isupper() and jsondata[i-1] != " ":
            jsondata = jsondata[:i] + ". " + jsondata[i:]
            
    return jsondata


def clean_and_get_embedding_all(path):
    model = "text-embedding-ada-002"

    for root, dirs, files in os.walk(path):
        for name in files:
            if root.find("features/genres_lyrics") == -1:
                continue
            
            
            modified_root = root.replace("genres_lyrics", "lyrics_embedding")      
            
            if f"{os.path.splitext(name)[0]}_ebdd.json" in os.listdir(modified_root):
                continue
            
            print(name)
            
            # clean
            jsondata = ""
            try:
                jsondata = ""
                with open(root + f"/{os.path.splitext(name)[0]}.json", "r") as f:
                    jsondata =  json.load(f)
                    print(name,"\n\n")
                    
                    jsondata = clean(jsondata)
                root : str
                      
                with open(modified_root + f"/{os.path.splitext(name)[0]}_ebdd.json", "x") as f:  
                
                    lbracket = "{"
                    rbracket = "}"
                    
                      
                    print(f"curl http://localhost:8080/v1/embeddings -H \"Authorization: Bearer OPENAI_API_KEY\" -H \"Content-Type: application/json\" -d \'{lbracket} \"input\": \"{jsondata}\", \"model\": \"{model}\" {rbracket}\' " )
                    
                    
                    output = subprocess.check_output(f"curl http://localhost:8080/v1/embeddings -H \"Authorization: Bearer OPENAI_API_KEY\" -H \"Content-Type: application/json\" -d \'{lbracket} \"input\": \"{jsondata}\", \"model\": \"{model}\" {rbracket}\' " , shell=True)
                    
                    result = output.decode()
                    # subprocess.check_output()
                    result = re.findall(r"\[-?\d.*\d\]",result)
                    result = [float(x) for x in re.findall(r"-?\d+\.?\d+",result[0])]
                    
                    json.dump(result, f)
                    
            except:
                print("some error ocurr: ", name)
                try:
                    os.remove(modified_root + f"/{os.path.splitext(name)[0]}_ebdd.json")
                    print("dumb json deleted")
                except:
                    pass
            
def get_transcription(path):      
        # transcription
        
        
        
    model = "whisper-medium.bin"
    for root, _, files in os.walk(path):
        for name in files:
            print(name)
            if root.find("/data/") == -1 or name.find("jazz.00054") != -1:
                    continue
            
            print(root)
            modified_root = root.replace("/data/", "/features/genres_lyrics/") 
            
            
            jsondata = ""
            try:
                with open(modified_root + f"/{os.path.splitext(name)[0]}.json", "r") as f:
                    jsondata =  json.load(f)
            except:
                try:
                    os.remove(f"{modified_root}/{os.path.splitext(name)[0]}.json")
                    print("dumb json deleted")
                except:
                    pass

            if f"{os.path.splitext(name)[0]}.json" in os.listdir(modified_root):
                print(f"file {name} already processed")
                continue

            try:
                with open(modified_root + f"/{os.path.splitext(name)[0]}.json", "x") as f:
                    pathhh = "@$PWD/" + os.path.relpath(root + "/" + name);
                    
                    print(f"curl http://localhost:8080/v1/audio/transcriptions -H \"Content-Type: multipart/form-data\" -F file=\"{pathhh}\" -F model=\"{model}\"")
                    
                    output = subprocess.check_output(f"curl http://localhost:8080/v1/audio/transcriptions -H \"Content-Type: multipart/form-data\" -F file=\"{pathhh}\" -F model=\"{model}\"", shell = True)
                    result = output.decode()
                    
                    json.dump(result, f)
            except:
                try:
                    os.remove(f"{modified_root}/{os.path.splitext(name)[0]}.json")
                    print("dumb json deleted")
                except:
                    pass
            
if __name__ == '__main__':    
    
    for set in SETS:
        try:
            os.mkdir(f"./dataset/split/{set}/features/lyrics_embedding")
            os.mkdir(f"./dataset/split/{set}/features/genres_lyrics")
        except:
            pass
        for genre in GENRES:
            try:
                os.mkdir(f"./dataset/split/{set}/features/lyrics_embedding/{genre}")
                os.mkdir(f"./dataset/split/{set}/features/genres_lyrics/{genre}")
            except:
                pass
        
    path = os.getcwd() + "/dataset/split"
    get_transcription(path)
    clean_and_get_embedding_all(path)   
