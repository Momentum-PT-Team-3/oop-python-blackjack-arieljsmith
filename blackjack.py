# This assignment is based on the card game blackjack (also called 21). If you are unfamiliar with the game, instructions can be found [here](https://bicyclecards.com/how-to-play/blackjack/).

# The main objective is to have a hand of cards whose sum is as close to 21 as possible without going over. 
# This game will have two players, one dealer (computer) and one human.

# ## Reqirements
# - Build a blackjack game using python between a player and a dealer.  


# The dealer's play is dictated by the rules of the game, and the dealer goes first. The dealer "hits" (is dealt a card) until their hand total is 17 or greater, at which point they stay. The dealers cards are all visible to the player.
# The player then chooses whether to be hit or stay. The player may hit as many times as they want before staying, but if their hand totals over 21, they "bust" and lose. 
# If you want to make the game work for multiple players, go for it.
# The deck is a standard 52 card deck with 4 suits. Face cards are worth 10. The Ace card can be worth 1 or 11.  
# Use classes. One way to think about classes is that they are the _nouns_ involved in what you are modeling, so Card, Deck, Player, Dealer, and Game are all nouns that could be classes.
# Give those classes methods. Think about the _actions_ that happen to or are caused by these different elements. These choices are subjective and hard, and there is no one right way.
# Use your classes and methods to execute the gameplay. It is always a great idea to sketch and/or comment this out first before writing code.

    # 0) Make A only be 1 for this first game version. TODO: handle 1 or 11 option later.
    # 1) A) Create a player and
    #    B) dealer class. Each need a hand attribute.
    # 2) Create a card class: suit, rank
    # 3) Create a deck class with cards. 52 total, 2-10, J Q K A, in each suit ◆ ♠ ♣ ♥
    # 4) Shuffle and deal method for cards
    # 5) Dealer play. Methods: hit, stay
    # 6) Player play. Methods: hit, stay
    # 7) Determine who wins, loses. Need method for calculating value of hand

# =============================================================================
# I M P O R T S
# =============================================================================

import random


# =============================================================================
# C L A S S E S
# =============================================================================

class Dealer:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return "Dealer"


class Player:
    def __init__(self):
        self.name = input("What is your name? ")
        self.hand = []

    def __str__(self):
        return self.name


class Deck:
    def __init__(self):
        pass


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class GameRound:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.end_game = False
        self.player = Player()
        self.dealer = Dealer()

    def start(self):
        while not self.end_game:
            # Start a gameround on this line
            self.check_end_condition()

    def check_end_condition(self):
        answer = input("Would you like to play another round? y/n: ")
        if answer == "y":
            # Start another gameround on this line
            self.check_end_condition()
        else:
            print("Thank you for playing!")
            self.end_game = True


# =============================================================================
# W H E R E  S H I R T  H A P P E N S
# =============================================================================

# Game Play/testing shirt works (Mostly the letter)
player = Player()
dealer = Dealer()
print(player, dealer)

suits = ["◆", "♠", "♣", "♥"]
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

deck = []
for suit in suits:
    for rank in ranks:
        card = Card(suit, rank)
        deck.append(card)

# game = Game()

# =============================================================================
# M I S C E L L A N Y
# =============================================================================
