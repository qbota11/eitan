
import nltk
from nltk.stem import WordNetLemmatizer

import mydb

def getPOS(t):
    pos = ""
    gen = ""
    lemmatizer = WordNetLemmatizer()
    if len(t[0]) < 2:
        return
    if not str.isalpha(t[0]):
         return
    if t[0][0] == "'":
        return
    if t[1] == "JJ" or t[1] == "JJR" or t[1] == "JJS":
        pos = "形容詞"
        gen = t[0].lower()
    elif  t[1] == "NN" or t[1] == "NNS":
        pos = "名詞"
        gen = lemmatizer.lemmatize(t[0].lower(), pos="n")
    elif  t[1] == "RB" or t[1] == "RBR" or t[1] == "RBS":
        pos = "副詞"
        gen = t[0].lower()
    elif  t[1] == "VB" or t[1] == "VBD" or t[1] == "VBG" or t[1] == "VBN" or t[1] == "VBP" or t[1] == "VBZ":
        pos = "動詞"
        gen = lemmatizer.lemmatize(t[0].lower(), pos="v")
        if gen == "be" or gen == "do":
            return
    if not pos:
        return
    if not checkPOS(gen,pos):
        return
    return pos,gen,t[0].lower()

from nltk.corpus import wordnet

def checkPOS(word,moto_pos):
    lemmas = wordnet.lemmas(word)
    pos = []
    for lemma in lemmas:
        if lemma.synset().pos() == 'n':
            pos.append("名詞")
        elif lemma.synset().pos() == 's' or lemma.synset().pos() == 'a':
            pos.append("形容詞")
        elif lemma.synset().pos() == 'r':
            pos.append("副詞")
        elif lemma.synset().pos() == 'v':
            pos.append("動詞")
    if not pos or moto_pos not in pos:
        return False
    return True


#ファイルを読み込んでテキストを解析
def parseText(file_path,source):
    f = open(file_path, 'r',encoding='utf-8')
    text = f.read()
    f.close()
    CONN = mydb.getDB()
    moto_source = source
    for t in nltk.pos_tag(nltk.word_tokenize(text)):
        source = moto_source
        a_words = getPOS(t)
        if not a_words:
            continue
        pos = a_words[0]
        gen = a_words[1]
        word = a_words[2]
        sql = "SELECT * FROM eitan WHERE gen = %s LIMIT 1;"
        cur = CONN.cursor(dictionary=True)
        cur.execute(sql,(gen,))
        rows = cur.fetchall() 
        cur.close()
        if not rows:
            sql = "INSERT INTO eitan SET pos = %s ,gen = %s ,words = %s ,source = %s ;"
            cur = CONN.cursor()
            cur.execute(sql,(pos,gen,word,source))
            CONN.commit()
            cur.close()
            continue
        row = rows[0]
        count = 0
        if source not in row["source"]:
            count = 1
        if source not in row["source"]:
            source = row["source"]+","+source
        if pos not in row["pos"]:
                pos = row["pos"]+","+pos
        if word not in row["words"]:
            word = row["words"]+","+word
        sql = "UPDATE eitan SET pos = %s ,words= %s ,source= %s,count = count+%s WHERE gen = %s LIMIT 1;"
        cur = CONN.cursor()
        cur.execute(sql,(pos,word,source,count,gen))
        CONN.commit()
        cur.close()
    CONN.close()


parseText('01.txt','x0x大学****年度')