import pymysql
import hashlib
import time
import string

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()

db = pymysql.connect("localhost",'root','dkstFeb.1st','userlist')

cursor =db.cursor()

sql = """INSERT INTO userlist(UsernameMD5,PasswordMD5,UsernameVig,Authority)
                     VALUES('5717be2478c707846b3bcf6a78fb825b','e10adc3949ba59abbe56e057f20f883e','NewUser',0)"""

sql1 ="UPDATE userlist SET UsernameVig='hktkqj' WHERE UID=1"

sql2 ='''UPDATE userlist set PasswordMD5=%s WHERE UID=%d''' % (md5lize('980129'),11)

print(md5lize('980129'))
try :
    cursor.execute(sql2)
    db.commit()
except :
    db.rollback()

db.close()