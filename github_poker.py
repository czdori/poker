import random 
import math
import itertools
from collections import defaultdict

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key = hand_rank)

def allmax(iterable, key=lambda x:x):
    "Return a list of all items equal to the max of the iterable."
    maxi = max(iterable, key=key)
    return [element for element in iterable if key(element) == key(maxi)]

# if we play with jokers, it goes like this...

def best_wild_hand(hand):       
    "Try all values for jokers in all 5-card selections."
    all_hands = [hand.replace('?B', blackcard).replace('?R',redcard) for blackcard in replacement('?B') for redcard in replacement('?R')]
    return max(itertools.combinations(all_hands, 5), key=hand_rank)
    
def replacement(joker):
    "Replace the joker cards indicated with ?B and ?R with the appropriate values."
    mydict = {'?B': 'SC', '?R': 'HD'}
    all = itertools.product('2345678910JQKA', mydict[joker])
    return [('').join(e) for e in all]
    

def hand_rank(hand):
    "Return a value indicating how high the hand ranks."
    # counts is the count of each rank
    # ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return (
        9 if (5, ) == counts else
        8 if straight and flush else
        7 if (4, 1) == counts else
        6 if (3, 2) == counts else
        5 if flush else
        4 if straight else
        3 if (3, 1, 1) == counts else
        2 if (2, 2, 1) == counts else
        1 if (2, 1, 1, 1) == counts else
        0), ranks

def group(items):
    "Return a list of [(count, x)...], highest count first, the highest x first"
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse = True)

def unzip(pairs):
    return zip(*pairs)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    # ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    # ranks = [{'A':14,
    #           'K':13,
    #           'Q':12,
    #           'J':11,
    #           'T':10,
    #           }.get(r,r) for r, s in hand]
    ranks = [14 if r == 'A' else
             13 if r == 'K' else
             12 if r == 'Q' else
             11 if r == 'J' else
             10 if r == 'T' else
             int(r)
             for r, s in hand]
    ranks.sort(reverse = True)
    return ranks if ranks != [14, 5, 4, 3, 2] else [5, 4, 3, 2, 1]

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return sum(ranks) - min(ranks)*5 == 10

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    result = [r for r in set(ranks) if ranks.count(r) == 2]
    if len(result) == 2:
        return (max(result), min(result))

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in set(ranks):
        if ranks.count(r) == n:
            return r
    return None

deck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n = 5, deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Return a list of numhands hands consisting of n cards each"
    random.shuffle(deck)
    deck = iter(deck)
    return [[next(deck) for card in range(n)] for hand in range(numhands)]  