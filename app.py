import pandas as pd
import os
import streamlit as st
from streamlit_sortables import sort_items
import pyrankvote
from pyrankvote import Candidate, Ballot

# VARIABLES
file_path = 'data/Feb2023.csv'

# READ CSV & CLEAN
def read_data(file_path):
    with open(file_path, 'r') as file_path:
        feb_df = pd.read_csv(file_path)

    sorted_df = feb_df.sort_values('Book').reset_index(drop=True).loc[:, ['Book', 'Author']]

    items = []
    for key, data in sorted_df.iterrows():
        items.append(f'{data[0]} - {data[1]}')

    return (items)

items = read_data(file_path)

books = []
for i in items:
    books.append(Candidate(i))


# STREAMLIT APP
st.markdown(
    """
    # Book Club Ranked Choice App

    Rearrange the titles below (first place on top, last place on bottom)
    """
)


sorted_books = sort_items(items, header=None, direction='vertical')

submissions = 0
ballots = []
if st.button('Done'):
    ballots.append(Ballot(ranked_candidates=sorted_books))
    st.write("Finished!")
    submissions += 1
else:
    st.write("click button above to record answers")


# DO RANKED CHOICE VOTE
if submissions == 3:
    st.write("All participants have voted!")
    results = pyrankvote.instant_runoff_voting(books, ballots)
    winner = results.get_winners()
    st.write(results)
    st.write("The winner is:")
    st.write(winner)
else:
    st.write("Waiting for all votes to be submitted...")
