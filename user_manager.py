import hashlib
import sqlite3

f="sturdy-octo-train.db"
db=sqlite3.connect(f)
c=db.cursor()

class User:
    user_id=0
    username=""
    password=""
    age=0
    email=""
    posts_contributed_to=""

    #def update_pw(unhashed):
        #self.password=hash(unhashed)

    def update():
        c.execute("update users set username=%s,password=%s,age=%d,email=%s posts_contributed_to=%s where user_id=%d"%(username,hash(password),age,email,pots_contributed_to,user_id))
        
def hash(unhashed):
    mho=hashlib.sha1()
    mho.update(unhashed)
    return mho.hexdigest()

#0 username exists
#1 success
def register(username,password,age,email):
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)!=0:
        return 0
    c.execute("select user_id from users")
    data=c.fetchall()
    c.execute("insert into users values ('%d','%s','%s','%d','%s','')"%(len(data)+1,username,hash(password),age,email))
    return 1

#0 no such username
#1 success
#2 wrong password
def login(username,password):
    c.execute("select password from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)==0:
        return 0
    if data[0][0]==hash(password):
        return 1
    return 2
    
#0 no such username
#1 success
def remove(username):
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)==0:
        return 0
    c.execute("delete from users where username='%s'"%(username))
    return 1

def exists(username):
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    return len(data)!=0

"""        
print register("homer","simpson",20,"blah@gmail.com")
print login('homer','simpson')
print login("homer","as")
print exists("homer")
print remove("homer")
print exists("homer")
"""

db.commit()
db.close()

