from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25),
                           nullable=False)
    
    last_name = db.Column(db.String(25),
                           nullable=False)
    
    image_url = db.Column(db.String, default="https://www.istockphoto.com/vector/man-avatar-profile-male-face-silhouette-or-icon-isolated-on-white-background-vector-gm1142192548-306311139?phrase=silhouette")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"