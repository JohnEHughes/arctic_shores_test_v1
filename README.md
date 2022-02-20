Arctic Shores Tech Test v1.0

Program to answer the tech test using python and a SQLite database.

Execute the start() function to run the software.
This will print a text menu in the terminal window where the user will have the following options to select:

q) - quit the program
c) - create a candidate - this will ask for a name and a customer reference
s) - create a score - this will ask for a candidate reference and a score. This will use the given reference
        to store the score to.
f) - get candidate - this will take a candidate reference, and if found, will return the name, reference and scores.

There can be many candidate names, but only unique references, and many scores per reference.

The candidate names are not validated.
The scores are checked to make sure they are a number between 0 and 100 inclusive.
The reference is first checked by valid_reference() for the correct formatting. This means the length is checked to be 8 chars in length. Then the string is
is iterated over, with each character's unicode being checked to see if it is a letter or number.

