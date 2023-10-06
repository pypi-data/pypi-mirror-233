# Imports
import streamlit as st
import datetime


# A simple function
def add_one(number):
    print("***Running add_one within amuni")
    return number + 1


# Mainline code - runs as soon as this file is imported or invoked
# Function code runs only on an explicit invocation
print("***Running amuni mainline")

now = datetime.datetime.now()
formatted_now = now.strftime("Current date and time: %Y-%m-%d %H:%M:%S")

# Write to the streamlit app
st.title("My sample python repository")
st.write("Hey there! ", formatted_now)
# Write to console
print()
print(formatted_now)
print()
print("***Leaving amuni mainline")
