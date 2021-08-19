from flask import Flask, request, render_template, redirect, url_for
from Log.Log_From_Config import LogDetails
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database.connect_database import *
from database.query import query
from flask_mail import Mail, Message
import configparser

app = Flask(__name__)  # creating the Flask class object
app.config['SECRET_KEY'] = "thisissecretkey"
login_manager = LoginManager()
login_manager.init_app(app)

#=============================
config = configparser.ConfigParser()
config.read('Email/email_parameter.ini')
# configuration of mail
app.config['MAIL_SERVER'] = config.get('EMAIL_PARAMETER', 'MAIL_SERVER')
app.config['MAIL_PORT'] = config.get('EMAIL_PARAMETER', 'MAIL_PORT')
app.config['MAIL_USERNAME'] = config.get('EMAIL_PARAMETER', 'MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config.get('EMAIL_PARAMETER', 'MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = config.get('EMAIL_PARAMETER', 'MAIL_USE_SSL')

#==========================


# user class for flask login module
class User(UserMixin):
    def __init__(self, userid, username):
        self.id = userid
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    try:
        u_id = ""
        user_name = ""
        query = f"select * from university_admission_system.Users where email= '{user_id}';"
        operation = "search"
        db_obj = DatabaseConnection()
        users = db_obj.execute_query(query, "dummy@xyz.com", operation)
        for user in users:
            u_id = user.user_id
            user_name = user.email
        user_obj = User(u_id, user_name)
        return user_obj
    except Exception as load_user_e:
        LogDetails("load_user", load_user_e)



# open the home page initially
@app.route('/')
def home():
    try:
        return render_template("login.html")
    except Exception as e:
        LogDetails("home", e)


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            email_id = request.form['email']
            pwd = request.form['psw']
            query = f"select * from university_admission_system.Users where email= '{email_id}';"
            operation = "search"
            db_obj = DatabaseConnection()
            users = db_obj.execute_query(query, "dummy@xyz.com", operation)
            if users:
                for user in users:
                    u_id = user.user_id
                    user_name = user.email
                    user_type = user.user_type
                    print(user_name)
                    user_password = user.password
                    print(user_password)
                    if pwd == user_password:
                        u = User(u_id, user_name)
                        login_user(u)
                        LogDetails("New login", user_name)
                        if user_type == "faculty":
                            return redirect(url_for('faculty_dashboard_home'))
                        else:
                            return redirect(url_for('student_dashboard', student_email=user_name))

            return render_template("login.html")

    except Exception as e:
        LogDetails("login", e)


@app.route('/signup', methods=['GET'])
def signup():
    try:
        return render_template("signup.html")
    except Exception as e:
        LogDetails("signup", e)


@app.route('/signup_submit', methods=['POST', 'GET'])
def signup_submit():
    try:
        if request.method == 'POST':
            first_name = request.form['fname']
            last_name = request.form['lname']
            email_id = request.form['email']
            user_type = request.form['utype']
            faculty_id = request.form['fid']
            password = request.form['psw']
            operation = "create"
            create_user = f"INSERT INTO university_admission_system.Users (first_name,last_name,email,user_type,faculty_id,password,user_id) values ('{first_name}','{last_name}','{email_id}','{user_type}','{faculty_id}','{password}',uuid());"
            dbobj = DatabaseConnection()
            response = dbobj.execute_query(create_user, email_id,
                                           operation)  # modify the code to handle the render template if the user already exist.
            LogDetails("signup_submit", response)
            return render_template("login.html")
        return "Invalid request type"
    except Exception as e:
        LogDetails("signup_submit", e)


@app.route("/faculty_dashboard_home")
@login_required
def faculty_dashboard_home():
    try:
        return render_template("faculty_dashboard.html")
    except Exception as e:
        LogDetails("faculty_dashboard_home", e)


@app.route("/add_course", methods=['POST', 'GET'])
@login_required
def add_course():
    if request.method == 'POST':
        course_name = request.form['cname']
        course_description = request.form['cdes']
        faculty_email = request.form['femail']
        LogDetails("add_course named ", course_name)
        final_query = f"INSERT INTO university_admission_system.Course_Table (course_id,course_name,description,added_by_name,added_by_email) values(uuid(),'{course_name}','{course_description}','{faculty_email}','{faculty_email}');"
        LogDetails("add_course_query", final_query)
        adddbobj = DatabaseConnection()
        response = adddbobj.add_course_query(final_query)
        return redirect(url_for('faculty_dashboard_home'))
    else:
        return "Not a post request."


# route for redirecting faculty from course management to faculty status.
@app.route('/faculty_status', methods=['GET'])
@login_required
def faculty_status():
    try:
        if request.method == 'GET':
            fetch_applied_course_query = "select course_name,std_first_name,std_last_name,std_father_name,std_email,std_qualification,applied_date,application_id,status from university_admission_system.Registered_Course_Table;"
            faculty_status_dbobj = DatabaseConnection()
            response = faculty_status_dbobj.faculty_status_query(fetch_applied_course_query)
            return render_template("faculty_status.html", appliedcourselist=response)
        return "the method is not allowed"
    except Exception as e:
        LogDetails("faculty_status", e)


# route for redirecting student to status page.
@app.route('/student_status/<student_email>', methods=['GET'])
@login_required
def student_status(student_email):
    try:
        if request.method == 'GET':
            fetch_applied_course_query = f"select course_name,std_first_name,std_last_name,std_father_name,std_email,std_qualification,applied_date,application_id,status from university_admission_system.Registered_Course_Table where std_email='{student_email}' ALLOW FILTERING;"
            faculty_status_dbobj = DatabaseConnection()
            response = faculty_status_dbobj.faculty_status_query(fetch_applied_course_query)
            return render_template("student_status.html", appliedcourselist=response)
        return "the method is not allowed"
    except Exception as e:
        LogDetails("faculty_status", e)


# route for redirecting faculty from course management to contact us.
@app.route('/contact_us', methods=['GET'])
@login_required
def contact_us():
    try:
        return render_template("contact_us.html")
    except Exception as e:
        LogDetails("contact_us", e)


# route for redirecting faculty from course management to modify course.
@app.route('/modify_course')
@login_required
def modify_course():
    try:
        if request.method == 'GET':
            search_course_query = "select course_name from university_admission_system.Course_Table;"
            modify_dbobj = DatabaseConnection()
            response = modify_dbobj.search_course_query(search_course_query)
            return render_template("faculty_modify_course.html", courseNameList=response)
        return "the method is not allowed"
    except Exception as e:
        LogDetails("modify_course", e)


# route for redirecting faculty from course management to delete course.
@app.route('/delete_course')
@login_required
def delete_course():
    try:
        if request.method == 'GET':
            search_course_query = "select course_name from university_admission_system.Course_Table;"
            delete_dbobj = DatabaseConnection()
            response = delete_dbobj.search_course_query(search_course_query)
            return render_template("faculty_delete_course.html", courseNameList=response)
        return "the method is not allowed"
    except Exception as e:
        LogDetails("delete_course", e)


# route for modifying the selected course details
@app.route('/modify_selected_course', methods=['POST', 'GET'])
@login_required
def modify_selected_course():
    try:
        if request.method == 'POST':
            modify_selected_dbobj = DatabaseConnection()
            course_name = request.form['c_id_to_modify']
            updated_description = request.form['emdes']
            modify_course_query = f"UPDATE university_admission_system.Course_Table SET description = '{updated_description}' where course_name = '{course_name}'; "
            modify_response = modify_selected_dbobj.modify_course_query(modify_course_query)
            LogDetails("modify_response", modify_response)
            return redirect(url_for('modify_course'))
    except Exception as e:
        LogDetails("modify_selected_course", e)


# route for deleting the selected course details
@app.route('/delete_selected_course', methods=['POST', 'GET'])
@login_required
def delete_selected_course():
    try:
        if request.method == 'POST':
            delete_selected_dbobj = DatabaseConnection()
            course_name = request.form['c_id_to_delete']
            delete_course_query = f"delete from university_admission_system.Course_Table where course_name = '{course_name}'; "
            delete_response = delete_selected_dbobj.delete_course_query(delete_course_query)
            LogDetails("delete_response", delete_response)
            return redirect(url_for('delete_course'))
    except Exception as e:
        LogDetails("delete_selected_course", e)


# route for redirecting faculty to course management
@app.route('/course_management', methods=['GET'])
@login_required
def course_management():
    try:
        return render_template("faculty_dashboard.html")
    except Exception as e:
        LogDetails("course_management", e)


@app.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        LogDetails("logout", "User logged out successfully")
        return render_template("login.html")
    except Exception as logout_e:
        LogDetails("logout", logout_e)


@app.route('/apply_course', methods=['POST', 'GET'])
@login_required
def apply_course():
    try:
        if request.method == 'POST':
            course_name = request.form['scourse']
            std_first_name = request.form['fname']
            std_last_name = request.form['lname']
            std_father_name = request.form['fathername']
            std_email = request.form['email']
            std_highest_qualification = request.form['hqual']
            create_table_query = "CREATE TABLE IF NOT EXISTS university_admission_system.Registered_Course_Table (course_name text,std_first_name text ,std_last_name text,std_father_name text,std_email text,std_qualification text,applied_date timestamp, application_id uuid PRIMARY KEY,status text);"
            applied_course_query = f"INSERT INTO university_admission_system.Registered_Course_Table (course_name,std_first_name,std_last_name,std_father_name,std_email,std_qualification,applied_date,application_id,status) values('{course_name}','{std_first_name}','{std_last_name}','{std_father_name}','{std_email}','{std_highest_qualification}',toTimestamp(now()),uuid(),'Under Review');"
            LogDetails("create table query", create_table_query)
            create_table_dbobj = DatabaseConnection()
            insert_table_dbobj = DatabaseConnection()
            response = create_table_dbobj.create_table(create_table_query)
            response = insert_table_dbobj.apply_course_query(applied_course_query)
            return redirect(url_for('student_dashboard', student_email=std_email))
        else:
            return "Not a post request."
    except Exception as e:
        LogDetails("apply_course", e)


@app.route('/student_dashboard/<student_email>', methods=['GET'])
@login_required
def student_dashboard(student_email):
    try:
        if request.method == 'GET':
            search_course_query = "select course_name from university_admission_system.Course_Table;"
            student_dashboard_dbobj = DatabaseConnection()
            response = student_dashboard_dbobj.search_course_query(search_course_query)
            return render_template("student_dahboard.html", courseNameList=response, std_email=student_email)
        return "the method is not allowed"
    except Exception as e:
        LogDetails("student_dashboard", e)


@app.route('/send_email/<action>/<string:address>/<string:application_id>', methods=['POST'])
@login_required
def send_approve_email(action, address, application_id):
    try:
        if request.method == 'POST':
            mail = Mail(app)
            msg = Message(
                'Status Update',
                sender='atul00032146@gmail.com',
                recipients=[address]

            )
            msg.body = 'Your application status is updated. Please login to the application to check.'
            if action == 'approve':
                update_approve_status_query = f"UPDATE university_admission_system.Registered_Course_Table SET status = 'Interview Scheduled' WHERE application_id = {application_id};"
                update_approve_dbobj = DatabaseConnection()
                response = update_approve_dbobj.update_course_status(update_approve_status_query)
            elif action == 'disapprove':
                update_disapprove_status_query = f"UPDATE university_admission_system.Registered_Course_Table SET status = 'Rejected' WHERE application_id = {application_id};"
                update_disapprove_dbobj = DatabaseConnection()
                response = update_disapprove_dbobj.update_course_status(update_disapprove_status_query)
            elif action == 'selected':
                update_selected_status_query = f"UPDATE university_admission_system.Registered_Course_Table SET status = 'Selected' WHERE application_id = {application_id};"
                update_selected_dbobj = DatabaseConnection()
                response = update_selected_dbobj.update_course_status(update_selected_status_query)
            mail.send(msg)
            return redirect(url_for('faculty_status'))
        return redirect(url_for('faculty_status'))
    except Exception as e:
        LogDetails("send_email", e)


#====================================
# @app.route('/send_email/disapprove/<string:address>/<string:application_id>', methods=['POST'])
# def send_disapprove_email(address, application_id):
#     try:
#         if request.method == 'POST':
#             mail = Mail(app)
#             msg = Message(
#                 'Status Update',
#                 sender='atul00032146@gmail.com',
#                 recipients=[address]
#             )
#             msg.body = 'Your application status is updated. Please login to the application to check.'
#             update_disapprove_status_query = f"UPDATE university_admission_system.Registered_Course_Table SET status = 'Rejected' WHERE id = '{application_id}';"
#             update_disapprove_dbobj = DatabaseConnection()
#             response = update_disapprove_dbobj.update_course_status(update_disapprove_status_query)
#             mail.send(msg)
#             return redirect(url_for('faculty_status'))
#         return redirect(url_for('faculty_status'))
#     except Exception as e:
#         LogDetails("send_email", e)

#=================================


if __name__ == "__main__":
    app.run(debug=True)
