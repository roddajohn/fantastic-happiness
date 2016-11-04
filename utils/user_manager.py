import hashlib
import sqlite3

f="./..data/sturdy-octo-train.db"


class User:
    user_id=0
    username=""
    password=""
    first=""
    last=""
    age=0
    email=""
    posts_contributed_to=""

    #change password then use this to update it
    def update_pw(self):
        db=sqlite3.connect(f)
        c=db.cursor()
        c.execute("update users set password='%s' where user_id=%d"%(hash(self.password),self.user_id))
        self.password=hash(self.password)
        db.commit()
        db.close()

    #updates everything except password
    def update(self):
        db=sqlite3.connect(f)
        c=db.cursor()
        c.execute("update users set username='%s',first='%s',last='%s',age=%d,email='%s', posts_contributed_to='%s' where user_id=%d"%(self.username,self.first,self.last,self.age,self.email,self.posts_contributed_to,self.user_id))
        db.commit()
        db.close()
               
def hash(unhashed):
    mho=hashlib.sha1()
    mho.update(unhashed)
    return mho.hexdigest()

#input is username
def get(un):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select * from users where username='%s'"%(un))
    data=c.fetchall()
    user=User()
    user.username=un
    user.user_id=data[0][0]
    user.password=data[0][2]
    user.first=data[0][3]
    user.last=data[0][4]
    user.age=data[0][5]
    user.email=data[0][6]
    user.posts_contributed_to=data[0][7]
    db.commit()
    db.close()
    return user

#0 username exists
#1 success
def register(username,password,first,last,age,email):
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
    c.execute("insert into users values ('%d','%s','%s','%s','%s','%d','%s','')"%(len(data)+1,username,hash(password),first,last,age,email))
    db.commit()
    db.close()
    return 1

#0 no such username
#1 success
#2 wrong password
def login(username,password):
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

#self explanatory
def exists(username):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute("select user_id from users where username='%s'"%(username))
    data=c.fetchall()
    db.commit()
    db.close()
    return len(data)!=0
