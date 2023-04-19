import pandas as pd
import csv
import pyrankvote as prv



# READ CSV & SEND CANDIDATES TO CSV
def read_data(file_path):
    with open(file_path, 'r') as file_path:
        books_df = pd.read_csv(file_path)

    sorted_df = books_df.sort_values('Book').reset_index(drop=True).loc[:, ['Book', 'Author']]

    items = []
    for key, data in sorted_df.iterrows():
        items.append(f'{data[0]} - {data[1].split()[-1]}')

    return items


def write_data(sorted_items):
    with open('ballots.csv', 'w') as final_ballots:
        writer = csv.writer(final_ballots)
        for book in sorted_items:
            writer.writerow(book)

    return "Finished!"


def get_results(count: int):
    ballots_raw = []

    with open('data/ballots.csv', 'r') as final_ballots:
        reader = csv.reader(final_ballots)
        c = 0
        for i in reader:
            ballots_raw.append(i)
            c += 1

        if int(count) != c:
            print(f"Waiting for all other votes to be submitted... ({c}/3)")

        final_ballots.close()

    books = []
    ballots = []

    j = 0
    for ballot_raw in ballots_raw:
        ballot_cand_form = []
        for book_raw in ballot_raw:
            book_form = prv.Candidate(book_raw)
            ballot_cand_form.append(book_form)
            if j == 0:
                books.append(book_form)
        ballots.append(prv.Ballot(ballot_cand_form))
        j += 1

    results = prv.instant_runoff_voting(books, ballots)
    print(results)
