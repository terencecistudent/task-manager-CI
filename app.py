import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGODB_NAME"] = os.environ.get('MONGODB_NAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

DBS_NAME = "task_manager"


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route("/add_task")
def add_task():
    return render_template("addtask.html")


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
