import streamlit as st
import requests
from streamlit_lottie import st_lottie

from pathlib import Path
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'pass123',database = 'school')
cursor = mycon.cursor(buffered = True)



#FIRST PAGE AFTER LOGIN/SIGNUP
def first_page():

    def load_lottieurl(url):
        r= requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    #ANIMATIONS
    lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_khzniaya.json")



    #HEADER SECTION FOR THE WEBSITE
    with st.container():
        st.subheader("Discover new paths :trident:")
        st.title(" Movie website ")
        st.write("Booking made easier :tada:")

    #DESCRIPTION SECTION

    with st.container():
        st.write("---")
        left_column,right_column = st.columns(2)
        with left_column:
            st.header("A Brief summary ")
            st.write(
                    """
                    
                    - This website has been created for making movie booking much more simpler
                    - The entire website has been created by making use of Python
                    - Head below to the movie section to select the movie and timings 
                    . Have fun!
                    
                    """
                )

        with right_column:
            st_lottie(lottie_coding, height =300, key="coding")


    #DISPLAY MOVIES AVAILABLE FROM MOVIETBL TABLE IN SQL
    with st.container():
        st.write("---")
        st.header("Movies available ")
        cursor.execute("select * from movietbl where Active like 'y';")
        tbl = cursor.fetchall()
        movie_id,movie_name,start,end_d= st.columns(4)
        with movie_id:
            st.header("Movie Id")
            for i in tbl:
                st.write(i[0])
        with movie_name:
            st.header("Name")
            for i in tbl:
                st.write(i[1])
        with start:
            st.header("Start date")
            for i in tbl:
                st.write(i[2])
        with end_d:
            st.header("End date")
            for i in tbl:
                st.write(i[3])

    
    #DISPLAY LIST OF MOVIE AND TIMINGS USING MOVIESCHEDULE TABLE
    with st.container():
        if "search_state" not in st.session_state:
            st.session_state.search_state = False
        st.write("---")
        st.header("Book a movie!")
        cursor.execute("select * from movietbl where Active like 'y';")
        options= cursor.fetchall()
        movie_list=[]
        for i in options:
            movie_list.append(i[1])
        option_movie = st.selectbox("Choose movie",movie_list)
        search = st.button("Search for availability")
        if search or st.session_state.search_state:
            st.session_state.search_state = True
            for el in options:
                if el[1]== option_movie:
                    movie_id_search = el[0]
                    break
            cursor.execute("select date,time from moviescheduletbl where movieid='{}'".format(movie_id_search))
            timings= cursor.fetchall()
            if len(timings) == 0:
                st.write("Sorry no movies available in your area ")
            else:
                if "timing_button_state" not in st.session_state:
                    st.session_state.timing_button_state = False
                timing_options = st.selectbox("Select timing",timings)
                timing_button = st.button("Select")


                #DISPLAYING SEATS BOOKED AND AVAILABLE
                if timing_button or st.session_state.timing_button_state:
                    st.session_state.timing_button_state = True
                    cursor.execute("select * from moviescheduletbl where date = '{}' and time = '{}'".format(timing_options[0],timing_options[1]))
                    reqmovie = cursor.fetchall()[0]
                    st.write(reqmovie)
                    for i in range(3):
                        d = {0:"A",1:"B",2:"C"}
                        st.write("+----+ "*5)
                        temp_seats=''
                        temp_seats1=''
                        for j in range(5):
                            letter = d[i]
                            st1 = letter+str((j+1))
                            temp_seats +="| {:>2} |".format(st1)+'  '
                        st.write(temp_seats)
                        for j in range(5):
                            cursor.execute("select Status from MovieTransactionTbl where MovieId = {} and ScheduleID = {} and SeatID like '{}';".format(reqmovie[1],reqmovie[0],st1))
                            tempstatus = cursor.fetchall()
                            status = tempstatus[0][0]
                            temp_seats1 += "| {:>2} |".format(status)+'  '
                        st.write(temp_seats1)
                        st.write("+----+ "*5)
                        st.write()


                    with st.container():
                        cursor.execute("select seatid from movietransactiontbl where status = 'NB'")
                        seat_options= cursor.fetchall()
                        if "seat_button_state" not in st.session_state:
                            st.session_state.seat_button_state = False
                        std = 500
                        gold = 1000
                        st.write("Rows A and B are Standard seats(Rs {}), Row C is Gold class(Rs {})".format(std,gold))
                        seats = st.multiselect("Select the seats you want",seat_options)
                        seat_button = st.button("Select seat")

                        if seat_button or st.session_state.seat_button_state:
                            st.session_state.seat_button_state = True
                            bill=0
                            for seat1 in seats:
                                if 'C' in seat1[0]:
                                    bill+=gold
                                else:
                                    bill+=std
                                cursor.execute("update MovieTransactionTbl set Status = 'B',EmailID = '{}' where MovieId = {} and ScheduleID = {} and SeatID like '{}';".format(email,reqmovie[1],reqmovie[0],seat1[0]))
                                cursor.execute("commit;")
                            st.success("Ticket has been booked...")
                            st.header("Thank you for your purchase! :)")
                            st.balloons()
                            st.header("Final price is ",bill)

                            
                    
                    


if "submit_state" not in st.session_state:
    st.session_state.submit_state = False

st.header("Welcome back!")
email = st.text_input("Enter email ")
password = st.text_input("Enter password ")
submit = st.button("Submit")
if submit or st.session_state.submit_state:
    st.session_state.submit_state = True
    cursor.execute("select * from UserLogin where EmailID like '{}';".format(email))
    if cursor.rowcount == 0:
        st.error("Email does not exist, Try signing up instead ")
    else:
        cursor.execute("select * from UserLogin where EmailID like '{}' and Password like '{}';".format(email,password))
        if cursor.rowcount == 0:
            st.error("Password is wrong. please re-enter password...")
        else:
            st.success("Successfully logged in...")
            first_page()

