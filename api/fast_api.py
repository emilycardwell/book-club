from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
import pyrankvote as prv
from typing import List


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

    with open('data/ballots.csv', 'a') as final_ballots:
        writer = csv.writer(final_ballots)
        writer.writerow(sorted_items)
        final_ballots.close()

    return "Finished!"


@app.get("/get_results")
def get_results(count: str):

    ballots_raw = []

    with open('data/ballots.csv', 'r') as final_ballots:
        reader = csv.reader(final_ballots)
        c = 0
        for i in reader:
            ballots_raw.append(i)
            c += 1

        if int(count) < c:
            return f"Waiting for all other votes to be submitted... ({c}/3)"

        if int(count) > c:
            return f"Too many ballots have been submitted: ({c}/3)... press button below"

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
    with open('data/ballots.csv', 'w') as ballots:
        writer = csv.writer(ballots)
        ballots.close()

    return "Ballots Cleared!"


@app.get("/show_ballots")
def clear_ballots():
    ballots_raw = []

    with open('data/ballots.csv', 'r') as ballots:
        reader = csv.reader(ballots)
        for i in reader:
            ballots_raw.append(i)
        ballots.close()

    return ballots_raw

@app.get("/")
def root():
    return  {'greeting': 'Welcome to the Book Club Ranked Choice Voting API!'}
