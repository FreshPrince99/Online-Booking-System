import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'sql123',database = 'school')
cursor = mycon.cursor(buffered = True)
def signup():
    email = input("Enter email ID: ")
    password = input("Enter password: ")
    name = input("Enter full name: ")
    Type = 'C'
    cursor.execute("select * from UserLogin where EmailID like '{}';".format(email))
    if cursor.rowcount == 0:
        cursor.execute("insert into UserLogin values('{}','{}','{}','{}');".format(email,name,password,Type))
        cursor.execute('commit')
        print("successfully signed up...")
    else:
        a = input("Email already exists, want to login instead(Y/N): ")
        if a.lower() == 'y':
            login()
        else:
            signup()
    return [email, name, Type]
def login():
    email = input("Enter email ID: ")
    password = input("Enter password: ")
    cursor.execute("select * from UserLogin where EmailID like '{}';".format(email))
    if cursor.rowcount == 0:
        a = input("Email does not exist, want to sign up instead(Y/N): ")
        if a.lower() == 'y':
            signup()
        else:
            login()
    else:
        cursor.execute("select * from UserLogin where EmailID like '{}' and Password like '{}';".format(email,password))
        if cursor.rowcount == 0:
            print("Password is wrong. please re-enter password...")
            login()
        else:
            print("Successfully logged in...")
            cursor.execute("select * from UserLogin where EmailID like '{}' and Password like '{}';".format(email,password))
            temp = cursor.fetchall()
            name = temp[0][1]
            Type = temp[0][3]
    return [email, name, Type]


