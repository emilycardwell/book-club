import streamlit as st
from streamlit_sortables import sort_items
import requests

from data_editing import read_data


# VARIABLES
file_path = 'data/Feb2023.csv'
books = read_data(file_path)

# API CALLS
def api_write_ballot(ballot: list):
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/add_ballot'
    parameters = {'ballot': ballot}
    print(parameters)

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_get_results(count: int):
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/get_results'
    parameters = {'count': count}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_clear_ballots():
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/clear_ballots'

    try:
        response = requests.get(url).json()
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
    st.write(api_clear_ballots())
