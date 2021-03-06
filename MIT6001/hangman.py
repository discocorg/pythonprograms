# Problem Set 2, hangman.py
# MIT60001 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if all((c in letters_guessed) for c in secret_word ):
        return True
    else:
        return False

#def test_answer():
#    assert is_word_guessed('bonk', (b,o,n,k) == True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    chosen_word=choose_word(wordlist)
    guessed_word = ""
    for c in secret_word:
        if c in letters_guessed:
            guessed_word += c
        else:
            guessed_word += "_ "
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    #solution below is inefficient because it allocates space for a new string with each iteration.
    #Better to go with available_letters = available_letters.translate({ord(c): None for c in 'letters_guessed'})
    available_letters = string.ascii_lowercase
    for c in letters_guessed: 
        if c in available_letters:
            available_letters = available_letters.replace(c,"")
    return available_letters 
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    guesses = 6
    warnings = 3
    letters_remaining = ""
    letter_guess = ''
    letters_guessed = []
    vowels = "aeiou"
    print("Let's play Hangman! The secret word has " + str(len(secret_word)) + " letters in it.")
    
    while True:
        print("-------------")
        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(secret_word)#Need to update so score is guesses * unique characters in secret_word
            print("Congratulations, you won!")
            print("Your total score for this game is: " + str(score))
            break
        elif guesses <= 0: 
            print("Sorry you ran out of guesses, the word was " + secret_word)
            break
        else:
            letters_remaining = get_available_letters(letters_guessed)
            print("You have " + str(guesses) + " letter guesses remaining and these letters to guess from: "+ letters_remaining)
            letter_guess = (input("Please supply your guess(letter): ")).lower()
            if not letter_guess.isalpha():
                if warnings > 0:
                    warnings -= 1
                    print("You didn't guess a letter and lose a guess, you have " +str(warnings) + " warnings remaining.")
                else: 
                    guesses -= 1
                    print("You didn't guess a letter and lose a guess.")
            else:
                if letter_guess in secret_word:
                    if letter_guess in letters_guessed:
                        if warnings > 0:
                            warnings -= 1
                            print("That letter has already been guessed you lose a warning, you have " +str(warnings) + " warinings remaining.")
                        else:
                            guesses -= 1
                            print("That letter has already been guessed you lose a guess because you've run out of warnings.")
                        
                    else:
                        guesses -= 1
                        letters_guessed.append(letter_guess)
                        current_word = get_guessed_word(secret_word, letters_guessed)
                        print("Good guess: " + current_word)
                else:
                    if letter_guess in vowels:
                        current_word = get_guessed_word(secret_word, letters_guessed)
                        print("Oops! That letter is not in my word: " + current_word)
                        guesses = guesses - 2
                    else:
                        current_word = get_guessed_word(secret_word, letters_guessed)
                        print("Oops! That letter is not in my word: " + current_word)
                        guesses -= 1
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.strip()
    my_word = my_word.replace(" ", "")
    if len(my_word) != len(other_word):
        return False
    else:
        linkchars = zip(my_word, other_word)
        for a,b in linkchars:
            if a!=b:
                if a=='_':
                    pass
                else: 
                    return False
        return True
#Test classes for match_with_gaps
def test_too_long():
    assert match_with_gaps("bonkaa","bonk") == False

def test_not_match():
    assert match_with_gaps("bo_r","bonk") == False

def test_match_w_space():
    assert match_with_gaps("r___","room") == True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    printwordlist = ""
    for pword in wordlist:
        pword = pword.strip()
        #print(pword)
        #print(my_word)
        if match_with_gaps(my_word,pword):
            print("Match found!")
            printwordlist = printwordlist + " " + pword
    print(printwordlist)

    
def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    guesses = 6
    warnings = 3
    letters_remaining = ""
    letter_guess = ''
    letters_guessed = []
    vowels = "aeiou"
    print("Let's play Hangman! The secret word has " + str(len(secret_word)) + " letters in it.")
    
    while True:
        print("-------------")
        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(secret_word)#Need to update so score is guesses * unique characters in secret_word
            print("Congratulations, you won!")
            print("Your total score for this game is: " + str(score))
            break
        elif guesses <= 0: 
            print("Sorry you ran out of guesses, the word was " + secret_word)
            break
        else:
            letters_remaining = get_available_letters(letters_guessed)
            print("You have " + str(guesses) + " letter guesses remaining and these letters to guess from: "+ letters_remaining)
            letter_guess = (input("Please supply your guess(letter): ")).lower()
            if letter_guess == '*':
                word_possible = get_guessed_word(secret_word, letters_guessed)
                show_possible_matches(word_possible)
            else:
                if not letter_guess.isalpha():
                    if warnings > 0:
                        warnings -= 1
                        print("You didn't guess a letter and lose a guess, you have " + str(warnings) + " warnings remaining.")
                    else: 
                        guesses -= 1
                        print("You didn't guess a letter and lose a guess.")
                else:
                    if letter_guess in secret_word:
                        if letter_guess in letters_guessed:
                            if warnings > 0:
                                warnings -= 1
                                print("That letter has already been guessed you lose a warning, you have " + str(warnings) + " warinings remaining.")
                            else:
                                guesses -= 1
                                print("That letter has already been guessed you lose a guess because you've run out of warnings.")
                        else:
                            guesses -= 1
                            letters_guessed.append(letter_guess)
                            current_word = get_guessed_word(secret_word, letters_guessed)
                            print("Good guess: " + current_word)
                    else:
                        if letter_guess in vowels:
                            current_word = get_guessed_word(secret_word, letters_guessed)
                            print("Oops! That letter is not in my word: " + current_word)
                            guesses = guesses - 2
                        else:
                            current_word = get_guessed_word(secret_word, letters_guessed)
                            print("Oops! That letter is not in my word: " + current_word)
                            guesses -= 1

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
