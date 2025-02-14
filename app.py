import streamlit as st
from streamlit_sortables import sort_items
import requests
import re
import os

from data_editing import read_data

gcr_url = os.getenv('GCR_URL')

# VARIABLES
file_path = 'test_data/test_options.csv'
books = read_data(file_path)


def catch_error(url, parameters=None):
    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'
    return response

# API CALLS
def api_write_ballot(sorted_items: list):
    url = f'{gcr_url}/add_ballot'
    parameters = {'sorted_items': sorted_items}
    return catch_error(url, parameters)

def api_undo_ballot():
    url = f'{gcr_url}/undo_ballot'
    return catch_error(url)


def api_get_results():
    url = f'{gcr_url}/get_results'
    response =  catch_error(url)

    try:
        winner = dict(response[1])
        return winner['name']
    except:
        return f'Incorrect results format: {response}'



def api_clear_ballots():
    url = f'{gcr_url}/clear_ballots'
    return catch_error(url)


# STREAMLIT APP
st.markdown(
    """
    # Ranked Choice Voting for Book Club
    ### This is a sample ballot. You can test the results by submitting a few times,\
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
