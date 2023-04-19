import streamlit as st
from streamlit_sortables import sort_items
import requests

from data_editing import read_data, write_data, get_results


# VARIABLES
file_path = 'data/Feb2023.csv'
books = read_data(file_path)

# API CALLS
@st.cache(suppress_st_warning=True)
def api_write_ballot(ballot: list):
    url = '/add_ballot'
    parameters = {}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

def api_get_results(count: int):
    url = '/get_results'
    parameters = {}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response


# STREAMLIT APP
st.markdown(
    """
    # Book Club Ranked Choice App

    Rearrange the titles below (first place on top, last place on bottom)
    """
)

ballot = sort_items(books, header=None, direction='vertical')


if st.button('Record Answers'):
    st.write(api_write_ballot(ballot))


st.write(get_results(file_path))
