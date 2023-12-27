import csv
import sys


def main():

    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        print("Incorrect number of command-line arguments!")
        return 1

    # TODO: Read database file into a variable

    database_file = sys.argv[1]

    database = []

    with open(database_file, 'r') as dfile:
        reader = csv.DictReader(dfile)

        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable

    sequence_file = sys.argv[2]

    sequence = None

    with open(sequence_file, 'r') as sfile:
        sequence = sfile.read()

    # TODO: Find longest match of each STR in DNA sequence

    # Get all the keys and remove name, leaving a list of all STRS
    strs = [k for k in database[0].keys()][1:]


    matches = {}

    for s in strs:
        # Add strs and their count (as strings(important)) to matches
        matches[s] = str(longest_match(sequence, s))


    # TODO: Check database for matching profiles
    length = len(database)

    i = 0

    # Go through every person in the database
    for i in range(0 , length):

        # Get info of current person
        gene_info = database[i]

        # Store their name
        name = gene_info["name"]

        # Remove name from the info
        # So that the STRs can be compared
        del gene_info["name"]

        # If the STRs match, print the name and exit
        if gene_info == matches:
            print(name)
            return
        i += 1


    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
