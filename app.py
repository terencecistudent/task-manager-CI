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


# We pass in the task ID because that's our hook into the primary key.
# Call the update function, We specify the ID. That's our key to uniqueness (line 54)
# specify the form fields, and we'll match those to the keys on the task collection (lines 56-60)
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


# Access tasks collection and call remove
# Key value pair inside curly brackets 
# Use the object ID to format or parse the task ID in a way that's acceptable to Mongo.
# Redirect to get_tasks to see if task was deleted.
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


# Its job is to do a find on the categories table.
# categories.html is the template we're going to render.
# categories parameter will feed that from a direct call to MongoDB.
@app.route("/get_categories")
def get_categories():
    return render_template("categories.html", categories=mongo.db.categories.find())


# Don't forget to pass in the category_id as a parameter because we'll 
# use this to search for that document and pass it over to our editcategory.html page.
# Pass it over as a parameter called category, not categories, because it's a single category for editing (line 88)
# Pass in the category_id. Make sure it's in the format that's acceptable to Mongo (line 89)
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))


# Pass in the category_id as a parameter for use in the update call.
# We identify the ID and also the field that we want to update.
# Then let's pass in the request object (line 103)
# Drill into the form that's contained within the request object (line 103)
# Refer to the form item, whose name is category_name (line 103)
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


# Pass in the category_id as a parameter to be used to locate and 
# remove that category document from the categories collection.
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
