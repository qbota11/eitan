import nltk
from nltk.stem import WordNetLemmatizer

import mydb
import random

def makeQuestionCSV(pattern):
    CONN = mydb.getDB()
    sql = "SELECT * FROM eitan  ORDER BY COUNT DESC;"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    rows = cur.fetchall() 
    cur.close()
    sql = "SELECT pos,gen,words,meaning FROM eitan WHERE pos LIKE '%動詞%';"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    v_pool = cur.fetchall() 
    cur.close()
    sql = "SELECT pos,gen,words,meaning FROM eitan WHERE pos LIKE '%名詞%';"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    n_pool = cur.fetchall() 
    cur.close()
    sql = "SELECT pos,gen,words,meaning FROM eitan WHERE pos LIKE '%形容詞%';"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    a_pool = cur.fetchall() 
    cur.close()
    sql = "SELECT pos,gen,words,meaning FROM eitan WHERE pos LIKE '%副詞%';"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    r_pool = cur.fetchall() 
    cur.close()
    pool = []
    i = 0
    fi = 0
    f_text = ""
    for row in rows:
        pos = row["pos"].split(",")[0]
        if pos == "名詞":
            pool = n_pool
        elif pos == "動詞":
            pool = v_pool
        elif pos == "形容詞":
            pool = a_pool
        elif pos == "副詞":
            pool = r_pool
        correct_position = random.randrange(1,5)
        if pattern == "英日":
            q = "[b]"+row["gen"]+"[/b]の意味として最も適したものを一つ選んで下さい。"
        elif pattern == "日英":
              meaning = row["meaning"].replace(",","%(=)%")
              q = "[b]"+meaning+"[/b]に対応する英単語として最も適したものを一つ選んでください。"
        options = ""
        for n in range(1,6):
            if n == correct_position:
                options += makeOption(row,pattern)
            else:
                options += makeOption(pool[random.randrange(0,len(pool))],pattern)
        commentary = makeCommentary(row)
        f_text += q+","+options+",,,,,"+str(correct_position)+","+commentary+"\n"
        i += 1
        if i >= 200:
            f = open(pattern+str(fi)+'.csv', 'w', encoding='UTF-8')
            f.write(f_text)
            f.close()
            fi += 1
            f_text = ""
            i = 0
    f = open(pattern+str(fi)+'.csv', 'w', encoding='UTF-8')
    f.write(f_text)
    f.close()
               
        
def makeOption(row,pattern):
    meaning = row["meaning"].replace(",","%(=)%")
    pos = ""
    for hin in row["pos"].split(","):
        pos += "[span style='border:1px #cdc4c4 solid;border-radius:5px;font-size:0.8rem;padding:0.1rem;background-color:#ebeeee;margin:0 0.2rem;']"+hin+"[/span]"
    word_list = row["words"].split(",")
    if row["gen"] not in word_list:
        word_list.append(row["gen"])
    tan = ""
    word_list.sort(key=len)
    for t in word_list:
        tan += "[span style='margin-right:0.5rem;']"+t+"[/span]"
    if pattern == "英日":
        option = meaning +"**+-+**"+"使用例: "+pos+tan+","
    elif pattern == "日英":
        meaning = "[p]意味: "+meaning.replace(",","%(=)%")+"[/p]"
        option = row["gen"] +"**+-+**"+"[p]使用例: "+pos+tan+"[/p]"+meaning+","

    return option
def makeCommentary(row):
    text= ""
    t1 = f"[p]{row['gen']}を使って簡単な英文を作って下さい。[/p]"
    text +=  setBloon(t1,"https://ja.mondder.com/public/users/2023/4/11681359885.webp","Mondder","l")
    t2 = setPTag(row['example'])
    text +=  setBloon(t2,"https://ja.mondder.com/public/users/2023/4/11681360375.webp","ChatGPT","r")
    t3 = f"[p]この例文に使われている単語の品詞を判定して下さい。[/p]"
    text +=  setBloon(t3,"https://ja.mondder.com/public/users/2023/4/11681359885.webp","Mondder","l")
    t4 = setPOS(row['example'])
    text +=  setBloon(t4,"https://ja.mondder.com/public/users/2023/4/11681360306.webp","NLTK","r")
    t5 = f"[p]例文を日本語に翻訳して下さい。[/p]"
    text +=  setBloon(t5,"https://ja.mondder.com/public/users/2023/4/11681359885.webp","Mondder","l")
    t6 = setPTag(row['example_yaku'])
    if len(row['example']) < 55:
        text +=  setBloon(t6,"https://ja.mondder.com/public/users/2023/4/11681360109.webp","Google","r")
    else:
        text +=  setBloon(t6,"https://ja.mondder.com/public/users/2023/4/11681360163.webp","DeepL","r")
    source =""
    source_list = row["source"].split(",")
    random.shuffle(source_list)
    for i,src in enumerate(source_list):
        if i > 12:
            source += "など"
            break
        if len(source)>1:
            source += ","
        source += src
       
    text += "[div class='simple-box']"+source+"に登場。[/div]"
    
    return text.replace(",","%(=)%")
def setPTag(text):
    result = ""
    text = text.replace(",","%(=)%")
    for e  in text.split("\n"):
        result +=  "[p]"+e+"[/p]"
    return  result


def setBloon(text,img,alt,mode):
    if len(text) <1:
        return ""
    if mode == "l":
        return f'[div class="speech-balloon balloon-left"][img class="balloon-icon" width="50" height="50" src="{img}" alt="{alt}"][div class="balloon-talk talk-left"]{text}[/div][/div]'
    else:
         return f'[div class="speech-balloon balloon-right"][div class="balloon-talk talk-right"]{text}[/div][img class="balloon-icon" width="50" height="50" src="{img}" alt="{alt}"][/div]'
def setPOS(text):
    if len(text) <1:
        return ""
    result = ""
    for te  in text.split("\n"):
        temp = ""
        for t in nltk.pos_tag(nltk.word_tokenize(te)):
            if t[1] in ['NN','NNS']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]名[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['NNP','NNPS']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]固[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]動[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['JJ','JJR','JJS']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]副[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['RB','RBR','RBS']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]形[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['PRP','WP']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]代[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['PRP$','WP$']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]所代[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['IN']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]前接[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['TO']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]前[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['DT','WDT']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]限[/rt][rp])[/rp][/ruby] "
            elif t[1] in ['MD']:
                temp += f"[ruby]{t[0]}[rp]([/rp][rt]助[/rt][rp])[/rp][/ruby] "
            else:
                temp += f"[span]{t[0]}[/span] "
        result += "[p]"+temp+"[/p]"
    return result
        

makeQuestionCSV("日英")