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
SUITES = ["diamonds", "spades", "clubs", "hearts"]
PIPS = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]


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
        self.show_dealer_hand()

    def hit(self, popped_card):
        self.hand.append(popped_card)

    def show_dealer_hand(self):
        print("DEALER'S HAND: ", [f"{card}" for card in self.hand])

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
        self.show_player_hand()

    def hit(self, popped_card):
        self.hand.append(popped_card)

    def show_player_hand(self):
        print("PLAYER'S HAND: ", [f"{card}" for card in self.hand])

    def reset_player_hand(self):
        self.hand = []


class Deck:
    def __init__(self):
        self.deck = self.build(SUITES, PIPS)

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

    def player_hit(self, player, dealer):
        popped_card = self.deck.pop()
        player.hit(popped_card)
        player.show_player_hand()
        dealer.show_dealer_hand()
        self.show_cards()

    def dealer_hit(self, player, dealer):
        popped_card = self.deck.pop()
        dealer.hit(popped_card)
        player.show_player_hand()
        dealer.show_dealer_hand()
        self.show_cards()

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
        self.winner_declared = False

        self.deck.deal(dealer, player)
        self.hand_values(dealer, player)
        self.recalculate_dealer_ace_value(dealer, player)
        self.recalculate_player_ace_value(dealer, player)
        print(f"PLAYER SCORE: {self.player_score}")
        print(f"DEALER SCORE: {self.dealer_score}")

        while self.winner_declared is False:
            if self.player_score == 21:
                print("You win!")
                self.winner_declared = True
            elif self.dealer_score == 21:
                print("Dealer wins!")
                self.winner_declared = True
            else:
                self.prompt_hit_or_stand(player, dealer)
                if self.player_score == 21:
                    print("You win!")
                    self.winner_declared = True
                else:
                    self.dealer_hit_loop(player, dealer)
                    if self.dealer_score == 21:
                        print("Dealer wins!")
                        self.winner_declared = True
                    elif self.dealer_score > 21:
                        if self.player_score < self.dealer_score:
                            print("You win!")
                            self.winner_declared = True
                        elif self.player_score == self.dealer_score:
                            print("It's a draw!")
                            self.winner_declared = True
                        else:
                            print("Dealer wins!")
                            self.winner_declared = True
                    else: # if self.dealer_score < 21
                        if 21 > self.player_score > self.dealer_score:
                            print("You win!")
                            self.winner_declared = True
                        elif self.player_score == self.dealer_score:
                            print("It's a draw!")
                            self.winner_declared = True
                        else:
                            print("Dealer wins!")
                            self.winner_declared = True
                    # Dealer now draws

    def hand_values(self, dealer, player):
    # def total_initial_hand_values(self, dealer, player):
        player_hand_values = []
        dealer_hand_values = []
        for card in player.hand:
            player_hand_values.append(card.value)
        for card in dealer.hand:
            dealer_hand_values.append(card.value)
        self.player_score = sum(player_hand_values)
        self.dealer_score = sum(dealer_hand_values)

        # OLD VERSION
        # for card in player.hand:
        #     self.player_score += card.value
        # for card in dealer.hand:
        #     self.dealer_score += card.value
        # print(f"DEALER SCORE: {self.dealer_score}")
        # print(f"PLAYER SCORE: {self.player_score}")

    # def total_subsequent_player_hand_values(self, player):
    #     self.player_score += player.hand[-1].value
    #     print(f"DEALER SCORE: {self.dealer_score}")
    #     print(f"PLAYER SCORE: {self.player_score}")

    # def total_subsequent_dealer_hand_values(self, dealer):
    #     self.dealer_score += dealer.hand[-1].value
    #     print(f"DEALER SCORE: {self.dealer_score}")
    #     print(f"PLAYER SCORE: {self.player_score}")

    def recalculate_player_ace_value(self, dealer, player):
        for card in player.hand:
            if card.rank == "Ace":
                if (card.value == 1) and (self.player_score + 10 <= 21):
                    card.value = 11 
                    self.hand_values(dealer, player)
                    print("Value *SHOULD* now be 11")
                elif (card.value == 11) and (self.player_score > 21):
                    card.value = 1
                    self.hand_values(dealer, player)
                    print("Value *SHOULD* now be 1")
                else:
                    print("Value *SHOULD* be whatever it already was")

    def recalculate_dealer_ace_value(self, dealer, player):
        for card in dealer.hand:
            if card.rank == "Ace":
                if (card.rank == 1) and (self.dealer_score + 10 <= 21):
                    card.rank = 11 
                    hand_values(dealer, player)
                elif (card.rank == 11) and (self.dealer_score > 21):
                    card.rank = 1
                    hand_values(dealer, player)

    def prompt_hit_or_stand(self, player, dealer):
        player_stand = False
        if (self.player_score < 21) and (self.dealer_score < 21) and (player_stand is False):
            while (self.player_score < 21) and (player_stand is False):
                player_choice = input("Hit or stand? ")
                if (player_choice.lower() != "hit") and (player_choice.lower() != "stand"):
                    print("Invalid input. Please only enter 'hit' or 'stand'.")
                elif player_choice.lower() == "hit":
                    self.deck.player_hit(player, dealer)
                    self.hand_values(dealer, player)
                    self.recalculate_player_ace_value(dealer, player)
                else:
                    print("Player has chosen to stand.")
                    player_stand = True

    def dealer_hit_loop(self, player, dealer):
        while self.dealer_score < 17:
            self.deck.dealer_hit(player, dealer)
            self.hand_values(dealer, player)
            self.recalculate_dealer_ace_value(dealer, player)


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
