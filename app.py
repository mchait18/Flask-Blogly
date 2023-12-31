"""Blogly application."""

from flask import Flask, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    return render_template('user/list.html', users=users)

@app.route('/users/new')
def add_user():
    """Directs to a form to add a new user"""
    return render_template('user/add_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a new user"""
    fname = request.form.get("fname")
    lname = request.form.get('lname')
    image = request.form.get('image_url') or None

    new_user = User(first_name=fname, last_name=lname, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = list(Post.query.filter(Post.user_id==user_id)) 
    return render_template("user/details.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Shows edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template("user/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """update user with new info"""
    user = User.query.get_or_404(user_id)
    
    user.first_name = request.form.get("fname")
    user.last_name = request.form.get('lname')
    user.image_url = request.form.get('image_url')
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

"""Posts methods"""
@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Directs user to a form to add a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post/add.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Creates a new post"""
    user = User.query.get_or_404(user_id)
    postTags=[int(num) for num in request.form.getlist('tagsChecked')]
    tags=Tag.query.filter(Tag.id.in_(postTags)).all()

    new_post = Post(title=request.form.get("title"),
                     content=request.form.get('content'), 
                     user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    
    return render_template("post/details.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Shows edit post page"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post/edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """update post with new info"""
    post = Post.query.get_or_404(post_id)    
    postTags=[int(num) for num in request.form.getlist('tagsChecked')]
    
    post.title = request.form.get("title")
    post.content = request.form.get('content')
    post.tags = Tag.query.filter(Tag.id.in_(postTags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """deletes post"""
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

"""Tag routes"""
@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tag/list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show details about a single tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag/details.html", tag=tag)

@app.route('/tags/new')
def add_tag():
    """Directs to a form to add a new tag"""
    posts=Post.query.all()
    return render_template('tag/add.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Creates a new user"""
    tagPosts=[int(num) for num in request.form.getlist('posts')]
    posts=Post.query.filter(Post.id.in_(tagPosts)).all()
    new_tag = Tag(name=request.form.get("name"), posts=posts)
   
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Directs to a form to edit a tag"""    
    tag = Tag.query.get_or_404(tag_id)
    posts=Post.query.all()
    return render_template("tag/edit.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Update a tag with new info"""
    tagPosts=[int(num) for num in request.form.getlist('posts')]
    tag = Tag.query.get_or_404(tag_id)    
    tag.name = request.form.get("name")  
    tag.posts=Post.query.filter(Post.id.in_(tagPosts)).all()
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """deletes tag"""
    tag = Tag.query.get_or_404(tag_id)    
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')
