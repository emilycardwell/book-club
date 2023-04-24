from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
import pyrankvote as prv



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/add_ballot")
def add_ballot(sorted_items: str):
    with open('data/ballots.csv', 'a') as final_ballots:
        writer = csv.writer(final_ballots)
        writer.writerow(list(sorted_items))
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

        if int(count) != c:
            return f"Waiting for all other votes to be submitted... ({c}/3)"

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

    return "All participants have voted! Results: /n", results


@app.get("/clear_ballots")
def clear_ballots():
    with open('data/ballots.csv', 'w') as candidates:
        writer = csv.writer(candidates)
        candidates.close()

    return "Ballots Cleared!"

@app.get("/")
def root():
    return  {'greeting': 'Welcome to the Book Club Ranked Choice Voting API!'}
