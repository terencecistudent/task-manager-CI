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


# used the find function with MongoDB to fetch our categories.
@app.route("/add_task")
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())


# use POST method to deliver form data
# go back to mongo and get the task collections (line 33)
# insert_one request form and coverting form to dict (line 35)
@app.route("/insert_track", methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))


# want to find one particular task from our task collections - parameter will pass ID in (line 42)
# we need is a list of the collections (line 43)
@app.route("/edit_task/<task_id>")
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)



if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
