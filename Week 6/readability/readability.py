from cs50 import get_string

def main():
    text = get_string("Text: ")
    grade = cli(text)


    if grade >= 16:
        print("Grade 16+")

    elif grade < 1:
        print("Before Grade 1")

    else:
        print(f"Grade {grade}")



def cli(text):
    letters, words, sentences = letters_words_sentences(text)

    # index = 0.0588 * L - 0.296 * S - 15.8

    l = letters / words * 100
    s = sentences / words * 100

    index = round(((0.0588 * l) - (0.296 * s) - 15.8))

    return index


def letters_words_sentences(text):
    i = 0
    length = len(text)

    # Corner case if an empty string is recieved
    if length > 0:
        words = 1
    else:
        words = 0

    letters = 0
    sentences = 0

    while i < length:

        # Letters
        if text[i].isalpha():
            letters += 1

        # Sentences
        if text[i] in ['.', '!', '?']:
            sentences += 1

        # Words
        if text[i].isspace():
            words += 1

        i += 1


    return letters, words, sentences


if __name__ == "__main__":
    main()
