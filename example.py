
import mydb
import openai
def exampleByGPT(word):
    openai.api_key = "********************************"
    word = "「"+word+"」"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": word+"という単語を使って簡単な英文を作って下さい。\n"},
        ],
        )
    return (response.choices[0]["message"]["content"].strip())
def createExample():
     CONN = mydb.getDB()
     sql = "SELECT gen FROM eitan WHERE example = '';"
     cur = CONN.cursor(dictionary=True)
     cur.execute(sql,())
     rows = cur.fetchall() 
     cur.close()
     for row in rows:
         try:
             example = exampleByGPT(row["gen"])
         except Exception as e:
             print(e)
             #continue
             return
         if len(example) < 5:
             continue
         sql = "UPDATE eitan SET example= %s  WHERE gen = %s LIMIT 1;"
         cur = CONN.cursor()
         cur.execute(sql,(example,row["gen"]))
         CONN.commit()
         cur.close()
     CONN.close()  

createExample()