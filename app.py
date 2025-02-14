import streamlit as st
from streamlit_sortables import sort_items
import requests
import re
import os

from data_editing import read_data

gcr_url = "https://book-club-971132514441.europe-west4.run.app"

# VARIABLES
file_path = 'test_data/test_options.csv'
books = read_data(file_path)

# API CALLS
def api_write_ballot(sorted_items: list):
    url = f'{gcr_url}/add_ballot'
    parameters = {'sorted_items': sorted_items}
    response = requests.get(url, params=parameters).json()
    return response

def api_undo_ballot():
    url = f'{gcr_url}/undo_ballot'
    response = requests.get(url).json()
    return response


def api_get_results():
    url = f'{gcr_url}/get_results'
    response = requests.get(url).json()
    if type(response) == str:
        return response
    else:
        winner = response[0]['name'].replace('_', ' ').replace('-', ' - ').title()
        return f"The winner is: {winner}"


def api_clear_ballots():
    url = f'{gcr_url}/clear_ballots'
    response = requests.get(url).json()
    return response


# STREAMLIT APP
st.markdown(
    """
    # Ranked Choice Voting for Book Club
    ### This is a sample ballot. You can test the results by submitting a 2-3 times,\
    then clicking 'Get Results.'
    ##
    Rearrange the titles below: 1st place on top, last-place on bottom
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

st.markdown('###')

if st.button('Submit Answers', type='primary'):
    st.write(api_write_ballot(ballots_form))

if st.button('Undo Ballot', type='secondary'):
    st.write(api_undo_ballot())

st.markdown('##')

if st.button('Get Results', type='primary'):
    st.write(api_get_results())

if st.button("Clear All Ballots", type='secondary'):
    st.write(api_clear_ballots())
