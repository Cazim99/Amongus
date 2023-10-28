from __init__ import CONFIGURATIONS, PATCH_LIST, inputs_rules, inputs_rules_update

from flask import send_file
from flask import Flask, render_template, request, redirect, flash, session
import secrets
import os, sys

sys.path.append(os.path.abspath(os.path.join('..')))
from db import DBengine
from db.Users import Users
from methods.form import check_form, is_submited

# -------------------- CONFIGURATIONS 
SERVER_CONFIGURATION = CONFIGURATIONS['server']['items']
DBengine.DB_CONFIG = CONFIGURATIONS['database']['items']
# -------------------- CONFIGURATIONS 

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

"""@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)"""

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", 
                           patchs=PATCH_LIST, 
                           gm_download_link=SERVER_CONFIGURATION['game_download_link'],
                           session=session
                           )

@app.route('/download')
def download():
    return send_file('config.ini',as_attachment=True)

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('logged_in')
        session.pop('username')
    return home()

@app.route("/psettings")
def settings():
    if 'logged_in' not in session:
        return redirect('home')

    user = Users.by_username(session['username'])
        
    if user == None:
        flash("User not found!","is-danger")
        return redirect("home")
    else:
        return render_template("profile.html", title=user['username'], userinfo=user, gm_download_link=SERVER_CONFIGURATION['game_download_link'])

@app.route("/profile")
def profile():
    user = None 
    if 'username' in request.args:
        user = Users.by_username(request.args['username'])
        if user == None:
            flash("User not found!","is-danger")
            return redirect('home')
    elif 'username' not in request.args:
        return redirect('home')
        
    userinfo = {
        'full_name':user['full_name'],
        'username':user['username'],
        'email':user['email'],
    }
    return render_template("profile.html", title=user['username'], userinfo=userinfo, gm_download_link=SERVER_CONFIGURATION['game_download_link'])

@app.route("/updateprofile",methods=['GET','POST'])
def updateprofile():
    if 'logged_in' not in session:
        return redirect('home')
        
    if is_submited(request.form):
        if check_form(request.form, inputs_rules_update):
            new_user = {}
            for value in inputs_rules_update.keys():
                new_user[value] = request.form[value]
            error_message = Users.update(new_user)
            if error_message is None:
                flash("Account succesfully updated", "is-success")
                return render_template("profile.html", title=new_user['username'], userinfo=new_user, gm_download_link=SERVER_CONFIGURATION['game_download_link'])
            else:
                flash(error_message, "is-danger")
        return redirect('psettings')
    else:
        return redirect('home')

@app.route("/about")
def about():
    return render_template("about.html", title="about", gm_download_link=SERVER_CONFIGURATION['game_download_link'])

# sign-up-application?full_name=App%20Test&username=AppTest&email=AppTest@a&password=AppTest12345&confirm-password=AppTest12345
@app.route("/sign-up-application", methods=['GET','POST'])
def register_application():
    if request.headers['User-Agent'].count("Windows"):
        return "404 Page not found!"
    
    respond = {
            "message":"",
            "status-code":None,
    }
    
    form = check_form(request.args, inputs_rules, fromApplication=True)
    if form is True:
        new_user = {}
        for value in request.args:
            new_user[value] = request.args[value]
        error_message = Users.create_user(new_user)
        if error_message is None:
            respond['message'] = "Account succesfully created, you can login now"
            respond['status-code'] = 200
            return respond
        else:
            respond['message'] = error_message
            respond['status-code'] = 422
            return respond
    else:
        return form
    
@app.route("/login-application", methods=['GET','POST'])
def login_application():
    if request.headers['User-Agent'].count("Windows"):
        return "404 Page not found!"
    
    if 'email' in request.args and 'password' in request.args:
        respond = {
            "message":"",
            "status-code":None,
            "user":None,
        }
        
        user = Users.by_email(request.args['email'])
        if user:
            if user['password'] == request.args['password']:
                if user['baned'] == 1:
                    respond['user'] = None
                    respond['message'] = f"You are banned"
                    respond['status-code'] = 422 # Unsuported entry 
                    return respond  
                respond['user'] = str(user)
                respond['message'] = f"Wellcome {user['username']}"
                respond['status-code'] = 200
                return respond
            
        respond['user'] = None
        respond['message'] = f"Invalid credentials, try again !"
        respond['status-code'] = 422 # Unsuported entry
        return respond

@app.route("/sign-up", methods=['GET','POST'])
def register():
    if 'logged_in' in session:
        return redirect('home')
    
    if is_submited(request.form):
        if check_form(request.form, inputs_rules):
            new_user = {}
            for value in inputs_rules.keys():
                new_user[value] = request.form[value]
            error_message = Users.create_user(new_user)
            if error_message is None:
                flash("Account succesfully created, you can login now", "is-success")
                return redirect("login")
            else:
                flash(error_message, "is-danger")
        return redirect("sign-up")
    
    return render_template("sign-up.html", title="Sign up", patchs=PATCH_LIST, gm_download_link=SERVER_CONFIGURATION['game_download_link'])

@app.route("/reportissue")
def report_an_issue():
    return render_template("report-an-issue.html", title="Report an issue", gm_download_link=SERVER_CONFIGURATION['game_download_link'])

@app.route("/login",methods=['GET','POST'])
def login():
    if 'logged_in' in session:
        return redirect('home')
    
    if is_submited(request.form):
        if 'email' in request.form and 'password' in request.form:
            user = Users.by_email(request.form['email'])
            if user:
                if user['password'] == request.form['password']:
                    flash(f"Wellcome {user['username']}", "is-info")
                    session['logged_in'] = True
                    session['username'] = user['username']
                    return redirect("home")
                
            flash(f"Invalid credentials, try again !", "is-danger")
            return redirect("login")
    
    return render_template("login.html", title="Login", patchs=PATCH_LIST, gm_download_link=SERVER_CONFIGURATION['game_download_link'])

if __name__ == "__main__":
    app.run(SERVER_CONFIGURATION['host'], SERVER_CONFIGURATION['port'] ,debug=SERVER_CONFIGURATION['debug'])

