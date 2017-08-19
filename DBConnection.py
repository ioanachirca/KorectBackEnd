import psycopg2
import psycopg2.extras
import traceback
import time

class DBConnection:
    def __init__(self, dbname, user, host, password):
        self.dbConnection = psycopg2.connect("dbname='"+ dbname + "' user='" + user + "' host='" + host + "' password='" + password +"'");

    def destroy(self):
        if self.dbConnection is not None:
            self.dbConnection.close()
            print('Database connection closed.')


    def login(self, username, password):
        currentCursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor);
        currentCursor.execute("SELECT username, password from users where username='" + username + "'");
 
        # display the PostgreSQL database server version
        data = currentCursor.fetchone()
        print(data)

    def add_question(self, text, difficulty, subject, is_multiple_answer):
        command = """INSERT INTO questions(text, difficulty, subject, ma)
                     VALUES (%s, %s, %s, %s) RETURNING q_id;"""
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(command, (text, difficulty, subject, is_multiple_answer, ))
        q_id = cursor.fetchone()
        self.dbConnection.commit()
        cursor.close()

        return q_id

    def add_answer(self, q_id, text, is_correct, var):
        command = """INSERT INTO answers(q_id, text, correct, var)
                     VALUES (%s, %s, %s, %s);"""
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(command, (q_id, text, is_correct, var, ))
        self.dbConnection.commit()
        cursor.close()

    def get_question_with_answers(self, q_id):
        command = """SELECT * FROM questions WHERE q_id = """ + str(q_id) + """;"""
        cursor = self.dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(command)
        question = cursor.fetchone()
        if question == None:
            print("No question with id " + str(q_id))
        else:
            print(question)
            get_answers_command = """SELECT * FROM answers WHERE q_id = """ + str(q_id) + """;"""
            cursor.execute(command)
            answers = cursor.fetchall()
            if answers == []:
                print("No answers for question " + str(q_id))
            else:
                print("hah")

        cursor.close()

    
        


if __name__ == '__main__':
    try:
        my_db = DBConnection(dbname='korect', user='postgres', host='localhost', password='postgres');
        print("ok");
        #q_id = my_db.add_question("a sau b?", 1, "qw", False)
        #print("Added question with id " + str(q_id))
        my_db.get_question_with_answers(2)

    except:
        print ("EROARE");
        traceback.print_exc();
    finally:
        my_db.destroy();
        print('final');