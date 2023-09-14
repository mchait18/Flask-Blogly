from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
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
            d = {"fname": "TestFirst2", "lname": "TestLast2", "image_url": "https://media3.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif?cid=790b7611b808f91fb1ef76582389256e93505b3cc474ffbf&rid=giphy.gif"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst2 TestLast2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"fname": "updatedFirst", "lname": "TestLast2", "image_url": "https://media3.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif?cid=790b7611b808f91fb1ef76582389256e93505b3cc474ffbf&rid=giphy.gif"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updatedFirst", html)

class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample post."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast", 
                    image_url="https://media3.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif?cid=790b7611b808f91fb1ef76582389256e93505b3cc474ffbf&rid=giphy.gif")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="Test Post", content="Test Content", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            # self.assertIn('Test Content', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            self.assertIn('Test Content', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "TestTitle2", "content": "TestContent2", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTitle2", html)
           

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "updatedTitle", "content": "UpdatedContent2", "user_id": self.user_id}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updatedTitle", html)
            self.assertIn("UpdatedContent2", html)

class TagsViewsTestCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add sample tag."""
        Tag.query.delete()
        
        tag = Tag(name="TestTag")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
         
    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
           
    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name": "Test Tag 2"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Tag 2", html)
           

    def test_edit_tag(self):
        with app.test_client() as client:
            d = {"name": "updated Tag"}
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updated Tag", html)
         
