import streamlit as st
import requests
from streamlit_lottie import st_lottie

import pickle
from pathlib import Path
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root',password = 'pass123',database = 'school')
cursor = mycon.cursor(buffered = True)



#SIGNUP PAGE


st.set_page_config(page_title="Login/Signup", page_icon=":movie_camera:", layout="wide")
st.title("Greetings fellow passerby..")
st.write("Please enter your details below to get started")
st.sidebar.success("Select a page above")

st.header("Signup")

email = st.text_input("Enter email ")
name = st.text_input("Enter your name ")
password = st.text_input("Enter the password you wish to keep ")
go = st.button("Go!")
if go:
    Type = 'C'
    cursor.execute("select * from UserLogin where EmailID like '{}';".format(email))
    if cursor.rowcount == 0:
        cursor.execute("insert into UserLogin values('{}','{}','{}','{}');".format(email,name,password,Type))
        cursor.execute('commit')
        st.success("successfully signed up...")
        st.write("Please procced to the login page to get started")
    else:
        st.write("Email already exists, want to login instead? ")










