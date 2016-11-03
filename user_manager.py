import hashlib
import sqlite3


class User:
    user_id=0
    username=""
    password=""
    age=0
    email=""
    posts_contributed_to=""

    #def update_pw(unhashed):
        #self.password=hash(unhashed)

    def update(self):
        f="sturdy-octo-train.db"
        db=sqlite3.connect(f)
        c=db.cursor()
        c.execute("update users set username=%s,password=%s,age=%d,email=%s posts_contributed_to=%s where user_id=%d"%(username,hash(password),age,email,pots_contributed_to,user_id))
        db.commit()
        db.close()
               
def hash(unhashed):
    mho=hashlib.sha1()
    mho.update(unhashed)
    return mho.hexdigest()

def get(uid):
    f="sturdy-octo-train.db"
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select * from users where user_id='%s'"%(uid))
    data=c.fetchall()
    user=User()
    user.user_id=uid
    user.username=data[0][1]
    user.password=data[0][2]
    user.age=data[0][3]
    user.email=data[0][4]
    user.posts_contributed_to=data[0][5]
    db.commit()
    db.close()
    return user

#0 username exists
#1 success
def register(username,password,age,email):
    f="sturdy-octo-train.db"
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)!=0:
        db.commit()
        db.close()
        return 0
    c.execute("select user_id from users")
    data=c.fetchall()
    c.execute("insert into users values ('%d','%s','%s','%d','%s','')"%(len(data)+1,username,hash(password),age,email))
    db.commit()
    db.close()
    return 1

#0 no such username
#1 success
#2 wrong password
def login(username,password):
    f="sturdy-octo-train.db"
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select password from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)==0:
        db.commit()
        db.close()
        return 0
    if data[0][0]==hash(password):
        db.commit()
        db.close()
        return 1
    db.commit()
    db.close()
    return 2
    
#0 no such username
#1 success
def remove(username):
    f="sturdy-octo-train.db"
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    if len(data)==0:
        db.commit()
        db.close()
        return 0
    c.execute("delete from users where username='%s'"%(username))
    db.commit()
    db.close()
    return 1

def exists(username):
    f="sturdy-octo-train.db"
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    db.commit()
    db.close()
    return len(data)!=0

"""        
print register("homer","simpson",20,"blah@gmail.com")
print login('homer','simpson')
print login("homer","as")
print exists("homer")
print remove("homer")
print exists("homer")
"""
print get(1)
