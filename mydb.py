
'''
CREATE TABLE eitan(
     gen VARCHAR(100) NOT NULL PRIMARY default "",
     pos VARCHAR(100) NOT NULL default "",
     words VARCHAR(200) NOT NULL default "",
     meaning VARCHAR(200) NOT NULL default "",
     source VARCHAR(8000) NOT NULL default "",
     example VARCHAR(500) NOT NULL default "",
     example_yaku VARCHAR(500) NOT NULL default "",
     count INT NOT NULL default 1,
  ) ;

'''

import mysql.connector
def getDB():
        return mysql.connector.connect(user='root', password='*****',host='localhost', database='*****')