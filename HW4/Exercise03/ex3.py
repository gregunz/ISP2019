#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

# SCHEMA: messages (name, message)
## This method returns a list of messages in a json format such as
## [
##  { "name": <name>, "message": <message> },
##  { "name": <name>, "message": <message> },
##  ...
## ]
## If this is a POST request and there is a parameter "name" given, then only
## messages of the given name should be returned.
## If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages",methods=["GET","POST"])
def messages():
    with db.cursor() as cursor:
        sql = "SELECT name,message FROM messages"
        if request.method=="POST":
            name = request.form.get("name")
            if name is not None and name is not "":
                sql+=" WHERE name = %s"
                cursor.execute(sql, name)
            else:
                return 'an error occured', 500
        if request.method=="GET":
            cursor.execute(sql)

        results = cursor.fetchall()
        json = [{'name':name, 'message':message} for name, message in results]
        return jsonify(json),200

# SCHEMA: users (name,password)
## This method returns the list of users in a json format such as
## { "users": [ <user1>, <user2>, ... ] }
## This methods should limit the number of users if a GET URL parameter is given
## named limit. For example, /users?limit=4 should only return the first four
## users.
## If the paramer given is invalid, then the response code must be 500.
@app.route("/users",methods=["GET"])
def contact():
    with db.cursor() as cursor:
        sql = "SELECT name FROM users"
        limit = request.args.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                return 'an error occured', 500
            sql += ' LIMIT %s'
            cursor.execute(sql, limit)
        else:
            cursor.execute(sql)
        results = cursor.fetchall()
        json = {'users': [row[0] for row in results]}
        return jsonify(json),200

if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                username,
                password,
                database)
    with db.cursor() as cursor:
        populate.populate_db(seed,cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0',port=80)