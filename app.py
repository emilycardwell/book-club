import pandas as pd
import os
import streamlit as st
import streamlit_sortables as ss
import pyrankvote
from pyrankvote import Candidate, Ballot

# VARIABLES
data_path = os.environ['DATA_PATH']
file_name = 'April_ALE.csv'
file_path = f'{data_path}/{file_name}'

# READ CSV & CLEAN
feb_df = pd.read_csv(file_path)
sorted_df = feb_df.sort_values('Book').reset_index(drop=True).loc[:, ['Book', 'Author']]
sorted_df.head()

items = []
for key, data in sorted_df.iterrows():
    items.append(f'{data[0]} - {data[1]}')

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


sorted_books = ss.sort_items(items, header=None, direction='vertical')

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
