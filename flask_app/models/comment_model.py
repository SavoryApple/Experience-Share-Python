from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.story_id = data['story_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (content, created_at, updated_at, user_id, story_id) VALUES (%(content)s, NOW(), NOW(), %(user_id)s, %(story_id)s);"
        return connectToMySQL('story_project_schema').query_db( query, data )

    @staticmethod
    def validate_create_comment(data):
        is_valid = True 
        if len(data['content']) < 1:
            flash("Comments must be at least 1 character", 'comment')
            is_valid = False
        return is_valid

    @classmethod
    def get_all_with_all_users(cls, data):
        query = "SELECT * FROM comments LEFT JOIN users ON users.id = comments.user_id WHERE story_id = %(story_id)s"
        return connectToMySQL('story_project_schema').query_db( query, data )
        