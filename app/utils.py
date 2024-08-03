import random

def return_secret_word():
    uniqueLetters = []
    word = random.choices((open("src/filtered_words.txt", "r")).readlines())[
            0].strip("\n").upper()

    for letter in word:
        if letter not in uniqueLetters:
            uniqueLetters.append(letter)

    if len(uniqueLetters) > 6:
        return_secret_word()
    else:
        return word