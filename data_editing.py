import pandas as pd
from pyrankvote import Candidate, Ballot
import csv
import pyrankvote



# READ CSV & SEND CANDIDATES TO CSV
def read_data(file_path):
    with open(file_path, 'r') as file_path:
        feb_df = pd.read_csv(file_path)

    sorted_df = feb_df.sort_values('Book').reset_index(drop=True).loc[:, ['Book', 'Author']]

    items = []
    for key, data in sorted_df.iterrows():
        items.append(f'{data[0]} - {data[1].split()[-1]}')

    with open('candidates.csv', 'w') as candidates:
        writer = csv.writer(candidates, delimiter=' ', quotechar='|')
        for book in items:
            writer.writerow(book)

    return items


def write_data(sorted_items):
    with open('ballots.csv', 'w') as final_ballots:
        writer = csv.writer(final_ballots, delimiter=' ', quotechar='|')
        for book in sorted_items:
            writer.writerow(book)

    return "Finished!"


def get_results():
    ballots = []
    with open('ballots.csv', 'w') as final_ballots:
        reader = csv.reader(final_ballots, delimiter=' ', quotechar='|')
        for ballot in reader:
            ballot = []
            for choice in ballot:
                book = Candidate(choice)
                ballot.append(book)
            ballots.append(Ballot(ballot))

    l = len(ballots)
    if l < 3:
        return f"Waiting for all other votes to be submitted... ({l}/3)"

    books = []
    with open('candidates.csv', 'r') as candidates:
        reader = csv.reader(candidates, delimiter=' ', quotechar='|')
        for book in reader:
            books.append(Candidate(book))

    results = pyrankvote.instant_runoff_voting(books, ballots)

    # winner = results.get_winners()

    return "All participants have voted! Results: /n", results
