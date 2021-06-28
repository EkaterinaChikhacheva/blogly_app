from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    '''Test for views for Users'''

    # def __init__(self):
    #     return self

    def setUp(self):
        '''add simple user'''

        User.query.delete()

        user = User(first_name = 'Test', last_name = 'User', image_url = 'https://media.tenor.com/images/8af08a3556c6e66f5ce88539183efd23/tenor.gif')

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        '''Clean up any fouled transaction'''

        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client as client:
            resp = client.get(f'/users/{self.pet_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-4">Test User</h1>', html)
            self.assertIn(self.user.image_url, html)

    # def test_add_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name": "SecondTest", "last_name" : "SecondUser", "image_url" : "https://media.tenor.com/images/8af08a3556c6e66f5ce88539183efd23/tenor.gif"}
    #         resp = client.post('/', data = d, follow_redirects = True)
    #         html = resp.get_data(as_text = True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("SecondTest", html)