import sqlite3



"""
Two functions to help the main.py functions to validate the reference variable.
"""

# Open the database and create a cursor
conn = sqlite3.connect("candidate.db")
c = conn.cursor()


""" **************************
Args - ref - str
Return - Bool

A validation function that takes the reference as an argument, checks the length is equal to 8 and then
if it is made up of only letters and numbers. If either of these steps fail, a relevant message is sent to the user
explaining why.
**************************"""
def valid_reference(ref):
    if len(ref) != 8:
        print("Reference must be 8 characters long.")
        return False
    else:
        count = 0
        for i in ref:
            if (57 >= ord(i) >= 48) or (90 >= ord(i) >= 65) or (122 >= ord(i) >= 97):
                count += 1
                if count == 8:
                    return True
            else:
                print("Reference must be only letters/digits.")
                return False


""" **************************
Args - ref - str
Return - either DB row or False
This function takes the reference as an argument and checks the database to see if it exists. If it does it
messages the user and return the record.
If not, then it returns False

**************************"""
def check_reference_exists(ref):
    with conn:
        c.execute("SELECT * FROM candidate_table WHERE reference=?", (ref,))
        candidate_selected = c.fetchone()
        if candidate_selected:
            print("Reference exists...")
            return candidate_selected
        return False