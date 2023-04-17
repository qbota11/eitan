

import mydb
import unicodedata
def isJapanese(string):
    if not string:
        return False
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

import re
def JudgeKatakana(word):
    re_katakana = re.compile(r'[\u30A1-\u30FF]+')
    return re_katakana.fullmatch(word.replace(" ","").replace("　",""))


from googletrans import Translator
def findMeaningByGoogle():
    CONN = mydb.getDB()
    sql = "SELECT gen FROM eitan WHERE meaning = '';"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    rows = cur.fetchall() 
    cur.close()
    for row in rows:
        try:
            meaning = Translator().translate(row["gen"], src="en", dest="ja").text
        except:
            continue
        if JudgeKatakana(meaning):
            continue
        if isJapanese(meaning):
              sql = "UPDATE eitan SET meaning = %s  WHERE gen = %s LIMIT 1;"
              cur = CONN.cursor()
              cur.execute(sql,(meaning,row["gen"]))
              CONN.commit()
              cur.close()
    CONN.close



import sqlite3
#https://bond-lab.github.io/wnja/ からwnjpn.dbをダンロードし適当な場所に配置。
def getMeaning(word,limit):
    conn = sqlite3.connect("./wnjpn.db")
    cur = conn.cursor()
    sql = "\
        SELECT DISTINCT word_en.wordid, word_en.lemma,  word_ja.lemma\
        FROM sense sense_A, sense sense_B , word word_en , word word_ja \
        WHERE word_en.wordid = sense_A.wordid\
            and sense_A.lang = 'eng'\
            and sense_B.lang = 'jpn'\
            and sense_A.synset = sense_B.synset\
            and sense_B.wordid = word_ja.wordid\
            and word_en.lemma = ?\
        ORDER BY word_en.lemma"
    cur.execute(sql, (word,))
    before = 0
    meaning =  ""
    n  = 0
    i = 1
    for row in cur:
        if JudgeKatakana(row[2]):
            continue
        if before != row[0]:
            if meaning:
                meaning += " "
            meaning += str(i)+' ' + row[2]
            before = row[0]
            n = 1
            i += 1
        else :
            if n >= limit :
                continue
            n += 1
            meaning +=  ',' +row[2]
    if "2 " not in meaning:
        meaning = meaning.replace("1 ","")
    cur.close()
    conn.close()
    return meaning

def findMeaningByWordnet():
    CONN = mydb.getDB()
    sql = "SELECT * FROM eitan LIMIT 5;"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    rows = cur.fetchall() 
    cur.close()
    for row in rows:
        meaning = getMeaning(row["gen"],3)
        if  len(meaning) < 1:
            continue
        sql = "UPDATE eitan SET meaning= %s  WHERE gen = %s LIMIT 1;"
        cur = CONN.cursor()
        cur.execute(sql,(meaning,row["gen"]))
        CONN.commit()
        cur.close()
    CONN.close() 


findMeaningByWordnet()
#findMeaningByGoogle()