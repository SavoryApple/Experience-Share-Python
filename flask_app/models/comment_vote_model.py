from flask_app.config.mysqlconnection import connectToMySQL

class comment_Vote:
    def __init__( self , data ):
        self.id = data['id']
        self.vote = data['vote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comment_id = data['comment_id']
        self.user_id = data['user_id']
        self.story_id = data['story_id']

    @classmethod
    def create_vote_comment_with_user(cls, data):
        query = "SELECT * FROM comment_votes WHERE user_id = %(user_id)s AND comment_id = %(comment_id)s;"
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return False
        else:
            query = "INSERT INTO comment_votes (vote, created_at, updated_at, user_id, comment_id) VALUES (0, NOW(), NOW(), %(user_id)s, %(comment_id)s);"
            return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def upvote_comment_on_story_from_user(cls, data):
        query = "SELECT * FROM comment_votes WHERE user_id = %(user_id)s AND comment_id = %(comment_id)s AND vote = 1"
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return False
        else:
            query = "UPDATE comment_votes SET vote = 1 WHERE user_id = %(user_id)s AND comment_id = %(comment_id)s"
            return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def downvote_comment_on_story_from_user(cls, data):
        query = "SELECT * FROM comment_votes WHERE user_id = %(user_id)s AND comment_id = %(comment_id)s AND vote = -1"
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return False
        else:
            query = "UPDATE comment_votes SET vote = -1 WHERE user_id = %(user_id)s AND comment_id = %(comment_id)s"
            return connectToMySQL('story_project_schema').query_db( query, data )

    @classmethod
    def sum_all_votes_with_comment_id(cls, data):
        query = "SELECT SUM(vote) FROM comment_votes WHERE comment_id = %(comment_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('story_project_schema').query_db( query, data )
        if results:
            return results[0]
        return False

    
        