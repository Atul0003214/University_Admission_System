from database.connect_database import *


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_user_name(cls, username):
        query = f"select * from university_admission_system.Users where email={username} ;"
        operation = "search"
        db_obj = DatabaseConnection()
        response = db_obj.execute_query(query, username, operation)
        print(response)
        if response:
            user = cls(response.user_id, response.email, response.password)
        else:
            user = None
        return user

    @classmethod
    def find_by_user_id(cls, _id):
        query = f"select * from university_admission_system.Users where user_id={_id} ;"
        operation = "search"
        db_obj = DatabaseConnection()
        response = db_obj.execute_query(query, "dummy@xyz.com", operation)
        if response:
            user = cls(response.user_id, response.email, response.password)
        else:
            user = None
        return user
