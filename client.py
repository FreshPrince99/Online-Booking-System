import mysql.connector as sqltor
from datetime import *
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'sql123',database = 'school')
cursor = mycon.cursor(buffered = True)
from datetime import *   
def show_all(email):
    cursor.execute("select * from movietbl where Active like 'y';")
    tbl = cursor.fetchall()
    print("{:>7}".format("MovieID"),"{:>15}".format("Movie Name"))
    for i in tbl:
        print("{:>7}".format(i[0]),"{:>15}".format(i[1]))
    print()
    if(True):
        mname = input("Enter movie name: ")
        cursor.execute("select MovieScheduleTbl.ScheduleID, MovieTbl.MovieName, MovieScheduleTbl.Date, MovieScheduletbl.Time from MovieScheduleTbl inner join MovieTbl on MovieScheduletbl.MovieID = MovieTbl.MovieID where MovieTbl.MovieName like '{}';".format(mname))
        print()
        if cursor.rowcount == 0:
            print("Sorry no shows are shceduled for this movie...")
        else:
            
            schtbl = cursor.fetchall()
            print("{:>5}".format("Sl.No"),"{:>11}".format("ScheduleID"),"{:>25}".format("Movie Name"),"{:>10}".format("Date"), "{:>8}".format("Time"))
            for i in schtbl:
                j = 1
                
                print("{:>5}".format(j),"{:>11}".format(i[0]),"{:>25}".format(i[1]),"{:>10}".format(i[2]), "{:>8}".format(i[3]))
            print()
            n = int(input("Pick ScheduleID of movie you want to watch: "))
            cursor.execute("select * from moviescheduletbl where ScheduleID = {};".format(n))
            reqmovie = cursor.fetchall()[0]
            for i in range(3):
                d = {0:"A",1:"B",2:"C"}
                print("+----+ "*5)
                for j in range(5):
                    letter = d[i]
                    st = letter+str((j+1))
                    print("| {:>2} |".format(st),end = ' ')
                print()
                for j in range(5):
                    cursor.execute("select Status from MovieTransactionTbl where MovieId = {} and ScheduleID = {} and SeatID like '{}';".format(reqmovie[1],reqmovie[0],st))
                    tempstatus = cursor.fetchall()
                    status = tempstatus[0][0]
                    print("| {:>2} |".format(status),end = ' ')
                print()
                print("+----+ "*5)
                print()
            std = 500
            gold = 1000
            print("Rows A and B are Standard seats(Rs {}), Row C is Gold class(Rs {})".format(std,gold))
            num = int(input("Enter no. of seats you want to book: "))
            bill = 0
            for i in range(num):
                seat = input("Enter choice of seat: ")
                cursor.execute("select Status from MovieTransactionTbl where MovieId = {} and ScheduleID = {} and SeatID like '{}';".format(reqmovie[1],reqmovie[0],seat))
                tempstatus = cursor.fetchall()
                status = tempstatus[0]
                if status == "B":
                    print("Sorry, Seat is already Booked...")
                else:
                    cursor.execute("update MovieTransactionTbl set Status = 'B',EmailID = '{}' where MovieId = {} and ScheduleID = {} and SeatID like '{}';".format(email,reqmovie[1],reqmovie[0],seat))
                    cursor.execute("commit;")
                    print("Ticket has been booked...")
                    if seat[0] == 'C':
                        bill+=gold
                    else:
                        bill+=std
            print("Bill =",bill)

