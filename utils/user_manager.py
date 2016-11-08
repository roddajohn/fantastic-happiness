import hashlib
import sqlite3

f="data/sturdy-octo-train.db"


class User:
    user_id=0
    username=""
    password=""
    first=""
    last=""
    age=0
    email=""
    posts_contributed_to=""
    permissions=""


    def add_post_contributed_to(self,post):
        self.posts_contributed_to+=","+post

    def remove_post_contributed_to(self,post):
        posts=self.posts_contributed_to.split(',')
        self.posts_contributed_to=""
        for i in posts:
            if i!=post:
                self.posts_contributed_to+=i

    def add_permission(self,perm):
        self.permissions+=","+perm

    def remove_permission(self,perm):
        perms=self.permissions.split(',')
        self.permissions=""
        for i in perms:
            if i!=perm:
                self.permissions+=i

    def check_permission(self, perm):
        perms=self.permissions.split(',')
        return perm in perms

    #change password then use this to update it
    def update_pw(self):
        db=sqlite3.connect(f)
        c=db.cursor()
        c.execute("update users set password='%s' where user_id=%d"%(hash(self.password),self.user_id))
        self.password=hash(self.password)
        db.commit()
        db.close()
        
    def contribute(self,story_id):
        db=sqlite3.connect(f)
        c=db.cursor()

        c.execute("select * from users where username='%s'"%(self.username))
        data=c.fetchall()
        
        for row in data:
            if row[7] == "":
                new = str(story_id)
            else:
                new = row[7]+","+str(story_id)
    
        c.execute("UPDATE users SET posts_contributed_to='%s' WHERE username='%s'"%(new, self.username))
        db.commit()
        db.close()

        self.posts_contributed_to=new

    #updates everything except password
    #user after adding/removing permissions/posts_contributed_to and after changing any user properties except 4 password
    def update(self):
        db=sqlite3.connect(f)
        c=db.cursor()
        c.execute("update users set username='%s',first='%s',last='%s',age=%d,email='%s',posts_contributed_to='%s',permissions='%s' where user_id=%d"%(self.username,self.first,self.last,self.age,self.email,self.posts_contributed_to,self.permissions,self.user_id))
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
    user.permissions=data[0][8]
    db.commit()
    db.close()
    return user

#0 username exists
#1 success
#2 blank field
#3 bad password: not enough chars
#4 bad password: no lowercase letters
#5 bad password: no uppercase letters
#6 bad password: no numbers
#7 age not int
#9 4,5
#10 4,6
#11 5,6
def register(username,password,first,last,age,email):
    if username=="" or password=="" or first=="" or last=="" or email=="" or age==0:
        return 2
    
    badPw = 0
    lower = False
    upper = False
    num = False
    for letter in password:
        if letter is letter.lower():
            lower = True
        if letter is letter.upper():
            upper = True
        try:
            hold = int(letter)
            num = True
        except:
            hold = 0

    if not lower:
        badPw+=4
    if not upper:
        badPw+=5
    if not num:
        badPw+=6
            
    if len(password) < 6:
        badPw=3

    if badPw > 0:
        return badPw
        
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
    try:
        c.execute("insert into users values ('%d','%s','%s','%s','%s','%d','%s','','')"%(len(data)+1,username,hash(password),first,last,int(age),email))
    except ValueError:
        return 7
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
