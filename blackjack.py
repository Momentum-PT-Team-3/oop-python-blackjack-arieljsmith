# =============================================================================
# I M P O R T S
# =============================================================================

import random


# =============================================================================
# C O N S T A N T S
# =============================================================================

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
        # self.show_cards()

    def player_hit(self, player, dealer):
        popped_card = self.deck.pop()
        player.hit(popped_card)
        player.show_player_hand()
        dealer.show_dealer_hand()
        # self.show_cards()

    def dealer_hit(self, player, dealer):
        popped_card = self.deck.pop()
        dealer.hit(popped_card)
        player.show_player_hand()
        dealer.show_dealer_hand()
        # self.show_cards()

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
                    else:
                        if 21 > self.player_score > self.dealer_score:
                            print("You win!")
                            self.winner_declared = True
                        elif self.player_score == self.dealer_score:
                            print("It's a draw!")
                            self.winner_declared = True
                        else:
                            print("Dealer wins!")
                            self.winner_declared = True

    def hand_values(self, dealer, player):
        player_hand_values = []
        dealer_hand_values = []
        for card in player.hand:
            player_hand_values.append(card.value)
        for card in dealer.hand:
            dealer_hand_values.append(card.value)
        self.player_score = sum(player_hand_values)
        self.dealer_score = sum(dealer_hand_values)

    def recalculate_player_ace_value(self, dealer, player):
        for card in player.hand:
            if card.rank == "Ace":
                if (card.value == 1) and (self.player_score + 10 <= 21):
                    card.value = 11 
                    self.hand_values(dealer, player)
                elif (card.value == 11) and (self.player_score > 21):
                    card.value = 1
                    self.hand_values(dealer, player)

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

game = Game()
game.start()
