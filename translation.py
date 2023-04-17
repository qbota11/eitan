
import mydb



import deepl
def deeplTrans():
    translator = deepl.Translator("***********************************")
    CONN = mydb.getDB()
    sql = "SELECT gen,example FROM eitan WHERE example_yaku = '' AND CHAR_LENGTH(example) >= 55;"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    rows = cur.fetchall() 
    cur.close()
    for row in rows:
        try:
            yaku = translator.translate_text(row["example"],source_lang="EN",target_lang="JA").text
        except:
            continue
        if len(yaku) > 5:
              sql = "UPDATE eitan SET example_yaku= %s  WHERE gen = %s LIMIT 1;"
              cur = CONN.cursor()
              cur.execute(sql,(yaku,row["gen"]))
              CONN.commit()
              cur.close()
    CONN.close


from googletrans import Translator
def googleTrans():
    CONN = mydb.getDB()
    sql = "SELECT gen,example FROM eitan WHERE example_yaku = '' AND CHAR_LENGTH(example) < 55;"
    cur = CONN.cursor(dictionary=True)
    cur.execute(sql,())
    rows = cur.fetchall() 
    cur.close()
    for row in rows:
        try:
            yaku = Translator().translate(row["example"], src="en", dest="ja").text
        except:
            continue
        if len(yaku) > 5:
              sql = "UPDATE eitan SET example_yaku= %s  WHERE gen = %s LIMIT 1;"
              cur = CONN.cursor()
              cur.execute(sql,(yaku,row["gen"]))
              CONN.commit()
              cur.close()
    CONN.close

#55文字以下はGoogleでそれ以上はdeeplで訳した
#googleTrans()
#deeplTrans()
