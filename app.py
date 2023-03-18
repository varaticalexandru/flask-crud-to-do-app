# imports
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set-up app
app = Flask(__name__)

# app config (tell app db location)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize db with app settings
with app.app_context():
    db = SQLAlchemy(app)

# db class/model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return "<Task %r>" % self.id


# create the db ()
    # from app import app, db
    # app.app_context().push()
    # db.create_all()


# index route for root URL
@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":  # add a task, upd the db
        
        task_content = request.form['content'] # get the content of the form from the request object

        # create ToDo object
        new_task = ToDo(content=task_content)

        # add task to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue adding that task"

    else:   # request.method == "GET"

        tasks = ToDo.query.order_by(ToDo.date_created).all() # all tasks ordered by creation date

        return render_template("index.html", tasks=tasks)

# delete route
@app.route("/delete/<int:id>")
def delete(id):

    task_to_delete = ToDo.query.get_or_404(id) # try to get the task by id from the db

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/')

    except:
        return "There was a problem deleting that task"


# update route
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    task = ToDo.query.get_or_404(id)    # try to get the task by id from the db

    if request.method == "POST":
       
       task.content = request.form["content"]
       
       try:
           db.session.commit()
           return redirect('/')
       except:
           return 'There was a problem updating that task'

    else:   # request.method == "GET"
        return render_template("update.html", task=task)


# main driver function
if __name__ == "__main__":
    app.run(debug=True)