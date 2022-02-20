import sqlite3, json
from validators import valid_reference, check_reference_exists

"""
Arctic Shores test v1.0
Author: J Hughes
Date: 20/02/22


Program written to answer the Arctic Shores tech test.
This uses this

A basic terminal start menu provides the interface with four options:
q) - quit the program
c) - create a candidate - this will ask for a name and a customer reference
s) - create a score - this will ask for a candidate reference and a score. This will use the given reference
        to store the score to.
f) - get candidate - this will take a candidate reference, and if found, will return the name, reference and scores.

"""


# Open the database and create a cursor
conn = sqlite3.connect("candidate.db")
c = conn.cursor()


# Function to create the initial table in the database, if one does not exist, else ignore.
def create_database():
    with conn:
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='candidate_table' ''')
        if not c.fetchone()[0]:
            c.execute("""CREATE TABLE candidate_table (
                    name text,
                    reference text,
                    scores real
                    )""")


# This is the main user interface - a basic while loop to capture a user's choice
def start():
    create_database()
    while True:
        options = input("Enter Candidate (c), Score (s), Fetch Data (f) or Quit (q): ")
        if options == 'q':
            break
        elif options == 'c':
            create_candidate()
        elif options == 's':
            create_score()
        elif options == 'f':
            get_candidate()
        else:
            print("Invalid input, please try again:")


""" **************************
Args - none
Return - none
Two inputs are gathered at the start, the reference is validated via valid_reference() and if valid, it is then
checked to see if it exists in the database. If exists, then message sent and returns back to the start.
If it does not exist, then a new record is stored in the database.
**************************"""
def create_candidate():
    name = input("Enter Candidate name: ")
    ref = input("Enter reference (letters/numbers 8 in length): ")
    scores = []

    if valid_reference(ref):
        score = json.dumps(scores)
        with conn:
            c.execute("SELECT * FROM candidate_table WHERE reference=?", (ref,))
            candidate_selected = c.fetchone()
            if not candidate_selected:
                c.execute("INSERT INTO candidate_table VALUES (?,?,?)", (name, ref, score))
                print(f"Candidate {name} has been saved to the database with Reference: {ref}")
            else:
                print("Reference already exists.")


""" **************************
Args - none
Return - none
Function to give a score to a candidate. First, it asks for a reference from the user which is then validated.
If the reference is correctly formatted, then it is passed to the check_reference_exists function to see if it exists
in the db. If it does, then it updates the candidate's score.
This is done by retrieving the score from the db, converting to a list, appending the new score, converting back to
JSON and then stored back in the db.
**************************"""
def create_score():
    ref = input("Enter Candidate reference: ")
    if not valid_reference(ref):
        print("Please enter a valid reference. ")
    else:
        with conn:
            candidate_selected = check_reference_exists(ref)
            if candidate_selected:
                scores = json.loads(candidate_selected[2])
                score = input("Please enter a score (0-100): ")
                try:
                    score = float(score)
                except ValueError:
                    print("Invalid score type.")
                else:
                    if 0 <= score <= 100:
                        scores.append(float(score))
                        scores = json.dumps(scores)
                        c.execute("UPDATE candidate_table SET scores=? WHERE reference=?", (scores, ref))
                        print(f"{score} has been added to the candidate with reference of {ref}.")
                    else:
                        print("Score must be between 0 and 100.")
            else:
                print("Reference does not exist")


""" **************************
Args - none
Return - none
Function to get a candidate record from the db. A user gives a reference and if it exists (checked via the
valid_reference() and check_reference_exists() functions), the function will print out the name,
reference and scores in a JSON format.
**************************"""
def get_candidate():
    ref = input("Enter Candidate reference: ")
    if valid_reference(ref):
        with conn:
            candidate_selected = check_reference_exists(ref)
            if candidate_selected:
                candidate_selected_dict = {
                    "candidate_ref": candidate_selected[1],
                    "name": candidate_selected[0],
                    "scores": candidate_selected[2]
                    }

                cand_json = json.dumps(candidate_selected_dict)
                print(cand_json)
            else:
                print("Reference does not exist")


# Execute start() to run the program
start()
