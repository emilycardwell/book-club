import streamlit as st
from streamlit_sortables import sort_items
import requests
import re

from data_editing import read_data


# VARIABLES
file_path = 'data/ALE_Apr2023.csv'
books = read_data(file_path)
people = 3


# API CALLS
def api_write_ballot(sorted_items: list):
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/add_ballot'
    parameters = {'sorted_items': sorted_items}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_undo_ballot():
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/undo_ballot'

    try:
        response = requests.get(url).json()
    except:
        response = 'Input Error, try again'

    return response

def api_get_results():
    url = 'https://book-club-zkfrzn26zq-oa.a.run.app/get_results'
    parameters = {'count': people}

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

ballots_form = []
for a in ballot:
    b = a.lower()
    c = b.replace(' - ', '-')
    d = c.replace(' ', '_')
    e = re.sub(r'[^\w\s_-]', '', d)
    ballots_form.append(e)

if st.button('Record Answers'):
    st.write(api_write_ballot(ballots_form))

if st.button('Undo Ballot'):
    st.write(api_undo_ballot())

if st.button('Get Results'):
    st.write(api_get_results(3))

if st.button("Clear All Ballots"):
    st.write(api_clear_ballots())
