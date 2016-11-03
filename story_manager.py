import sqlite3, time

class Story:
    story_id = -1
    title = ""
    latest_update = ""
    timestamp_latest_update = -1
    timestamp_created = -1
    contributed_to_by_user_ids = "-1"
    c = None
    
    #assigns an id to the story
    def assign_id(self):
        self.c.execute("SELECT MAX(story_id)  FROM STORIES")
        fetched = self.c.fetchall()
        for row in fetched:
            last_id = row[0]
        story_id = last_id+1
        return story_id

    #adds a user to the string of users with commas in between
    def add_user(self, user_id):
        self.contributed_to_by_user_ids = self.contributed_to_by_user_ids+","+str(user_id)

    #retrieves current time in UTC, seconds since epoch (Jan 1 1970)
    def get_timestamp(self):
        return time.time()
        
    #updates the story's text file and latest_update/timestamp_latest_update/contributed_to_by_user_ids
    def update_story(self, text, userid):
        self.timestamp_latest_update = self.get_timestamp()
        self.latest_update = text
        story_file = open(str(self.story_id)+".txt","r+")
        story_file.write(story_file.read()+text)
        self.add_user(user_id)
        self.update(db)

    #updates the db with the latest values
    def update_db(self):
        c.execute("UPDATE stories SET title = %s , last_update = %s , timestamp_last_update = %s , timestamp_created = %s , contributed_to_by_users = %s WHERE story_id = %s" %title %last_update %timestamp_last_update %timestamp_created %contributed_to_by_user_ids %story_id)
        
    #initializes by setting all values to the given values
    def __init__(self, c = None, new = False, title = '', text = '', timestamp = -1, creator_id = -1):
        self.c = c
        self.story_id = self.assign_id()
        self.title = title
        self.latest_update = text
        self.timestamp_latest_update = timestamp
        self.timestamp_created = timestamp
        self.contributed_to_by_user_ids = str(creator_id)
        if new:
            self.c.execute("INSERT INTO stories VALUES ('"+str(self.story_id)+"','"+self.title+"','"+self.latest_update+"','"+str(self.timestamp_latest_update)+"','"+str(self.timestamp_created)+"','"+self.contributed_to_by_user_ids+"')")


#####################################################################
# DO NOT MANUALLY CREATE STORY OBJECTS, INSTEAD USE THESE FUNCTIONS #
# ----------------------------------------------------------------- #
# create_story(title, text, timestamp, creator_id)                  #
# get_story(story_id)                                               #
# delete_story(story_id) * ONLY ADMIN USAGE *                       #
#####################################################################

def get_cursor(db):
    return db.cursor()

def get_db():
    return sqlite3.connect("sturdy-octo-train.db")

def db_close(db):
    db.commit()
    db.close()

#creates a new Story object with the given info and returns it
def create_story(title, text, timestamp, creator_id):
    db = get_db()
    c = get_cursor(db)
    
    ret = Story(c, True, title, text, timestamp, creator_id)
    ret.update_db()
    
    db_close(db)
    return ret

#returns a Story object by id populated from the database, even if that story doesn't exist
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

#deletes a story from the database by id
def delete_story(story_id):
    db = get_db()
    c = get_cursor(db)
    
    c.execute("DELETE FROM STORIES WHERE story_id = %s" %str(story_id))

    db_close(db)
