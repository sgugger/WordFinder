"""
Created on Mon Jan 29 08:27:26 2018
On a random grid of letters, find the word that's worth the most of points.
A word can be drawn going in any direction (even diagonals), changing direction
at any time is allowed, the only thing that isn't is to use the same letter 
twice.
The score of a word is the sum of the scores of the letters (depending on their
frequency) multiplied by its length minus two.
Example of use (have the dictionary in the same directory as the python file):
generate_grid()
search()
"""

import math
import random

dictionary = []#global variable containing the list of possible words.
percents = []#global variable containing the frequency of the 26 letters.
grid = []#global variable containing the gridd of letters.

def read_dictionary():
    """
    Open the dictionary, puts all the world in the global list of the same
    name and compute the frequencieseach letter appears.
    We assume the dictionary has the name dictionary.txt and is in the same 
    directory as the python file.
    """
    global dictionary
    global percents
    file = open("dictionary.txt")
    num_chars = 0
    percents = [0]*26
    for line in file:
        #Delete the last character (\n) to get the word.
        word = str.lower(line[0:-1])
        dictionary.append(word)
        #Add 1 in the list percents for each corresponding letter in the word.
        num_chars += len(word)
        for letter in word:
            percents[letter_index(letter)] += 1
    #percents contains the letters count at this point, so we divide it by
    #num_chars
    for i in range(26):
        percents[i] /= num_chars
    file.close()

def letter_index(char):
    """
    Returns the position of char in the alphabet
    char -- a lowcase character
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet.index(char)

def get_score(word):
    """
    Computes the score attributed to a word
    word -- a word in lowcase (only the 26 regular characters)
    """
    S = 0
    for letter in word:
        #The score of a letter is proportional to its rarity
        scr = int(0.05/percents[letter_index(letter)]) + 1
        #crop scores at 25
        if scr > 25:
            scr = 25
        S += scr
    return S * (len(word)-2)

def pull_random_letter():
    """
    Pulls a random letter. Each letter has the same chance of appearing as its
    frequency in the dictionary.
    """
    x = random.uniform(0,1)
    cum_sum = percents[0]
    idx =0
    while idx < 25 and cum_sum < x:
        idx += 1
        cum_sum+= percents[idx]
    return "abcdefghijklmnopqrstuvwxyz"[idx]

def generate_grid(d=7):
    """
    Generates a random grid of letters of size dxd, stored in a list, line 
    after line.
    d -- size of the grid
    """
    read_dictionary()
    global grid
    grid = []
    for i in range (d*d):
        grid.append(pull_random_letter())
    print_grid()

def print_grid():
    """
    Prints the grid
    """
    d = int(math.sqrt(len(grid)))
    out = " " + "-" * (2*d-1) + " \n"
    for i in range(d):
        out += "|"
        for j in range(d):
            out += grid[d*i + j] + "|"
        out += "\n"
    out += " " + "-" * (2*d-1) + " \n"
    print(out)
    
def find_prefix(pref):
    """
    Search the dictionary by dichotomy to determine if there is a word that
    begins with pref. If such a word exists, it returns it. In case pref in 
    itslef is a valid word, it returns this one and not antother word beginning
    with pref. It returns "" if no word beginning with pref exists.
    pref -- the prefix to search
    """
    a = 0
    b = len(dictionary) - 1
    while a < b:
        c = (a+b) // 2
        if pref < dictionary[c][0:len(pref)]:
            b = c-1
        elif pref > dictionary[c][0:len(pref)]:
            a = c+1
        else:
            break
    if dictionary[c][0:len(pref)] == pref:
        #at this stage, we know there is a word in the dictionary beginning by 
        #pref. let's refine the search to check if pref is in it or not.
        word = dictionary[c]
        b = c#since dictionnary[c] begins with pref, it is >pref
        while a < b:
            c = (a+b) // 2
            if pref < dictionary[c]:
                b = c-1
            elif pref > dictionary[c]:
                a = c+1
            else:
                break
        #Return pref if it's in the dictionary, the word we had found before
        #otherwise.
        if (pref == dictionary[c] or (a==b and pref == dictionary[a])):
            return pref
        else:
            return word
    elif a == b and pref == dictionary[a][0:len(pref)]:
        #In this case, there is only one word beginning with pref, so we return
        #it.
        return dictionary[a]
    else:
        return ""

def search():
    """
    Search the grid to draw the word with the best score possible.
    """
    d = int(math.sqrt(len(grid)))
    #squares will contain the list of positions from which we start.
    squares = list(range(d*d))
    #best_* will contain the best words and the relevant informations 
    #associated with it.
    best_word = ""
    best_loc = []
    best_score = 0
    while len(squares) > 0:
        #Let's pick a case randomly on the grid.
        ind_pos = random.randint(0,len(squares)-1)
        init_pos = squares.pop(ind_pos)
        to_check = [[nb] for nb in get_neighbors(init_pos,d)]
#contains the list of paths to explore. Each path is represented by a list
#of squares that will start at init_pos (not included in those lists).
        while len(to_check) > 0:
            #grab the path to check and construct the word associated to it.
            path = to_check.pop(0)
            word = grid[init_pos]
            for ngb in path:
                word += grid[ngb]
            #test if the word is the beginning of a valid word or not.
            result = find_prefix(word)
            if len(result) > 0:
                #if it is, add all the neighbors of the last position.
                new_ngb = get_neighbors(path[-1],d)
                for nn in new_ngb:
                    if nn != init_pos and nn not in path:
                        #we can decide here if we want to allow words that use 
                        #the same letter twice, just remove the test.
                        to_check.insert(0,path +[nn])
            #furthermore if word is valid, compare it to our best score to date
                if result == word:
                    scr = get_score(word)
                    if scr > best_score:
                        best_score = scr
                        best_word = word
                        best_loc = [init_pos] + path
    #Print the result.
    print_result(best_word,best_score,best_loc)
            
    
def get_neighbors(pos,d):
    """
    Returns the list of neighbors (diagonal included) of the square in position
    pos.
    pos -- the postion to check, an integer between 0 and d*d-1
    d -- the size of the grid
    """
    L = []
    #Up
    if pos >= d:
        L.append(pos-d)
        #Up left
        if pos%d > 0:
            L.append(pos-d-1)
        #Up right
        if pos%d < d-1:
            L.append(pos-d+1)
    #Bottom
    if pos < d*(d-1):
        L.append(pos+d)
        #Btoom left
        if pos%d > 0:
            L.append(pos+d-1)
        #Bottom right
        if pos%d < d-1:
            L.append(pos+d+1)
    #Left
    if pos%d > 0:
        L.append(pos-1)
    #Right
    if pos%d < d-1:
        L.append(pos+1)
    return L

def print_result(word,score,loc):
    """
    Prints the grid and the grid with only the letters of the best word found.
    word -- the word to show
    score -- the score associated
    loc -- the list of squares on the grid where the word is.
    """
    d = int(math.sqrt(len(grid)))
    space = " " * 10
    up_bot = " " + "-" * (2*d-1) + " "
    out = up_bot + space + up_bot + "\n"
    for i in range(d):
        out += "|"
        for j in range(d):
            out += grid[d*i + j] + "|"
        out += space
        out += "|"
        for j in range(d):
            if d*i+j in loc:
                out += grid[d*i + j] + "|"
            else:
                out += " |"
        out += "\n"
    out += up_bot + space + up_bot + "\n\n"
    out += f"Word {word} for {score} points."
    print(out)
