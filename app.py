import streamlit as st
from streamlit_sortables import sort_items
import requests

from data_editing import read_data


# VARIABLES
file_path = 'data/Feb2023.csv'
books = read_data(file_path)

# API CALLS
@st.cache(suppress_st_warning=True)
def api_write_ballot(ballot: list):
    url = 'https://localhost:8000/add_ballot'
    parameters = {'ballot': ballot}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_get_results(count: int):
    url = 'http://localhost:8000/get_results'
    parameters = {'count': count}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_clear_ballots(file_path: str):
    url = 'http://localhost:8000/clear_ballots'
    parameters = {'file_path': file_path}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response


# STREAMLIT APP
st.markdown(
    """
    # Book Club Ranked Choice App

    Rearrange the titles below (first-place on top, last-place on bottom)
    """
)

ballot = sort_items(books, header=None, direction='vertical')


if st.button('Record Answers'):
    st.write(api_write_ballot(ballot))

if st.button('Get Results'):
    st.write(api_get_results(3))

if st.button("Don't Press Me"):
    st.write(api_clear_ballots(file_path))
