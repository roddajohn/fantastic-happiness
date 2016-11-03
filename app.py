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
    if(session['uid']):
        session['feedType'] = 'all';
        return redirect(url_for("feed"))
    return render_template("login_register.html")

@app.route("/allStories")
def allFeed():
    if(session['uid']):
        
    return redirect(url_for("mainpage"))
    

@app.route("/myStories")
def myFeed():
    if(session['uid']):

        userContributions = utils.user_manager.get(session['uid']).posts_contributed_to

        listContributionIDs = userContributions.split(",")
        stories = []

        for(element in listContributionIDs)
            stories.append(utils.story_manager.get_story(int(element)))
        # if(session['feedType'] == 'all'):
        #     # gets dictionary of story objects sorted by time
        # if(session['feedType'] == 'my'):
        #     # gets dictionary of story objects based on user database field "stories contributed to"

        ## figure out how to differentiate between all stories and my stories depending on which navbar option clicked
            
    return redirect(url_for("mainpage"))
    
@app.route("/login", methods=['POST'])
def authenticate():
    # on success: redirect to feed, set feedType to my
    # on failure: kick to mainpage with message "not authenticated"
    
@app.route("/register", methods=['POST'])
def register():
    if(key in session):
        return redirect(url_for("mainpage"))
    if(!(key in request.form)         or
       request.form['username'] == '' or
       request.form['password'] == '' or
       request.form['age']      == '' or
       request.form['email']    == '')
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
    session.pop('feedType')
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
