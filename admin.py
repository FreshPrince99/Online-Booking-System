import mysql.connector as sqltor
from datetime import *
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'sql123',database = 'school')
cursor = mycon.cursor(buffered = True)
def insert_movie():
    cursor.execute("select MovieID from IdGenerationTbl;")
    temp = cursor.fetchall()
    movieid = temp[0][0]
    name = input("Enter Movie Name: ")
    StDate = input("Enter Start Date(yyyy-mm-dd): ")
    EnDate = input("Enter End Date(yyyy-mm-dd): ")
    cursor.execute("insert into MovieTbl(MovieID,MovieName,StartDate,EndDate) values({},'{}','{}','{}');".format(movieid,name,StDate,EnDate))
    cursor.execute("commit;")
    cursor.execute("update IdGenerationTbl set MovieID = MovieID +1;")
    cursor.execute("commit;")
    print("Movie has been inserted...")
def schedule_movies():
    cursor.execute("select ScheduleID from IdGenerationTbl;")
    temp = cursor.fetchall()
    scheduleid = temp[0][0]
    schDate = input("Pick a Date(yyyy-mm-dd): ")
    schTime = input("Pick a time(hh:mm:ss): ")
    cursor.execute("select MovieID, MovieName from MovieTbl where '{}' between StartDate and EndDate;".format(schDate))
    if cursor.rowcount == 0:
        print("No movies available...")
    else:
        temp = cursor.fetchall()
        print("Movies available for showing: ",end = '')
        for i in temp:
            print(i[1]+'('+str(i[0])+')',end = ', ')
        print()
        movieid = int(input("Pick MovieId to Schedule: "))
        cursor.execute("insert into MovieScheduleTbl values({},{},'{}','{}');".format(scheduleid,movieid,schDate,schTime))
        cursor.execute("commit;")
        cursor.execute("update IdGenerationTbl set ScheduleID = ScheduleID +1;")
        cursor.execute("commit;")
        for i in range(1,16):
            if(i<6):
                seatid = 'A'+str(i)
            if(i>5 and i<11):
                seatid = 'B'+str(i-5)
            if(i>10):
                seatid = 'C'+str(i-10)
            cursor.execute("select TranID from IdGenerationTbl;")
            temp = cursor.fetchall()
            tranid = temp[0][0]
            cursor.execute("insert into MovieTransactionTbl(TranID,MovieID,ScheduleID,SeatID) values({},{},{},'{}');".format(tranid,movieid,scheduleid,seatid))
            cursor.execute("commit;")
            cursor.execute("update IdGenerationTbl set TranID = TranID +1;")
            cursor.execute("commit;")
        print("Movie has been scheduled...")
def view_bookings():
    vdate = input("Pick a date(yyyy-mm-dd): ")
    cursor.execute("select * from moviescheduletbl where Date like '{}';".format(vdate))
    temp = cursor.fetchall()
    if cursor.rowcount != 0:
        schid = temp[0][0]
        movieid = temp[0][1]
        cursor.execute("select TranID, SeatID, EmailID from MovieTransactionTbl where MovieID = {} and ScheduleID = {} and Status like 'B';".format(movieid,schid))
        temp2 = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Bookings Yet...")
        else:
            print("Tickets Booked For The Movie: ")
            for i in temp2:
                print("Ticket Number: {}, SeatID: {}, EmailID: {}".format(i[0],i[1],i[2]))
    else:
        print("No movies scheduled that day...")

def alter_prices():
    cursor.execute("select Price from seattbl where SeatID like 'A1';")
    temp = cursor.fetchall()
    std = temp[0][0]
    cursor.execute("select Price from seattbl where SeatID like 'C1';")
    temp2 = cursor.fetchall()
    g = temp2[0][0]
    print("""The original prices are:
1)Standard seat: {}
2)Gold class seat: {}""".format(std,g))
    nstd = int(input("Enter new price for standard seats: "))
    ng = int(input("Enter new price for gold class seat: "))
    cursor.execute("update SeatTbl set price = {} where SeatID like 'A_' or SeatID like 'B_';".format(nstd))
    cursor.execute("commit;")
    cursor.execute("update SeatTbl set price = {} where SeatID like 'C_';".format(ng))
    cursor.execute("commit;")
    print("Prices have been updated...")


