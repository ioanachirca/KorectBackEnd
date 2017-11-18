#!/usr/bin/python
import psycopg2
import psycopg2.extras
import traceback
import time

class DBConnection:
    def __init__(self, dbname, user, host, password):
        self.dbConnection = psycopg2.connect("dbname='"+ dbname + "' user='" + user + "' host='" +
                                                host + "' password='" + password +"'")


    def destroy(self):
        if self.dbConnection is not None:
            self.dbConnection.close()
            print('Database connection closed.')


    def truncate_table(self, tableName):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("TRUNCATE " + tableName + " CASCADE;")
        self.dbConnection.commit()
        print("Deleted data from table " + tableName)
        cursor.close()


    def login(self, username, password):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT username, password from users where username=%s", (username,))
        return_value = None
 
        data = cursor.fetchone()
        print(data)
        if (data['password'] == password):
            print("yes")
            cursor.execute("SELECT u_id from users_info where username=%s", (username,))
            data = cursor.fetchone()
            return_value = data['u_id']
        else:
            print("no")
        cursor.close()
        return return_value


    def register(self, username, password, utype):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""BEGIN;
                                INSERT INTO users ("username","password") VALUES (%s, %s);
                                INSERT INTO users_info ("username","type") VALUES (%s, %s);
                                """, (username, password, username, utype, ))
        self.dbConnection.commit()
        cursor.close()


    def delete_user(self, username):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""BEGIN;
                                DELETE FROM users where username=%s;
                                DELETE FROM users_info where username=%s;
                                """, (username, username, ))
        self.dbConnection.commit()
        cursor.close()


    def add_exam(self, exam_name):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""INSERT INTO exams ("name") VALUES (%s)
                                """, (exam_name, ))
        self.dbConnection.commit()
        cursor.close()


    def get_exam(self, exam_name):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""SELECT * FROM exams WHERE name=%s;""", (exam_name,));
        return_value = cursor.fetchall()
        print(return_value)
        cursor.close()
        return return_value

    def delete_exam(self, exam_name):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""DELETE FROM exams WHERE name=%s;""", (exam_name,))
        self.dbConnection.commit()
        cursor.close()


    def add_question(self, text, difficulty, subject, is_multiple_answer):
        command = """INSERT INTO questions(text, difficulty, subject, ma)
                     VALUES (%s, %s, %s, %s) RETURNING q_id;"""
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(command, (text, difficulty, subject, is_multiple_answer, ))
        q_id = cursor.fetchone()
        self.dbConnection.commit()
        cursor.close()
        return q_id

    def delete_question(self, text):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""DELETE FROM questions WHERE text=%s;""", (text,))
        self.dbConnection.commit()


    def add_answer_to_question(self, q_text, a_text, is_correct, var):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""SELECT q_id FROM questions WHERE text=%s;""", (q_text,))
        question = cursor.fetchone()
        if question is None:
            return
        q_id = question["q_id"]
        print(q_id)
        cursor.execute("""INSERT INTO answers (q_id, text, correct, var) VALUES (%s, %s, %s, %s);""", 
                            (q_id, a_text, is_correct, var,))       
        self.dbConnection.commit()
        cursor.close()


    def get_question_with_answers(self, q_id):
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""SELECT * FROM questions WHERE q_id=%s;""", (q_id,))
        question = cursor.fetchone()
        if question is None:
            print("No question with id %s", (q_id,))
            return []
        else:
            print(question)
            cursor.execute("""SELECT * FROM answers WHERE q_id=%s;""", (q_id,))
            answers = cursor.fetchall()
            if answers == []:
                print("No answers for question %s", (q_id,))
                return []
            else:
                return [] # rethink this when needed

        cursor.close()

    
        
if __name__ == '__main__':
    try:
        my_db = DBConnection(dbname='korect', user='postgres', host='localhost', password='postgres')
        print("OK")

    except:
        print ("ERROR")
        traceback.print_exc()
    finally:
        my_db.destroy()
