from openai import OpenAI
from PyQt5 import QtCore, QtGui, QtWidgets

# load api key
apiKey = ''
with open('lib/apiKey.txt', 'r', encoding='utf-8') as f:
    apiKey = f.read()
stopKey ="\n"

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = apiKey
)

def chat(inStr:str, log=False):
    if (log==True): 
        print(f"\n\n[Input]\n{inStr}")
            
    outStr = ''
    
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role":"user","content":inStr}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=10240,
        stream=True
    )
    
    if (log==True): 
        print("\n\n[AI answer]")

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            if (log==True): 
                print(chunk.choices[0].delta.content, end='')
            outStr += chunk.choices[0].delta.content

    return outStr

def chatSync(inStr:str, box, log=False):
    if (log==True): 
        print(f"\n\n[Input]\n{inStr}")
            
    outStr = ''
    
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role":"user","content":inStr}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=10240,
        stream=True
    )
    
    if (log==True): 
        print("\n\n[AI answer]")

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            if (log==True): 
                print(chunk.choices[0].delta.content, end='')
            outStr += chunk.choices[0].delta.content
            box.setText(QtCore.QCoreApplication.translate("Dialog", outStr))
            box.repaint()
    return outStr