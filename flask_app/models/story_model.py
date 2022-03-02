from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Story:
    def __init__( self , data ):
        self.id = data['id']
        self.category = data['category']
        self.item_name = data['item_name']
        self.place_purchased = data['place_purchased']
        self.img_url = data['img_url']
        self.story = data['story']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

    @classmethod
    def save(cls, data):
        query = """INSERT INTO stories (category, item_name, place_purchased, img_url, story, created_at, updated_at, creator_id) VALUES (%(category)s, %(item_name)s, %(place_purchased)s, %(img_url)s, %(story)s, NOW(), NOW(), %(creator_id)s);"""
        return connectToMySQL('story_project_schema').query_db( query, data )

    @staticmethod
    def validate_create_story(data):
        is_valid = True 
        if data['category'] == "choose":
            flash("Please select a category!", 'create')
            is_valid = False
        if len(data['item_name']) < 3:
            flash("Item name must be at least 3 characters", 'create')
            is_valid = False
        if len(data['place_purchased']) < 3:
            flash("Place purchased must be at least 3 characters", 'create')
            is_valid = False
        if len(data['story']) < 25:
            flash("Please write a story at least 25 characters long", 'create')
            is_valid = False
        return is_valid

    @classmethod
    def get_all_with_all_users(cls):
        query = '''
                SELECT * FROM stories
                JOIN users ON users.id = creator_id;
                '''
        return connectToMySQL('story_project_schema').query_db( query ) # list of dictionaries

    @classmethod
    def get_all_with_all_users_sorted_by_a_thru_z(cls):
        query = '''
                SELECT * FROM stories
                JOIN users ON users.id = creator_id ORDER BY item_name;
                '''
        return connectToMySQL('story_project_schema').query_db( query ) # list of dictionaries

    @classmethod
    def get_all_with_all_users_sorted_by_category(cls):
        query = '''
                SELECT * FROM stories
                JOIN users ON users.id = creator_id ORDER BY category;
                '''
        return connectToMySQL('story_project_schema').query_db( query ) # list of dictionaries
        
    @classmethod
    def get_one_with_creator(cls, data):
        query = '''
                SELECT * FROM stories
                JOIN users ON creator_id = users.id
                WHERE stories.id = %(id)s;
                '''
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            this_story = cls(results[0])
            for row in results:
                user_data = {
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_story.user = this_user
            return this_story

    @classmethod
    def get_story_by_id(cls, data):
        query = """SELECT * FROM stories WHERE id = %(id)s;"""
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return cls(results[0])
        return False

    @classmethod
    def update_story(cls, data):
        query = """UPDATE stories SET category = %(category)s, item_name=%(item_name)s, place_purchased=%(place_purchased)s, img_url=%(img_url)s, story=%(story)s, updated_at=NOW() WHERE id=%(id)s;"""
        return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def delete_story(cls, data):
        query = """DELETE FROM stories WHERE id = %(id)s"""
        return connectToMySQL('story_project_schema').query_db( query, data )




##############################################################################################################

    

    

    

    

    @classmethod
    def get_all_magazines_and_creators(cls):
        query = """SELECT * FROM magazines JOIN users ON users.id = magazines.creator_id;"""
        return connectToMySQL('belt_exam').query_db(  query )

    