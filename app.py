"""Blogly application."""

from flask import Flask, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def add_user():
    """Directs to a form to add a new user"""
    return render_template('add_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a new user"""
    fname = request.form["fname"]
    lname = request.form["lname"]
    image = request.form["image_url"]

    new_user = User(first_name=fname, last_name=lname, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Shows edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """update user with new info"""
    fname = request.form["fname"] 
    lname = request.form["lname"]
    image = request.form["image_url"]

    user = User.query.get_or_404(user_id)
    if fname:
        user.first_name = fname
    if lname:
        user.last_name = lname
    if image:
        user.image_url = image

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    # user = User.query.get_or_404(user_id)
    user = User.query.filter_by(id=user_id).delete()
    # user.delete()
    db.session.commit()
    return redirect('/users')
