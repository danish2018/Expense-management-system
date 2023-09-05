from flask import Blueprint,request,flash,render_template,redirect,url_for
from werkzeug.security import generate_password_hash ,check_password_hash
from . models import User
from flask_login import login_user,logout_user,login_required
from . import db


authentication = Blueprint('authentication',__name__)

@authentication.route("/signup",methods = ["GET","POST"])
def Signup():
    
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        contact = request.form.get('contact')

        email_exist = User.query.filter_by(email = email).first()
        user_exist = User.query.filter_by(username = username).first()
        if email_exist:
            flash("Email already exist",category = 'error')
        elif user_exist:
            flash("User already exist", category = 'error')
        elif password1 !=password2:
            flash("Paswword does not match",category='error')
        elif len(contact)<10:
            flash('Invalid contact',category='error')
        else:
            new_user = User(email = email ,username = username ,password = generate_password_hash(password1 , method = 'sha256'), contact = contact)
            db.session.add(new_user)
            db.session.commit()
            flash('User Created !! You can login now..')
            return redirect(url_for('authentication.login'))
    return render_template('signup.html')
    
@authentication.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in ',category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('Password Incorrect',category='error')
        else:
            flash('Email does not exist',category='error')
        
    return render_template('login.html')




# @app.route("/profile/<id>",methods = ["GET","POST"])
# def profile(id):
#     user = User.query.filter_by(id=id).first()
#     if user:
#         email = user.email
#         username = user.username
#     return redirect('/')


    
@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    remember_me= False
    return redirect(url_for('views.home'))