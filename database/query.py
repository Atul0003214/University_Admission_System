# Query Dictionary
class query:

    query_dict = {
    "create_user_table" : "CREATE TABLE university_admission_system.Users (user_id uuid,first_name text,last_name text,email text  PRIMARY KEY,user_type text, faculty_id text, password text);",
    "inset_new_user":"INSERT INTO university_admission_system.Users (first_name,last_name,email,user_type,faculty_id,password,f_id) values ('first_name','last_name','email_id','student','faculty_id','password',uuid());",
    "create_course_table":"CREATE TABLE university_admission_system.Course_Table (course_id uuid,course_name text PRIMARY KEY,description text,added_by_name text,added_by_email text);",
    "add_course":"INSERT INTO university_admission_system.Course_Table (course_id,course_name,description,added_by_name,added_by_email) values(uuid(),'{course_name}','{course_description}','{faculty_email}','{faculty_email}');",
    "apply_new_course":"CREATE TABLE university_admission_system.Applied_Course_Table (applied_course_id uuid PRIMARY KEY,course_name text ,student_first_name text,student_last_name text,student_father_name text, student_email text, highest_qualification text,date timeuuid);",
    "insert_applied_course":"CREATE TABLE university_admission_system.Faculty (faculty_id uuid,faculty_number text PRIMARY KEY,faculty_first_name text,faculty_last_name text,faculty_doj timestamp,faculty_dob timestamp); "

    }







