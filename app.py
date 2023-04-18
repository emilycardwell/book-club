import streamlit as st
from streamlit_sortables import sort_items


from data_editing import read_data, write_data, get_results


# VARIABLES
file_path = 'data/Feb2023.csv'
items = read_data(file_path)


# STREAMLIT APP
st.markdown(
    """
    # Book Club Ranked Choice App

    Rearrange the titles below (first place on top, last place on bottom)
    """
)

sorted_items = sort_items(items, header=None, direction='vertical')

if st.button('Done'):
    st.write(write_data(sorted_items))
else:
    st.write("click button above to record answers")
