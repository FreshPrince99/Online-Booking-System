import streamlit as st
import requests
from streamlit_lottie import st_lottie

import pandas as pd
import sqlalchemy


import pickle
from pathlib import Path

import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'pass123',database = 'school')
cursor = mycon.cursor(buffered = True)



st.header("Admin page")
password_admin = st.text_input("Enter password ")
enter = st.button("Enter")

special_pass="movie*admin*123"

if "enter_state" not in st.session_state:
    st.session_state.enter_state = False

def updation_rec():
    cursor.execute('select * from moviescheduletbl')
    schedule = cursor.fetchall()
    seats1 =['A1','A2','A3','A4','A5','B1','B2','B3','B4','B5','C1','C2','C3','C4','C5']
    cursor.execute('select scheduleid from movietransactiontbl')
    data2=cursor.fetchall()
    cursor.execute('select tranid from movietransactiontbl')
    data3=cursor.fetchall()
    max_tranid = data3[len(data3)-1]
    for i in schedule:
        if i[0] not in data2:
            movie = i[1]
            for j in seats1:
                s="insert into movietransactiontbl values('{}','{}','{}','{}','{}','{}')".format(max_tranid+1,movie,i[0],j,'NB','NULL')
                max_tranid+=1
                cursor.execute(s)
                mycon.commit()

updation_rec()

if enter or st.session_state.enter_state:
    st.session_state.enter_state = True
    if password_admin == special_pass:
        st.success('Welcome')
        engine = sqlalchemy.create_engine("mysql+pymysql://root:pass123@localhost/school")
        with st.container():
            st.header("User Login table")
            df = pd.read_sql_table("userlogin",engine)
            df

        with st.container():
            st.header("Id generation table")
            df = pd.read_sql_table("idgenerationtbl",engine)
            df

        with st.container():
            st.header("Movie table")
            df = pd.read_sql_table("movietbl",engine)
            df

        with st.container():
            st.header("Movie transaction table")
            df = pd.read_sql_table("movietransactiontbl",engine)
            df

        with st.container():
            st.header("Schedule table")
            df = pd.read_sql_table("moviescheduletbl",engine)
            df

        with st.container():
            st.header("Seat table")
            df = pd.read_sql_table("seattbl",engine)
            df

        
        with st.container():
            cursor.execute("show tables")
            tables_tuple= cursor.fetchall()
            st.header("Adding records")
            changes = st.selectbox("Select table",tables_tuple)   #for creating drop down
            changes_button= st.button("Edit")
            if "changes_button_state" not in st.session_state:
                st.session_state.changes_button_state = False

            if changes_button or st.session_state.changes_button_state:
                st.session_state.changes_button_state = True


                if changes[0] == 'idgenerationtbl':
                    m_id = st.text_input("Enter the movie id ")
                    s_id=st.text_input("Enter the scheduled id ")
                    t_id=st.text_input("Enter the transaction id")
                    idgen_button= st.button("edit")
                    if "idgen_button_state" not in st.session_state:
                        st.session_state.idgen_button_state = False

                    if idgen_button or st.session_state.idgen_button_state:
                        cursor.execute("insert into idgenerationtbl values('{}','{}','{}')".format(m_id,s_id,t_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()

                elif changes[0] == 'movietbl':
                    m_id = st.text_input("Enter the movie id ")
                    mname_id=st.text_input("Enter the name of the movie ")
                    start_id=st.text_input("Enter the start date")
                    end_id=st.text_input("Enter the end date")
                    a_id=st.text_input("Enter active status(Y/N) of the movie")
                    movietb_button= st.button("edit")
                    if "movietb_button_state" not in st.session_state:
                        st.session_state.movietb_button_state = False

                    if movietb_button or st.session_state.movietb_button_state:
                        cursor.execute("insert into movietbl values('{}','{}','{}','{}','{}')".format(m_id,mname_id,start_id,end_id,a_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()

                elif changes[0] == 'movietransactiontbl':
                    t_id=st.text_input("Enter transaction id ")
                    m_id = st.text_input("Enter the movie id ")
                    s_id=st.text_input("Enter the schedule id ")
                    seat_id=st.text_input("Enter the seat id")
                    status_id=st.text_input("Enter the status")
                    email_id=st.text_input("Enter email")
                    transac= st.button("edit")
                    if "transac_state" not in st.session_state:
                        st.session_state.transac_state = False

                    if transac or st.session_state.transac_state:
                        cursor.execute("insert into movietransactiontbl values('{}','{}','{}','{}','{}','{}')".format(t_id,m_id,s_id,seat_id,status_id,email_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()

                    updation_rec()


                elif changes[0] == 'moviescheduletbl':
                    s_id=st.text_input("Enter the schedule id ")
                    movie_id=st.text_input("Enter the movie id")
                    date_id=st.text_input("Enter the date")
                    time_id=st.text_input("Enter time")
                    sched= st.button("edit")
                    if "sched_state" not in st.session_state:
                        st.session_state.sched_state = False

                    if sched or st.session_state.sched_state:
                        cursor.execute("insert into moviescheduletbl values('{}','{}','{}','{}','{}')".format(s_id,movie_id,date_id,time_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()

                elif changes[0] == 'seattbl':
                    s_id=st.text_input("Enter the schedule id ")
                    price_id=st.text_input("Enter the price")
                    seat123= st.button("edit")
                    if "seat123_state" not in st.session_state:
                        st.session_state.seat123_state = False

                    if seat123 or st.session_state.seat123_state:
                        cursor.execute("insert into seattbl values('{}','{}')".format(s_id,price_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()

                elif changes[0] == 'userlogin':
                    email_id=st.text_input("Enter email id")
                    name=st.text_input("Enter the name ")
                    pass_special=st.text_input("Enter the password ")
                    type_id=st.text_input("Enter the type")
                    sched= st.button("edit")
                    if "sched_state" not in st.session_state:
                        st.session_state.sched_state = False

                    if sched or st.session_state.sched_state:
                        cursor.execute("insert into userlogin values('{}','{}','{}','{}')".format(email_id,name,pass_special,type_id))
                        cursor.execute("commit;")
                        st.success("Record has been added!")
                        st.balloons()
                
                        



