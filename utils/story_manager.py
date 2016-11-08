import sqlite3, time, os

class Story:
    story_id = -1
    title = ""
    latest_update = ""
    timestamp_latest_update = -1
    timestamp_created = -1
    contributed_to_by_user_ids = "-1"
    c = None
    
    #assigns an id to the story - works
    def assign_id(self):
        self.c.execute("SELECT MAX(story_id) FROM stories")
        fetched = self.c.fetchall()
        for row in fetched:
            last_id = row[0]
        if last_id == None:
            story_id = 0
        else:
            story_id = last_id+1
        return story_id

    #adds a user to the string of users with commas in between - works
    def add_user(self, user_id):
        if self.contributed_to_by_user_ids == "-1":
            self.contributed_to_by_user_ids = str(user_id)
        else:
            self.contributed_to_by_user_ids = self.contributed_to_by_user_ids+","+str(user_id)

    #returns full text of a story
    def full_text(self):
        return open("data/stories/"+str(self.story_id)+".txt","r").read()
               
    #updates the story's text file and latest_update/timestamp_latest_update/contributed_to_by_user_ids - works
    def update_story(self, text, userid, c_cur):
        self.timestamp_latest_update = get_timestamp()
        self.latest_update = text
        try:
            story_file = open("data/stories/"+str(self.story_id)+".txt","r+")
            story_file.write(story_file.read()+text)
        except IOError:
            story_file = open("data/stories/"+str(self.story_id)+".txt","w")
            story_file.write(text)
        self.add_user(userid)
        self.update_db(c_cur)

    #updates the db with the latest values - works
    def update_db(self, c_cur):
        c_cur.execute("UPDATE stories SET title ='%s', last_update ='%s', timestamp_last_update ='%s', timestamp_created ='%s', contributed_to_by_users ='%s' WHERE story_id = '%s'"%(self.title,self.latest_update,self.timestamp_latest_update,self.timestamp_created,self.contributed_to_by_user_ids,self.story_id))

    #updates the string of users that have contributed to this story
    def contribute(self,user_id):
        db = get_db()
        c = get_cursor(db)

        c.execute("select * from stories where story_id='%s'"%(self.story_id))
        data=c.fetchall()
        
        for row in data:
            if row[5] == "":
                new = str(user_id)
            elif str(user_id) not in row[5]:
                new = row[5]+","+str(user_id)
            else:
                new = row[5]
        
        c.execute("UPDATE stories SET contributed_to_by_users='%s' WHERE story_id='%s'"%(new, self.story_id))
        db_close(db)

        self.contributed_to_by_user_ids=new
        
    #initializes by setting all values to the given values - works
    def __init__(self, c = None, new = False, title = '', text = '', creator_id = -1):
        self.c = c
        self.story_id = self.assign_id()
        self.title = title
        self.latest_update = text
        self.timestamp_latest_update = get_timestamp()
        self.timestamp_created = get_timestamp()
        if new:
            self.update_story(text, creator_id, c)
            self.c.execute("INSERT INTO stories VALUES ('"+str(self.story_id)+"','"+self.title+"','"+self.latest_update+"','"+str(self.timestamp_latest_update)+"','"+str(self.timestamp_created)+"','"+self.contributed_to_by_user_ids+"')")


#####################################################################
# DO NOT MANUALLY CREATE STORY OBJECTS, INSTEAD USE THESE FUNCTIONS #
# ----------------------------------------------------------------- #
# create_story(title, text, creator_id)                             #
# get_story(story_id)                                               #
# delete_story(story_id) * ONLY ADMIN USAGE *                       #
# order_by_timestamp()                                              #
#####################################################################

def get_cursor(db):
    return db.cursor()

def get_db():
    return sqlite3.connect("data/sturdy-octo-train.db")

def db_close(db):
    db.commit()
    db.close()

#creates a new Story object with the given info and returns it - works
def create_story(title, text, creator_id):
    db = get_db()
    c = get_cursor(db)
    
    ret = Story(c, True, title, text, creator_id)
    ret.update_db(c)
    
    db_close(db)
    return ret

#returns a Story object by id populated from the database, even if that story doesn't exist - works
def get_story(story_id):
    db = get_db()
    c = get_cursor(db)
    
    ret = Story(c)
    ret.story_id = story_id
    c.execute("SELECT * FROM STORIES WHERE story_id = %s" %str(story_id))
    fetched = c.fetchall()
    for row in fetched:
        ret.title = row[1]
        ret.last_update = row[2]
        ret.timestamp_last_update = row[3]
        ret.timestamp_created = row[4]
        ret.contributed_to_by_user_ids = row[5]
        
    db_close(db)
    return ret

#deletes a story from the database and its corresponding text file by id - works
def delete_story(story_id):
    db = get_db()
    c = get_cursor(db)
    
    c.execute("DELETE FROM STORIES WHERE story_id = %s" %str(story_id))
    os.remove("data/stories/"+str(story_id)+".txt")

    db_close(db)

#returns a list of story objects ordered by timestamp (if last is True, order by latest update, if false, order by creation) - works
def order_by_timestamp(last):
    db = get_db()
    c = get_cursor(db)

    if last:
        c.execute("SELECT * FROM stories ORDER BY timestamp_last_update")
    else:
        c.execute("SELECT * FROM stories ORDER BY timestamp_created")
        
    ret = []
    
    fetched = c.fetchall()
    for row in fetched:
        ret.append(get_story(row[0]))

    db_close(db)

    ret.reverse()
    
    return ret

#prints a story (for debugging purposes) - works
def print_story(story):
    print("story_id: {0}, title: {1}, last_update: {2}, timestamp_last_update: {3}, timestamp_created: {4}, contributed_to_by_users: {5}".format(story.story_id,story.title,story.latest_update,str(story.timestamp_latest_update),str(story.timestamp_created),story.contributed_to_by_user_ids))

#updates a story given a Story object, text, and the user who wrote that text - works
def update_story(story, text, userid):
    db = get_db()
    c = get_cursor(db)

    story.update_story(text, userid, c)

    db_close(db)

#retrieves current time in UTC, seconds since epoch (Jan 1 1970) - works
def get_timestamp():
    return time.ctime(time.time())
