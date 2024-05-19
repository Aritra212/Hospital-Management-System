import sqlite3

def create_db():
    con=sqlite3.connect(database='hms1.db')
    cur=con.cursor()
    
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS department(id varchar(10) PRIMARY KEY,name text)")

        cur.execute("CREATE TABLE IF NOT EXISTS employees(id varchar(10) PRIMARY KEY,name text,guardian_name text,dob date,gender varchar(10),joining_date date,profession varchar(15),department varchar(10),post varchar(30),salary decimal(10,2),mobile varchar(20),email text,address text,password varchar(30), FOREIGN KEY(department) REFERENCES department(id))")

        cur.execute("CREATE TABLE IF NOT EXISTS patient(id varchar(10) PRIMARY KEY,name text,guardian_name text,dob date,gender varchar(10),status varchar(15),admit date,department varchar(10),doctor varchar(10),mobile varchar(20),email text,address text,problems text, medicines text, FOREIGN KEY(doctor) REFERENCES employees(id), FOREIGN KEY(department) REFERENCES department(id))")

        cur.execute("CREATE TABLE IF NOT EXISTS bed(id INTEGER PRIMARY KEY AUTOINCREMENT,category text,charges decimal(7,2),pid varchar(10) default null,FOREIGN KEY(pid) REFERENCES patient(id))")

        cur.execute("CREATE TABLE IF NOT EXISTS bills(id varchar(15) PRIMARY KEY, pid varchar(10),b_date date,tamt decimal(10,2),ramt decimal(10,2),items text, FOREIGN KEY(pid) REFERENCES patient(id))")

        cur.execute("CREATE TABLE IF NOT EXISTS charges(type text, category text, charges decimal(10,2), PRIMARY KEY(type, category))")

        cur.execute("insert into employees(id) values('EMP000')")
        cur.execute("insert into patient(id) values('PID000')")
        cur.execute("insert into department(id) values('DEP000')")
        cur.execute("insert into bills(id) values('BIL000')")
        print('success')

    except Exception as exp:
            print("Error",f"Error due to {str(exp)}")
    con.commit()
create_db()