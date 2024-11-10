from .img2txt import readImg
from .LLM import chat, chatSync
import json

def img2word(img):
    data = readImg(img)['metadata']
    data.reverse()
    line = []
    words = []
    
    l = []    
    lastY = 0
    for token in data:
        print(token)
        ys = [token['polygon']['y1'], token['polygon']['y2'], token['polygon']['y3'], token['polygon']['y4']]
        y1, y2 = min(ys), max(ys)
        
        if (lastY < y1 and lastY != 0):
            line.append(sorted(l, key=lambda x : x['polygon']['x1']))
            l = []
            
        lastY = (y1+y2)/2
        l.append(token)
        
    for l in line:
        ss = "" 
        lastX = 0
        for token in l:
            xs = [token['polygon']['x1'], token['polygon']['x2'], token['polygon']['x3'], token['polygon']['x4']]        
            ys = [token['polygon']['y1'], token['polygon']['y2'], token['polygon']['y3'], token['polygon']['y4']]
            x1, x2 = min(xs), max(xs)
            y1, y2 = min(ys), max(ys)
            
            fontSize = y2-y1
            
            if (fontSize < (x1-lastX) and lastX != 0):
                words.append(ss)
                ss = ''
                lastX = 0
            lastX = x2
            ss += token['label']
        words.append(ss)
        
    return words

def correction(words, log=False):
    outStr = chat( f"""
영단어장을 만들어줘. 단, 아래 규칙을 따라.
1. 영단어가 손상되었다면 이를 보정해. 보정 사실은 표기하지마.
2. '영단어', '뜻', 예문들'을 '/'으로 구분해서 한번에 한줄로 정리해. 
3. **를 사용한 강조는 하지마.

    영단어:"
{words}
"
"""
        , log=log
    )
    outStr = chat( f"""
다음 문자열에서 보정되었다는 내용만 제거해. 기존 형식은 유지해.

    영단어장:"
{outStr}
"
"""
        , log=log
    )

    voca = []
    for line in outStr.split('\n'):
        if (len(line) == 0 or line[0] != '*'): continue
        
        source = line[1:].strip().split('/')
        word = source[0].strip()
        mean = source[1]
        ex = [s.strip().replace('"', '') for s in source[2:]]
        voca.append({'word': word, "mean":mean, 'ex':ex})
    
    return voca

def genReading(voca, box, leng = 1000, log=False, subject="상관없어."):
    ss = ''
    for w in voca:
        ss += f"{w['word']}:{w['mean']}\n"
    
    outStr = chatSync( f"""
영단어장의 영단어를 이용해서 1000자 정도의 영어로된 읽을 거리를 작성해줘.
**를 사용한 강조는 하지말고 텍스트로만 적어.
    영단어:"
{ss}
"
"""
        ,box
        , log=log
    )
    
    return outStr