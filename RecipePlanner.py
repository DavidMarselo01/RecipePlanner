#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:57:37 2021

@author: davidn
"""
from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
import hashlib
import pymysql.cursors
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = "super secret key"
IMAGES_DIR = os.path.join(os.getcwd(), "images")

connection = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="",
                             db="RecipePlanner",
                             charset="utf8mb4",
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

#FIRST PAGE OF THE APP, LOGIN OR REGISTER
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("index.html")

#LOGGING IN

#This function is here to make sure that when a person is using our app, the user is always logged in
#So, we are checking if the session is ative and not just in the cookies
def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dec

#1. We click on the Register link in the index.html which will follow the route of /register, which will render register.html

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

#2. In register.html we fill out the form and the action is taken by the registerAuth()function
    #In the function we check if the user already exists and if not put the new user in the database

@app.route("/registerAuth", methods=["POST"])
def registerAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()
        firstName = requestData["firstName"]
        lastName = requestData["lastName"]
        
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO Person (username, password, firstName, lastName) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, hashedPassword, firstName, lastName))
        except pymysql.err.IntegrityError:
            error = "%s is already taken." % (username)
            return render_template('register.html', error=error)    

        return redirect(url_for("login"))

    error = "An error has occurred. Please try again."
    return render_template("register.html", error=error)

#3. Index.html - click on login
    
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

#4. In the login.html there is a form, the action is the loginAuth() fucntion
    #Check if the user is in the database and log in or not
    
@app.route("/loginAuth", methods=["POST"])
def loginAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()

        with connection.cursor() as cursor:
            queryLogin = "SELECT * FROM person WHERE username = %s AND password = %s"
            cursor.execute(queryLogin, (username, hashedPassword))
            
        data = cursor.fetchone()
        cursor.close()
        error = None
        if data:
            session["username"] = username
            #with connection.cursor() as cursor:
                #queryName = "SELECT firstName, lastName FROM person  WHERE username = %s AND password = $s"
                #cursor.execute(queryName, (username, hashedPassword))
            #dataName = cursor.fetchone()
            #session["nameOfPerson"] = str(dataName)
            #cursor.close()
            return redirect(url_for("home"))

        error = "Incorrect username or password."
        return render_template("login.html", error=error)

#5. Log out

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username")
    return redirect("/")

#HOME PAGE WHERE THE USER DOES ALL OF THE ACTIONS

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username = session['username'])

if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run('127.0.0.1', 5000, debug = True)
    
    
#EVERYTHING TO DO WITH IMAGES (UPLOAD AND SEE YOU IMAGES OR IMAGES OF YOUR FRIENDS)

#1. Render the upload.html, in which we have a form with an action to go the 
    #/uploadImage path with method post