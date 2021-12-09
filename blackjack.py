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

    def deal(self, popped_cards):
        for card in popped_cards:
            self.hand.append(card)
        print("DEALER'S HAND: ", [f"{card}" for card in self.hand])

    def hit(self):
        pass

    def reset_dealer_hand(self):
        self.hand = []


class Player:
    def __init__(self):
        self.name = input("What is your name? ")
        self.hand = []

    def __str__(self):
        return self.name

    def deal(self, popped_cards):
        for card in popped_cards:
            self.hand.append(card)
        print("YOUR HAND: ", [f"{card}" for card in self.hand])

    def hit(self):
        pass

    def reset_player_hand(self):
        self.hand = []


class Deck:
    def __init__(self):
        self.deck = self.build(["diamonds", "spades", "clubs", "hearts"], [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"])

    def __str__(self):
        return str(self.deck)

    def build(self, suits, ranks):
        deck = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                deck.append(card)
        random.shuffle(deck)
        return deck

    def deal(self, dealer, player):
        dealer_tuple = (self.deck.pop(), self.deck.pop())
        player_tuple = (self.deck.pop(), self.deck.pop())
        dealer.deal(dealer_tuple)
        player.deal(player_tuple)
        self.show_cards()

    def hit(self):
        pass

    def show_cards(self):
        print("The cards in this deck include: ", [f"{card}" for card in self.deck])


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.calculate_value(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def calculate_value(self, rank):
        value_dictionary = {
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            "Jack": 10,
            "Queen": 10,
            "King": 10,
            "Ace": 1
        }
        card_value = value_dictionary[rank]
        # print(f"The value of {rank} is {card_value}") # FOR TESTING ONLY
        return card_value


class GameRound:
    def __init__(self, player, dealer):
        self.deck = Deck()
        self.dealer_score = 0
        self.player_score = 0
        # Deal first two cards to dealer hand, second two cards to player hand
            # This involves removing each card from the deck before placing it in the respective hand
        # Print contents of dealer hand
        # Print contents of player hand
        self.deck.deal(dealer, player)
        self.total_hand_values(dealer, player, self.dealer_score, self.player_score)
        self.prompt_hit_or_stand()
        # function to check if player's hand is at 21. If it is, they win!
        # if it ISN'T, then we go into dealer actions.

    def total_hand_values(self, dealer, player, dealer_score, player_score):
        for card in player.hand:
            player_score += card.value
        for card in dealer.hand:
            dealer_score += card.value
        print(f"DEALER SCORE: {dealer_score}")
        print(f"PLAYER SCORE: {player_score}")

    def prompt_hit_or_stand(self):
        # While summed value of player's hand is less than 21...
            player_choice = input("Hit or stand? ")
            if (player_choice.lower() != "hit") and (player_choice.lower() != "stand"):
                print("Invalid input. Please only enter 'hit' or 'stand'.")
            elif player_choice.lower() == "hit":
                pass
            else:
                pass


class Game:
    def __init__(self):
        self.end_game = False
        self.player = Player()
        self.dealer = Dealer()

    def start(self):
        while not self.end_game:
            GameRound(self.player, self.dealer)
            self.check_end_condition()

    def check_end_condition(self):
        answer = input("Would you like to play another round? y/n: ")
        if answer == "y":
            self.player.reset_player_hand()
            self.dealer.reset_dealer_hand()
            GameRound(self.player, self.dealer)
            self.check_end_condition()
        else:
            print("Thank you for playing!")
            self.end_game = True


# =============================================================================
# W H E R E  S H I R T  H A P P E N S
# =============================================================================

# Game Play/testing shirt works (Mostly the latter)
# player = Player()
# dealer = Dealer()
# print(f"{player} is playing against the {dealer}.")
# print ()
# deck = Deck()
# deck.show_cards()

# suits = ["diamonds", "spades", "clubs", "hearts"]
# ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

# deck = []
# for suit in suits:
#     for rank in ranks:
#         card = Card(suit, rank)
#         deck.append(card)

game = Game()
game.start()

# =============================================================================
# M I S C E L L A N Y
# =============================================================================
