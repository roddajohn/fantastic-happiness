import sqlite3

db = sqlite3.connect("sturdy-octo-train.db")
c = db.cursor()

class Story:
    story_id = 0
    title = ""
    latest_update = ""
    timestamp_latest_update = 0
    timestamp_created = 0
    contributed_to_by_user_ids = "0"

    def assign_id(self):
        c.execute("SELECT MAX(story_id)  FROM STORIES")
        fetched = c.fetchall()
        for row in fetched:
            last_id = row[0]
        story_id = last_id+1
        print story_id
        return story_id
    
    def create(self, title, text, timestamp, creator_id):
        self.story_id = self.assign_id()
        self.title = title
        self.latest_update = text
        self.timestamp_latest_update = timestamp
        self.timestamp_created = timestamp
        #self.contributed_to_by_user_ids = add_user(creator_id)
        c.execute("INSERT INTO stories VALUES ('"+str(self.story_id)+"','"+self.title+"','"+self.latest_update+"','"+str(self.timestamp_latest_update)+"','"+str(self.timestamp_created)+"','"+self.contributed_to_by_user_ids+"')")

test = Story()
test.create("pytest","pytest",0,0)

db.commit()
db.close()
