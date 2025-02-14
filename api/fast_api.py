from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
import pyrankvote as prv
from typing import List

people = 3
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/add_ballot")
def add_ballot(sorted_items: List[str] = Query(None)):

    n = 0
    with open('test_data/test_ballots.csv', 'r') as final_ballots:
        reader = csv.reader(final_ballots)
        for i in reader:
            n += 1

    with open('test_data/test_ballots.csv', 'a') as final_ballots:
        writer = csv.writer(final_ballots)
        writer.writerow(sorted_items)
        final_ballots.close()

    n2 = 0
    with open('test_data/test_ballots.csv', 'r') as final_ballots:
        reader = csv.reader(final_ballots)
        for i in reader:
            n2 += 1

    if n+1 == n2:
        return "Finished!"
    else:
        return "Ballot not recorded, please press button again"


@app.get("/undo_ballot")
def add_ballot():

    undo_ballots = []
    with open('test_data/test_ballots.csv', 'r') as ballots:
        reader = csv.reader(ballots)
        for i in reader:
            undo_ballots.append(i)
        ballots.close()

    with open('test_data/test_ballots.csv', 'w') as ballots:
        writer = csv.writer(ballots)
        for j in range(len(undo_ballots)-1):
            writer.writerow(undo_ballots[j])
        ballots.close()

    return "Last ballot cleared!"


@app.get("/get_results")
def get_results():

    ballots_raw = []

    with open('test_data/test_ballots.csv', 'r') as final_ballots:
        reader = csv.reader(final_ballots)
        b = 0
        for i in reader:
            ballots_raw.append(i)
            b += 1

        if people > b:
            return f"Waiting for all other votes to be submitted... ({b}/{people})"

        if people < b:
            return f"Too many ballots have been submitted: ({b}/{people})... press button below"

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

    winner = results.get_winners()

    return "All participants have voted!", winner[0]


@app.get("/clear_ballots")
def clear_ballots():
    with open('test_data/test_ballots.csv', 'w') as ballots:
        writer = csv.writer(ballots)
        ballots.close()

    return "Ballots Cleared!"


@app.get("/show_ballots")
def clear_ballots():
    ballots_raw = []

    with open('test_data/test_ballots.csv', 'r') as ballots:
        reader = csv.reader(ballots)
        for i in reader:
            ballots_raw.append(i)
        ballots.close()

    return ballots_raw

@app.get("/")
def root():
    return  {'greeting': 'Welcome to the Book Club Ranked Choice Voting API!'}
