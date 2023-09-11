from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast", 
                    image_url="https://media3.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif?cid=790b7611b808f91fb1ef76582389256e93505b3cc474ffbf&rid=giphy.gif")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst TestLast', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirst TestLast</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirst2", "last_name": "TestLast2", "image_url": "https://media3.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif?cid=790b7611b808f91fb1ef76582389256e93505b3cc474ffbf&rid=giphy.gif"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst2 TestLast2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "updatedFirst"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updatedFirst", html)
