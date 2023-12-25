from login_signup import *
from admin import *
from client import *
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'sql123',database = 'school')
cursor = mycon.cursor(buffered = True)
#loops until u sign in successfully
print("Welcome To BookMySeat")
a = input('''To continue further
1)Login
2)Signup
Enter Choice: ''')
while(True):
    if a == '1':
        L = login()
        email, name, Type = L[0],L[1],L[2]
        break
    elif a == '2':
        L =signup()
        email, name, Type = L[0],L[1],L[2]
        break
    else:
        print('Invalid input...Re-enter details')
        a = input('''1)Login
2)Signup
Enter Choice: ''')
print()
#after signing in we check if the user is admin or client
if Type == 'A':
    while(True):
        a = input("""1)View Bookings
2)Insert Movie
3)Schedule Movies
4)Alter Prices
5)Logout
Enter choice: """)
        if a == '1':
            view_bookings()
        elif a == '2':
            insert_movie()
        elif a == '3':
            schedule_movies()
        elif a == '4':
            alter_prices()
        elif a == '5':
            break
        else:
            print("Invalid input, re-enter choice...")
        print()
#if user is a client
elif Type == 'C':
    show_all(email)
