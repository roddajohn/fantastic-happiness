from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, os, utils.user_manager, utils.story_manager

app = Flask(__name__)
#creates instance of Flask and passes env variable __name__

app.secret_key = '\x1fBg\x9d\x0cLl\x12\x9aBb\xcd\x17\xb3/\xe4\xca\xf76!\xee\xf2\xc8?\x85\xdb\xd6;[\xae\xfb\xeb'

# Pages/routes
# mainpage: login form or feed
# settings: alter settings form
# my stories: could be feed
# full story
# logout: logout

@app.route("/")
def mainpage():
    if(session['username']):
        return redirect(url_for("myFeed"))
    return render_template("login_register.html")

@app.route("/allStories")
def allFeed():
    if(session['username']):
        stories = []
        
        db = utils.story_manager.get_db()
        c = utils.story_manager.get_cursor(db)
        
        #arbitrary number of stories
        #pls indlude as a function in story_manager.py
        c.execute("SELECT timestamp_latest_update,story_id FROM STORIES ORDER BY timestamp_latest_update LIMIT 10")
        fetched = c.fetchall()

        for(row in fetched):
            stories.append(utils.story_manager.get_story(int(row[0])))

        return render_template("feed.html",feed = stories)
    
    return redirect(url_for("mainpage"))
    
@app.route("/myStories")
def myFeed():
    if(session['username']):

        userContributions = utils.user_manager.get(session['username']).posts_contributed_to

        listContributionIDs = userContributions.split(",")
        stories = []

        for(element in listContributionIDs)
            stories.append(utils.story_manager.get_story(int(element)))

        return render_template("feed.html",feed = stories)
            
    return redirect(url_for("mainpage"))
    
@app.route("/login", methods=['POST'])
def authenticate():
    if(key in session):
        return redirect(url_for("mainpage"))
    if(!(key in request.form)         or
       request.form['username'] == '' or
       request.form['password'] == ''):
        return redirect(url_for("mainpage", message = "Please fill in all fields!"))
    loginSuccess = login(request.form['username'],request.form['password'])
    if(loginSuccess == 0):
        return redirect(url_for("mainpage", message = "User does not exist!"))
    if(loginSuccess == 2):
        return redirect(url_for("mainpage", message = "Password is incorrect!"))
    if(loginSuccess == 1):
        session['username'] = request.form['username']
        return redirect(url_for("mainpage"))

    return redirect(url_for("mainpage"))
    
@app.route("/register", methods=['POST'])
def register():
    if(key in session):
        return redirect(url_for("mainpage"))
    if(!(key in request.form)         or
       request.form['username'] == '' or
       request.form['password'] == '' or
       request.form['age']      == '' or
       request.form['email']    == ''):
        return redirect(url_for("mainpage", message = "Please fill in all fields!"))
    if(request.form['password'] != request.form['confpass'])
        return redirect(url_for("mainpage", message = "Passwords must match!"))
    success = utils.user_manager.register(request.form['username'],request.form['password'],
                                          request.form['age'],request.form['email'])
    if(success == 1):
        return redirect(url_for("mainpage", message = 'Success! : Please Sign In!'))
    if(success == 0):
        return redirect(url_for("mainpage", message = 'Username already taken!'))
    
@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for("mainpage", message = "Successfully logged out!"))
  

# @app.route("/login", methods=['POST'])
# def authenticate():
#     user = request.form['username']
#     pin = request.form['password']
#     shaHash = hashlib.sha1()
#     shaHash.update(pin)
#     pinHash = shaHash.hexdigest()
#     userslist = utils.authenticate.getUsers()
#     print pinHash
#     print userslist[user]
#     if (user in userslist):
#         if (userslist[user] == pinHash):
#             session[user] = app.secret_key
#             status['action'] = "success"
#             status['username'] = user
#             return redirect(url_for("mainpage"))
#         status['action'] = 'fail1'
#         return redirect(url_for("mainpage"))
#     status['action'] = "fail1"
#     return redirect(url_for("mainpage"))

# @app.route("/register", methods=['POST'])
# def register():
#     user = request.form["user"]
#     pin = request.form["pass"]
#     shaHash = hashlib.sha1()
#     shaHash.update(pin)
#     passHash = shaHash.hexdigest()
#     userslist = utils.authenticate.getUsers()
#     if (user.find(',') == -1 or user == '' or pin == ''):
#         status['action'] = 'fail3'
#         redirect(url_for("mainpage"))
#     if (user in userslist):
#         status['action'] = 'fail2'
#         return redirect(url_for("mainpage"))
#     utils.authenticate.addUser(user,passHash)
#     status['action'] = 'registered'
#     return redirect(url_for("mainpage"))

# @app.route("/logout", methods=['POST'])
# def byebye():
#     session.pop(status['username'])
#     status.pop('username')
#     status['action'] = 'logout'
#     return redirect(url_for('mainpage'))
    
if __name__ == "__main__":
    app.debug = True
    app.run()
