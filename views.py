from models import *
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, abort
from flask import make_response, flash
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc, asc
import datetime
import requests
import sys
import random
import string
import codecs
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
# connecting database
engine = create_engine('sqlite:///problems.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read()['web']['client_id']
APPLICATION_NAME = "Hostel Feedback"
# for login


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        if session.query(User).filter_by(name=username).first() == username:
            if verify_password(password):
                return redirect(url_for('hostelfeedback'))
        else:
            flash("Invalid login Credentials! You can signup if you don't have an account.")
            return render_template("newlogin.html")
    else:
        return render_template('newlogin.html')


# to show ratings to the warden
@app.route('/rating')
def rating():
    feedback = session.query(Feedback).all()
    return render_template('ratings.html', feedback=feedback)


@app.route('/signup', methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            flash("Invalid Password or Username")
        if session.query(User).filter_by(name=username).first() is not None:
            flash("Username already exists! Try something different")
        user = User(name=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("Succesfully signed up")
        return render_template('newlogin.html')
    else:
        print  "hello"
        return render_template('signup.html')


# stores ratings of the feedback to the database
@app.route('/categories/<int:categories_id>/feedback/<int:feedback_id>/someview', methods=['GET', 'POST'])
def someview(categories_id, feedback_id):
    if request.method == 'POST':
        if request.form['mess1']:
            answer1 = request.form['mess1']
        if request.form['mess2']:
            answer2 = request.form['mess2']
        if request.form['mess3']:
            answer3 = request.form['mess3']
        if request.form['mess4']:
            answer4 = request.form['mess4']
        if request.form['mess5']:
            answer5 = request.form['mess5']
        feedback = session.query(Feedback).filter_by(id=feedback_id).one()
        feedback.totalrating = feedback.totalrating + \
            int(answer5) + int(answer4) + \
            int(answer3) + int(answer2) + int(answer1)
        feedback.rating1 = feedback.rating1 + 25
        print feedback.totalrating
        return render_template('home.html')


# logout the user
@app.route('/logout')
def logout():
    return render_template('newlogin.html')


# hostelfeedback warden shows the home page for warden
@app.route('/hostelfeedbackwarden')
def hostelfeedbackwarden():
    categories = session.query(Categories).all()
    return render_template(
        'wardenhome.html')

# home page for students


@app.route('/hostelfeedback')
def hostelfeedback():
    categories = session.query(Categories).all()
    return render_template(
        'home.html')

# shows feedback page according to category to warden


@app.route('/hostelfeedback/<int:categories_id>/feedbackwarden', methods=['GET', 'POST'])
def feedbackwarden(categories_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    if request.method == 'POST':
        for i in range(1, 6):
            rating = request.form['mess%d' % (i,)]
            print rating
        return redirect(url_for('hostelfeedbackwarden'))
    else:
        if categories_id == 1:
            return render_template('messfeedbackwarden.html', category=category, feedback_id=1)
        elif categories_id == 2:
            return render_template('hostelfeedbackwarden.html', category=category, feedback_id=2)
        elif categories_id == 3:
            return render_template('wardenfeedbackwarden.html', category=category, feedback_id=3)
        elif categories_id == 4:
            return render_template('foodfeedbackwarden.html', category=category, feedback_id=4)
        elif categories_id == 5:
            return render_template('medicalfeedbackwarden.html', category=category, feedback_id=5)


# shows feedback page according to category
@app.route('/hostelfeedback/<int:categories_id>/feedback', methods=['GET', 'POST'])
def feedback(categories_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    if request.method == 'POST':
        for i in range(1, 6):
            rating = request.form['mess%d' % (i,)]
            print rating
        return redirect(url_for('hostelfeedback'))
    else:
        if categories_id == 1:
            return render_template('messfeedback.html', category=category, feedback_id=1)
        elif categories_id == 2:
            return render_template('hostelfeedback.html', category=category, feedback_id=2)
        elif categories_id == 3:
            return render_template('wardenfeedback.html', category=category, feedback_id=3)
        elif categories_id == 4:
            return render_template('foodfeedback.html', category=category, feedback_id=4)
        elif categories_id == 5:
            return render_template('medicalfeedback.html', category=category, feedback_id=5)


# show comments to warden
@app.route('/hostelfeedbackwarden/<int:categories_id>/feedbackwarden/<int:feedback_id>/commentswarden', methods=['GET', 'POST'])
def commentswarden(categories_id, feedback_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    comments = session.query(Comments).all()
    return render_template('commentwarden.html', category=category, comments=comments, feedback=feedback_id)


# comment and view comments
@app.route('/hostelfeedback/<int:categories_id>/feedback/<int:feedback_id>/comments', methods=['GET', 'POST'])
def comments(categories_id, feedback_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    comments = session.query(Comments).all()
    if request.method == 'POST':
        comment = Comments(
            commentdata=request.form['commentdata'], categories_id=categories_id)
        session.add(comment)
        session.commit()
        flash("Your Comment has been added!")
        return redirect(url_for('comments', categories_id=category.id, feedback_id=feedback_id))
    else:
        return render_template('comment.html', category=category, comments=comments, feedback=feedback_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
