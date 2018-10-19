from app import mysql

def myDatabase():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""CREATE DATABASE IF NOT EXISTS mydatabase""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS studentinformation(
    studentid VARCHAR(9) NOT NULL,
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR (20) NOT NULL,
    sex VARCHAR (6) NOT NULL,
    course VARCHAR (4) NOT NULL,
    PRIMARY KEY(studentid))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS courses(
    courseid VARCHAR(4) NOT NULL ,
    courseDescription TEXT(255) NOT NULL,
    PRIMARY KEY (courseid))""")

    cursor.close()
    conn.close()

class Operation(object):
    def __init__(self, studentid, firstname, lastname, sex, course):
        self.studentid = studentid
        self.firstname = firstname
        self.lastname = lastname
        self.sex = sex
        self.course = course

    def signup(self):
        myDatabase()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO studentinformation(studentid, firstname, lastname, sex, course)
                      VALUES ('%s','%s','%s','%s','%s')"""%
                      (self.studentid, self.firstname, self.lastname, self.sex, self.course))
        conn.commit()
        cursor.close()
        conn.close()

def search(data):
    datas = '%'+data+'%'
    myDatabase()
    conn = mysql.connect()
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()
    cur4 = conn.cursor()
    cur5 = conn.cursor()
    cur1.execute("SELECT * FROM studentinformation WHERE studentid = '%s'" %(data))
    res1 = cur1.fetchall()
    cur2.execute("SELECT * FROM studentinformation WHERE firstname LIKE '%s'"%(datas))
    res2 = cur2.fetchall()
    cur3.execute("SELECT * FROM studentinformation WHERE lastname LIKE '%s'"%(datas))
    res3 = cur3.fetchall()
    cur4.execute("SELECT * FROM studentinformation WHERE sex LIKE '%s'"%(datas))
    res4 = cur4.fetchall()
    cur5.execute("SELECT * FROM studentinformation WHERE course LIKE '%s'"%(datas))
    res5 = cur5.fetchall()
    return res1+res2+res3+res4+res5

def update(holder,idnumber,firstname,lastname,sex,course):
    myDatabase()
    conn = mysql.connect()
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()
    cur4 = conn.cursor()
    cur5 = conn.cursor()
    cur1.execute("""UPDATE studentinformation SET studentid = '%s' WHERE studentid = '%s' """ %(idnumber,holder))
    cur2.execute("""UPDATE studentinformation SET firstname = '%s' WHERE studentid = '%s' """ % (firstname, holder))
    cur3.execute("""UPDATE studentinformation SET lastname = '%s' WHERE studentid = '%s' """ % (lastname, holder))
    cur4.execute("""UPDATE studentinformation SET sex = '%s' WHERE studentid = '%s' """ % (sex, holder))
    cur5.execute("""UPDATE studentinformation SET course = '%s' WHERE studentid = '%s' """ % (course, holder))
    conn.commit()
    cur1.close()
    cur2.close()
    cur3.close()
    cur4.close()
    cur5.close()
    conn.close()

def delete(idnumber):
    myDatabase()
    conn = mysql.connect()
    cur1 = conn.cursor()
    cur1.execute("""DELETE FROM studentinformation WHERE studentid = '%s'""" %(idnumber))
    conn.commit()
    cur1.close()
    conn.close()

def all():
    myDatabase()
    conn = mysql.connect()
    cur1 = conn.cursor()
    cur1.execute("""SELECT * FROM studentinformation JOIN courses ON studentinformation.course = courses.courseId""")
    result = cur1.fetchall()
    return result