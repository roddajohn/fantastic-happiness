import hashlib
import sqlite3

f="users.db"
db=sqlite3.connect(f)
c=db.cursor()

class User:
    uid=0
    username=""
    password=""
    age=0
    email=""
    contributed=""

    def update_pw(unhashed):
        self.password=hash(unhashed)

    def update():
        c.execute("UPDATE users SET username=username,password=update_pw(password),age=age,email=email contributed=contributed WHERE uid=uid")
        
db.commit()
db.close()

def hash(unhashed):
    mho=hashlib.sha1()
    mho.update(unhashed)
    return mho.hexdigest()

def register(username,password,age,email):
    c.execute("select uid from users where username="+username)
    data=c.fetchall()
    if len(data)!=0:
        return false
    c.execute("select uid from users")
    data=c.fetchall()
    c.execute("insert into users values (%d,%s,%s,%d,%s,"");"%(len(data)+1,username,hash(password),age,email))
    return true

