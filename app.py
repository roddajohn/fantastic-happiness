from flask import Flask, render_template, request, redirect, url_for, session, flash
import utils, sqlite3
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
    if 'username' in session:
        return redirect(url_for("myFeed"))
    return render_template("login.html")

@app.route("/allStories")
def allFeed():
    if 'username' in session:
        stories = utils.story_manager.order_by_timestamp(True)
        stories.pop(0)
        return render_template("index.html",feed = stories)
    return redirect(url_for("mainpage"))
    
@app.route("/myStories")
def myFeed():
    if 'username' in session:
        userContributions = utils.user_manager.get(session['username']).posts_contributed_to
        if len(userContributions) == 0:
            return redirect(url_for("allFeed"))
        listContributionIDs = userContributions.split(",")
        stories = []
        for element in listContributionIDs:
            stories.append(utils.story_manager.get_story(int(element)))
        return render_template("myStories.html",feed = stories)
    return redirect(url_for("mainpage"))

@app.route("/fullPost/<int:postId>", methods=['GET'])
def fullPost(postId):
    if 'username' in session:
        #if(request.form['postID']): # want to put a checker if statement here but dont know how yet
        story = utils.story_manager.get_story(postID)
        return render_template("fullPost.html",post = story)
        #return redirect(url_for("myFeed"))
    return redirect(url_for("mainpage"))

@app.route("/latestUpdate/<int:postID>")
def latestUpdate(postID):
    if 'username' in session:
        #if(request.form['postID']): # want to put a checker if statement here but dont know how yet
        story = utils.story_manager.get_story(postID)
        return render_template("latestUpdate.html",post = story)
        #return redirect(url_for("allFeed"))
    return redirect(url_for("mainpage"))

@app.route("/rendercreate")
def renderCreate():
    return render_template("createPost.html")

@app.route("/createstory", methods=['POST'])
def createStory():
    if 'username' in session:
        if(request.form['story'] and request.form['title']):
            user = utils.user_manager.get(session['username'])
            story = utils.story_manager.create_story(request.form['title'],request.form['story'],user.user_id)
            flash("Story Created!")
            return redirect(url_for("myFeed"))
        flash("Fill in all fields!")
        return redirect(url_for("allFeed"))
    return redirect(url_for("mainpage"))

@app.route("/editPost", methods=['POST'])
def editPost():
    if 'username' in session:
        if(request.form['postID'] and request.form['edit']):
            user = utils.user_manager.get(session['username'])
            storiesCont = (user.posts_contributed_to).split(",")
            if(request.form['postID'] in storiesCont):
                flash("You've already contributed to this story!")
                return redirect(url_for("myFeed"))
            story = utils.story_manager.get_story(request.form['postID'])
            story.update_story(request.form['edit'],user.user_id)
            flash("Story updated!")
            return redirect(url_for("myFeed"))
        return redirect(url_for("allFeed"))
    return redirect(url_for("mainpage"))

@app.route("/login", methods=['POST'])
def authenticate():
    if 'username' in session:
        return redirect(url_for("mainpage"))
    if  request.form['username'] == '' or request.form['password'] == '':
        flash("Please fill in all fields!")
        return redirect(url_for("mainpage"))
    loginSuccess = utils.user_manager.login(request.form['username'],request.form['password'])
    if(loginSuccess == 0):
        flash("User does not exist!")
        return redirect(url_for("mainpage"))
    if(loginSuccess == 2):
        flash("Password is incorrect!")
        return redirect(url_for("mainpage"))
    if(loginSuccess == 1):
        session['username'] = request.form['username']

    return redirect(url_for("mainpage"))
    
@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    if not request.form or request.form['username'] == '' or request.form['password'] == '' or request.form['first']    == '' or request.form['last'] == '' or request.form['age'] == '' or request.form['email'] == '':
        flash("Please fill in all fields!")
        return redirect(url_for("mainpage"))
    if(request.form['password'] != request.form['confpass']):
        flash("Passwords must match!")
        return redirect(url_for("mainpage"))
    success = utils.user_manager.register(request.form['username'],request.form['password'],
                                          request.form['first'],request.form['last'],
                                          request.form['age'],request.form['email'])
    if(success == 1):
        flash("Success! : Please Sign In!")
        return redirect(url_for("mainpage"))
    if(success == 0):
        flash("Username already taken!")
        return redirect(url_for("mainpage"))

@app.route("/updateSettings", methods=['POST'])
def updateSettings():
    if 'username' in session:
        if not key in request.form:
            return render_template("settings.html")
        if(request.form['password'] != request.form['confpass']):
            flash("Passwords do not match! Settings not updated")
            return render_template("settings.html")
        user = utils.user_manager.get(session['username'])
        if not request.form['email'] == '':
            user.email = request.form['email']
        if not request.form['age'] == '':
            user.age = request.form['age']
        if not request.form['first'] == '':
            user.first = request.form['first']
        if not request.form['last'] == '':
            user.last = request.form['last']
        if not request.form['password'] == '':
            user.password = request.form['password']
        user.update()
        flash("Settings updated!")
        return render_template("settings.html")
    return redirect(url_for("mainpage"))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Successfully logged out!")
        return redirect(url_for("mainpage"))
    return redirect(url_for("mainpage"))
      
if __name__ == "__main__":
    app.debug = True
    app.run()
