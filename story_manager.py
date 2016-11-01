class Story:
    story_id = 0
    title = ""
    latest_update = ""
    timestamp_latest_update = 0
    timestamp_created = 0
    contributed_to_by_user_ids = ""

    def create(title, text, timestamp, creator_id):
        self.title = title
        self.latest_update = text
        self.timestamp_latest_update = timestamp
        self.timestamp_created = timestamp
        self.contributed_to_by_user_ids = ""+creator_id
