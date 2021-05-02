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
                             password="Marselo01",
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
            queryLogin = "SELECT * FROM Person WHERE username = %s AND password = %s"
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

#Pantry
def getPantry():
    query = "SELECT ingredient_name, username, quantity, measure_unit FROM Pantry"
    with connection.cursor() as cursor:
        cursor.execute(query)
    cursor.close()
    dataPantry = cursor.fetchall()
    return dataPantry

def editPantryIngr(username, ingredient_name, quantity):
    query = "UPDATE Pantry SET quantity = %s WHERE username = %s AND ingredient_name = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (quantity, username, ingredient_name))
    cursor.close()
    
def deletePantryIngr(username, ingredient_name):
    query = "DELETE FROM Pantry WHERE username = %s AND ingredient_name = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (username, ingredient_name))
    cursor.close()
@app.route('/myPantry', methods=["GET"])
def myPantry():
    dataPantry = getPantry()
    username = session['username']
    return render_template('myPantry.html', dataPantry = dataPantry, 
                           username = username)

def quantityCheck(quantity):
    #Check that quantity is a number, otherwise output an error to the user
    if quantity.isdigit() and int(quantity):
        quantity = int(quantity)
    else:  
        try:
            quantity = float(quantity)
        except Exception:
            editIngrErrorStr = "You can only input numbers in the quantity field"
            return (False, editIngrErrorStr)
        
    #Check that quantity is >= 0, otherwise output an error to the user
    if quantity < 0:
        editIngrErrorNeg = "You can only input positive numbers in the quanitity field"
        return (False, editIngrErrorNeg)
    else:
        return (True, quantity)

@app.route('/editIngredient', methods=["POST"])
def editIngredient():
    if request.form:
        #Get all the data from the form that was submitted in myPantry.html
        data = request.form
        username = data["username"]
        ingredient_name = data["ingredient_name"]
        measure_unit = data["measure_unit"] 
        quantity = data["quantity"]
        
        checkQuant = quantityCheck(quantity)
        if checkQuant[0] == False:  
            editIngrError = checkQuant[1]
            dataPantry = getPantry()
            return render_template('myPantry.html', dataPantry = dataPantry,
                               editIngrError = editIngrError,
                               username = username)
        elif checkQuant[0] == True:
            editPantryIngr(username, ingredient_name, checkQuant[1])
            dataPantry = getPantry()
            return render_template('myPantry.html', dataPantry = dataPantry, 
                                   username = username)
    
@app.route('/deleteIngredient', methods=["POST"])
def deleteIngredient():
    if request.form:
        data = request.form
        username = data["username"]
        ingredient_name = data["ingredient_name"]
        deletePantryIngr(username, ingredient_name)
        dataPantry = getPantry()
        return render_template('myPantry.html', dataPantry = dataPantry,
                                username = username)

#Add Ingredients
#Select all the ingredient names and their measure unit
def getAllIngredients():
    query = "SELECT ingredient_name, measure_unit FROM Ingredients"
    with connection.cursor() as cursor:
        cursor.execute(query)
    cursor.close()
    dataAllIngredients = cursor.fetchall()
    return dataAllIngredients

def insertIntoPantry(ingredient_name, username, quantity, measure_unit):
    query = "INSERT INTO Pantry (ingredient_name, username, quantity, measure_unit) VALUES (%s, %s, %s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(query, (ingredient_name, username, quantity, measure_unit))
    cursor.close()
    
def checkIfIngrInPantry(ingredient_name, username):
    query = "SELECT quantity FROM Pantry WHERE ingredient_name = %s AND username = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (ingredient_name, username))
    cursor.close()
    itemPantry = cursor.fetchall()
    if (itemPantry):
        return True
    else:
        return False

def getQuantityIngrPantry(ingredient_name, username):
    query = "SELECT quantity FROM Pantry WHERE ingredient_name = %s AND username = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (ingredient_name, username))
    cursor.close()
    itemPantry = cursor.fetchall()
    return itemPantry

@app.route('/ingredients', methods=["GET"])
def ingredients():
    dataAllIngredients = getAllIngredients()
    return render_template('ingredients.html', dataAllIngredients = dataAllIngredients)

@app.route("/addIngredient", methods=["POST"])
def addIngredient():
    if request.form:
        #Get all the data from the form submitted in ingredients.html
        data = request.form
        quantity = data["quantity"]
        ingredient_name = data["ingredient_name"]
        measure_unit = data["measure_unit"]
        username = session['username']
        
        checkQuant = quantityCheck(quantity)
        if checkQuant[0] == False:  
            quantityError = checkQuant[1]
            dataAllIngredients = getAllIngredients()
            return render_template('ingredients.html', 
                                   dataAllIngredients = dataAllIngredients,
                                   quantityError = quantityError,
                                   username = username)
        elif checkQuant[0] == True:
            dataAllIngredients = getAllIngredients()
            if (checkIfIngrInPantry(ingredient_name, username) == False):
                insertIntoPantry(ingredient_name, username, quantity, measure_unit)
                successAdded = quantity + " " + str(measure_unit) + " of " + ingredient_name + " added to your Pantry"
                return render_template('ingredients.html', dataAllIngredients = dataAllIngredients, successAdded = successAdded)
            elif (checkIfIngrInPantry(ingredient_name, username) == True):
                quantityPrev = getQuantityIngrPantry(ingredient_name, username)
                print(quantityPrev)
                quantityPrev = quantityPrev[0]["quantity"]
                quantity = float(quantity)
                quantity += float(quantityPrev)
                successAdded = ingredient_name + " " + "was updated from " + quantityPrev + " " + str(measure_unit) + " to " + str(quantity) + " " + measure_unit
                editPantryIngr(username, ingredient_name, quantity)
                return render_template('ingredients.html', 
                                       dataAllIngredients = dataAllIngredients, 
                                       successAdded = successAdded)
                


if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run('127.0.0.1', 8080, debug = True)
    
    
#EVERYTHING TO DO WITH IMAGES (UPLOAD AND SEE YOU IMAGES OR IMAGES OF YOUR FRIENDS)

#1. Render the upload.html, in which we have a form with an action to go the 
    #/uploadImage path with method post
