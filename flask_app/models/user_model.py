from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, Flask, redirect, session, request
from flask_bcrypt import Bcrypt
from flask_app.models import story_model
app = Flask(__name__)
bcrypt = Bcrypt(app)
import re  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validate_user_registration(data):
        print("DATAAA:", data)
        user_in_db = User.get_by_email(data)
        is_valid = True 
        if user_in_db:
            flash("Email already exists!", 'registration')
            is_valid = False
        if not data['register_first_name'].isalpha():
            flash("Please enter characters A-Z only in first name", 'registration')
            is_valid = False
        if len(data['register_first_name']) < 2:
            flash("First name must be at least 2 characters", 'registration')
            is_valid = False
        if not data['register_last_name'].isalpha():
            flash("Please enter characters A-Z only in last name", 'registration')
            is_valid = False
        if len(data['register_last_name']) < 2:
            flash("Last name must be at least 2 characters", 'registration')
            is_valid = False
        if len(data['register_password']) < 8:
            flash('Password must be at least 8 characters long', 'registration')
            is_valid = False
        if data['register_password'] != data['register_confirm_password']:
            flash('Passwords must match', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['register_email']): 
            flash("Invalid email!", 'registration')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data ):
        hash_browns = bcrypt.generate_password_hash(data['password'])
        user = {
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "email" : data["email"],
            "password" : hash_browns
        }
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"""
        return connectToMySQL('story_project_schema').query_db( query, user ) #this returns row of user ID that i just saved

    @staticmethod
    def validate_login(data):
        user_in_db = User.get_by_email(data)
        if len(data['password']) < 2:
            flash("Please dont leave email or password blank!", 'login')
            return False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email/password!", 'login')
            return False
        if not user_in_db:
            flash("Invalid Email/Password", 'login')
            return False
        if not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash("Invalid Email/Password", 'login')
            return False
        return True

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all_with_stories_created(cls):
        query = '''
                SELECT * FROM users
                LEFT JOIN stories ON users.id = creator_id;
                '''
        return connectToMySQL('story_project_schema').query_db( query ) # list of dictionaries
        

###########################################################################################################

    

    @classmethod
    def update_user(cls, data):
        query = """UPDATE users SET first_name = %(first_name)s, last_name
        = %(last_name)s, email = %(email)s
        WHERE id = %(id)s;"""
        return connectToMySQL('belt_exam').query_db( query, data )

    @classmethod
    def get_one_with_magazines_created(cls, data):
        query = '''
                SELECT * FROM users
                LEFT JOIN magazines ON users.id = creator_id
                WHERE users.id = %(id)s;
                '''
        results = connectToMySQL('belt_exam').query_db( query, data ) # list of dictionaries
        this_user = cls(results[0]) 
        print(this_user)
        this_user.magazines = [] # the .recipes part is made up, could be named anything
        if results[0]['magazines.id']:
            for row in results:
                data = {
                    **row,
                    'id' : row['magazines.id'],
                    'created_at' : row['magazines.created_at'],
                    'updated_at' : row['magazines.updated_at']
                }# creates unique data for a single recipe
                this_magazine = story_model.Magazine(data)# turns single dictionary recipe into a recipe object
                this_user.magazines.append(this_magazine)# adds recipe object to the user list of recipes
        return this_user

    @classmethod
    def get_one_with_recipes_favorited(cls, data):
        query = '''
                SELECT * FROM users
                LEFT JOIN favorites ON favoriter_id = users.id
                LEFT JOIN recipes ON recipe_id = recipes.id
                WHERE users.id = %(id)s;
                '''
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            one_user = cls(results[0])
            one_user.recipes_favorited = []
            for row in results:
                recipe_data = {
                    "id" : row['recipes.id'],
                    "name" : row['name'],
                    "description" : row['description'],
                    "instructions" : row['instructions'],
                    "user_id" : row['user_id'],
                    "created_at" : row['recipes.created_at'],
                    "updated_at" : row['recipes.updated_at'],
                    "under30min" : row['under30min'],
                    "user_created_at" : row['user_created_at']
                }
                recipe = recipe.Recipe(recipe_data)
                one_user.recipes_favorited.append(recipe)
            return one_user

    

    

    

    

    
    
    @staticmethod
    def validate_update_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 letters", 'update')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 letters", 'update')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email is wrong format", 'update')
            is_valid = False
        if not data['first_name'].isalpha():
            flash("Please enter characters A-Z only in first name", 'update')
            is_valid = False
        if not data['last_name'].isalpha():
            flash("Please enter characters A-Z only in last name", 'update')
            is_valid = False
        return is_valid
        