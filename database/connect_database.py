import configparser
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from Log.Log_From_Config import LogDetails
from Log.Log_From_Config import LogDetails


# Get the database connection details.
class DatabaseConnection:
    """This class is to establish the connection with cassandra database"""

    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read('database/database.ini')
            self.client_id = self.config.get("CASSANDRA_DB", "client_id")
            self.client_secret = self.config.get("CASSANDRA_DB", "client_secret")
            # Make the database connection call
            self.cloud_config = {
                'secure_connect_bundle': 'database/secure-connect-university-admission-system.zip'
            }
            self.auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
            self.cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
            self.session = self.cluster.connect()
            LogDetails("DatabaseConnection class", "Request for connection started.")
        except Exception as init_e:
            LogDetails("home", init_e)

    def execute_query(self, query, email_id, operation):
        """This methode is to execute the query to the database """
        try:
            # before creating a new user validate if the user already exist in the system
            if operation == "create":
                result = ""
                validate_user = f"select count(*) from university_admission_system.Users where email='{email_id}';"
                c = self.session.execute(validate_user)
                for m in c:
                    if m.count:
                        result = "The Email already exist, You can try login with the same email"
                    else:
                        self.session.execute(query)
                        result = "The user created successfully"
                LogDetails("execute_query", result)
                return result
            elif operation == "search":
                output = self.session.execute(query)
                LogDetails("execute_query", output)
                return output
        except Exception as e:
            LogDetails("execute_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def add_course_query(self, query):
        """This is the function to add the new course to course table """
        try:
            LogDetails("database_executing_query", query)
            response = self.session.execute(query)
            LogDetails("add_course_query", response)
            return "the course added successfully"
        except Exception as e:
            LogDetails("add_course_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def search_course_query(self, query):
        """This is the function to fetch all  the course from the course table """
        try:
            course_name = []
            LogDetails("search_course_query", query)
            response = self.session.execute(query)
            LogDetails("search_course_query", response)
            for i in response:
                course_name.append(i.course_name)
            LogDetails("course_name_list", course_name)
            return course_name
        except Exception as e:
            LogDetails("search_course_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def delete_course_query(self, query):
        """This is the function to delete the course from the course table """
        try:
            LogDetails("delete_course_query", query)
            response = self.session.execute(query)
            LogDetails("delete_course_query", response)
            return "the course deleted successfully"
        except Exception as e:
            LogDetails("delete_course_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def modify_course_query(self, query):
        """This is the function to delete the course from the course table """
        try:
            LogDetails("modify_course_query", query)
            response = self.session.execute(query)
            LogDetails("modify_course_query", response)
            return "the course modified successfully"
        except Exception as e:
            LogDetails("modify_course_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def create_table(self, query):
        """This is the function to create new table in database.
            :parameter
            query = Query to execute to the database.
        """
        try:
            LogDetails("create_table", query)
            response = self.session.execute(query)
            LogDetails("create_table", response)
            return "the query successfully"
        except Exception as e:
            LogDetails("create_table", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")


    def apply_course_query(self, query):
        """This is the function to apply the new course by student
         :parameter
            query = Query to execute to the database.
        """
        try:
            LogDetails("apply_course_query", query)
            response = self.session.execute(query)
            LogDetails("apply_course_query", response)
            return "the course applied successfully"
        except Exception as e:
            LogDetails("apply_course_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

    def faculty_status_query(self, query):
        """This is the function to fetch all  the course from the course table """
        try:

            LogDetails("faculty_status_query", query)
            response = self.session.execute(query)
            LogDetails("faculty_status_query", response)
            return response
        except Exception as e:
            LogDetails("faculty_status_query", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")


    def update_course_status(self, query):
        """This is the function to update  the course status in the university_admission_system.Registered_Course_Table
         :parameter
            query = Query to execute to the database.
        """
        try:

            LogDetails("update_course_status", query)
            response = self.session.execute(query)
            LogDetails("update_course_status", response)
            return response
        except Exception as e:
            LogDetails("update_course_status", e)
        finally:
            LogDetails("close_connection", "connection closed successfully")

if __name__ == "__main__":
    db = DatabaseConnection()
    query1 = "INSERT INTO university_admission_system.Users (first_name,last_name,email,user_type,faculty_id," \
             "password,f_id) values ('first_name','last_name','email_id','student','faculty_id','password',uuid()); "
    db.execute_query(query1, "admin@zyx.com", "new_table")
