from flask import Flask, render_template, request, redirect, url_for, session, flash
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
        stories = utils.story_manager.order_by_timestamp(True)
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

@app.route("/fullPost", methods=['POST'])
def fullPost():
    if(session['username']):
        if(request.form['postID']):
            story = utils.story_manager.get_story(request.form['postID'])
            return render_template("fullPost.html",post = story)
        return redirect(url_for("myFeed"))
    return redirect(url_for("mainpage"))

@app.route("/latestUpdate")
def latestUpdate():
    if(session['username']):
        if(request.form['postID']):
            story = utils.story_manager.get_story(request.form['postID'])
            return render_template("latestUpdate.html",post = story)
        return redirect(url_for("allFeed"))
    return redirect(url_for("mainpage"))

@app.route("/editPost")
def editPost():
    if(session['username']):
        if(request.form['postID'] and request.form['edit']):
            user = utils.user_manager.get(session['username'])
            story = utils.story_manager.get_story(request.form['postID'])
            story.update_story(request.form['edit'],user.user_id)
            flash("Story updated!")
            return redirect(url_for("myFeed"))
        return redirect(url_for("allFeed"))
    return redirect(url_for("mainpage"))

@app.route("/login", methods=['POST'])
def authenticate():
    if(key in session):
        return redirect(url_for("mainpage"))
    if(!(key in request.form)         or
       request.form['username'] == '' or
       request.form['password'] == ''):
        flash("Please fill in all fields!")
        return redirect(url_for("mainpage"))
    loginSuccess = login(request.form['username'],request.form['password'])
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
    if(key in session):
        return redirect(url_for("mainpage"))
    if(!(key in request.form)         or
       request.form['username'] == '' or
       request.form['password'] == '' or
       request.form['first']    == '' or
       request.form['last']     == '' or
       request.form['age']      == '' or
       request.form['email']    == ''):
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

@app.route("/updateSettings")
def updateSettings():
    if(session['username']):
        if(!(key in request.form)):
            return render_template("settings.html")
        if(request.form['password'] != request.form['confpass']):
            flash("Passwords do not match! Settings not updated")
            return render_template("settings.html")
        user = utils.user_manager.get(session['username'])
        if(!(request.form['email'] == '')):
            user.email = request.form['email']
        if(!(request.form['age'] == '')):
            user.age = request.form['age']
        if(!(request.form['first'] == '')):
            user.first = request.form['first']
        if(!(request.form['last'] == '')):
            user.last = request.form['last']
        if(!(request.form['password'] == ''):
            user.password = request.form['password']
        user.update()
        flash("Settings updated!")
        return render_template("settings.html")
    return redirect(url_for("mainpage"))

@app.route("/logout")
def logout():
    if(session['username']):
        session.pop('username')
        flash("Successfully logged out!")
        return redirect(url_for("mainpage"))
    return redirect(url_for("mainpage"))
      
if __name__ == "__main__":
    app.debug = True
    app.run()
