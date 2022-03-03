from flask_app.config.mysqlconnection import connectToMySQL

class story_Vote:
    def __init__( self , data ):
        self.id = data['id']
        self.vote = data['vote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comment_id = data['comment_id']
        self.user_id = data['user_id']
        self.story_id = data['story_id']

    @classmethod
    def upvote_on_story_from_user(cls, data):
        query = "INSERT INTO story_votes (vote, created_at, updated_at, user_id, story_id) VALUES (1, NOW(), NOW(), %(user_id)s, %(story_id)s);"
        return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def downvote_on_story_from_user(cls, data):
        query = "INSERT INTO story_votes (vote, created_at, updated_at, user_id, story_id) VALUES (-1, NOW(), NOW(), %(user_id)s, %(story_id)s);"
        return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def sum_all_votes_with_story_id(cls, data):
        query = "SELECT SUM(vote) FROM story_votes WHERE story_id = %(story_id)s;"
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return results[0]
        return False
    
        