# =============================================================================
# N O T E S
# =============================================================================

# ON DECK:
    # Break up GameRound __init__ into smaller functions where sensible
        # SUB-WISH: Create formatting method to gather all the dividing lines and empty lines, maybe even the pauses, etc.

# COMPLETE (OF WISHLIST ITEMS):
    # Formatting everything to look a bit better during gameplay
    # make dealer or player a subclass of the other
    # running tally of number of player wins and dealer wins
    # hide dealer second card until it starts to hit
    # FIXED: ERROR: If dealer starts with an ace and a jack, for example, code won't recognize that it's at 21 before the dealer hits. Therefore, when the dealer *could* have won, they don't currently.
    # Remove unnecessary winner_declared attribute from GameRound
    # IMPROVEMENT: If player stands and dealer wins without making a move, we currently don't see the dealer's hand or score. This would be nice to know.
    # Make value_dictionary a global constant
    # Remove recalculate_player_ace_value and recalculate_dealer_ace_value methods from GameRound and consolidate into a single method in Player class
    # Bundle functionality of the calculate_value method in the Card class instead with the build method in the Deck class
    # SOLVEDBUG: After player busted (24), the dealer hit, resulting in a 20. After this it went immediately into "Revealing dealer card..."--this should not be necessary as the dealer's cards were already revealed. Either I need to reword this, or need to rethink the logic surrounding it.

# WISHLIST
    # Rearrange attributes and methods so they're in more sensible classes (a lot got dumped into GameRound) (i.e. is a method being done to a class? Then it should be within the class it's being done to.)
    # check that I'm not using more parameters than needed for my methods--prune where possible.
    # Docstrings! Doc! Strings!
    # Keep same deck through multiple rounds until it's empty, then create new deck.
    # Make any mentions of a card's pips, suits, ranks, values, etc. consistent (i.e. in some areas the card's pip is referred to as its rank, which is wording I started out using but moved on from midway through)

# LONG-TERM:
    # Splitting! oooooo


# =============================================================================
# I M P O R T S
# =============================================================================

import random
import time


# =============================================================================
# C O N S T A N T S ,  E T C .
# =============================================================================

SUITES = ["♦️ ", "♠️ ", "♣️ ", "♥️ "]
PIPS = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
VALUES = {
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

print()
time.sleep(0.8)


# =============================================================================
# C L A S S E S
# =============================================================================

class Player:
    def __init__(self, name=input(" What is your name? ")):
        self.name = name
        self.hand = []
        self.score = 0
        self.total_wins = 0

    def __str__(self):
        return self.name

    def recalculate_ace_values(self):
        for card in self.hand:
            if card.rank == "Ace":
                if (card.value == 1) and (self.score + 10 <= 21):
                    card.value = 11
                elif (card.value == 11) and (self.score > 21):
                    card.value = 1

    def show_hand(self):
        print(f" {self.name.upper()}'S HAND: ", [f"{card}" for card in self.hand])

    def reset_hand(self):
        self.hand = []


class Dealer(Player):
    def __init__(self, name="Dealer"):
        super().__init__(name)


class Deck:
    def __init__(self):
        self.deck = self.build(SUITES, PIPS)

    def __str__(self):
        return str(self.deck)

    def build(self, suits, ranks):
        deck = []
        for suit in suits:
            for rank in ranks:
                card_value = VALUES[rank]
                card = Card(suit, rank, card_value)
                deck.append(card)
        random.shuffle(deck)
        return deck

    def deal(self, dealer, player):
        dealer_tuple = (self.deck.pop(), self.deck.pop())
        player_tuple = (self.deck.pop(), self.deck.pop())
        for card in dealer_tuple:
            dealer.hand.append(card)
        for card in player_tuple:
            player.hand.append(card)
        print(f" {dealer.name.upper()}'S HAND: ['{dealer.hand[0]}', --------]")
        player.show_hand()

    def player_hit(self, player):
        popped_card = self.deck.pop()
        player.hand.append(popped_card)

    def dealer_hit(self, dealer):
        popped_card = self.deck.pop()
        dealer.hand.append(popped_card)


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class GameRound:
    def __init__(self, player, dealer):
        self.deck = Deck()
        self.dealer_card_reveal = False

        self.play_a_round(player, dealer)

    def __str__(self):
        return "Ceci n'est pas une Game. (Ou est-ce?)"

    def play_a_round(self, player, dealer):
        print()
        print(" ============================================")
        print(" ============================================")
        print()
        print(" Dealing cards...")
        print()
        time.sleep(1)

        self.deck.deal(dealer, player)
        self.hand_values(dealer, player)
        dealer.recalculate_ace_values()
        player.recalculate_ace_values()
        self.hand_values(dealer, player)
        self.present_scores_while_dealercard_hidden(player, dealer)

        self.determine_winner(dealer, player)

        print()
        time.sleep(0.8)
        print(f" DEALER'S WINS: {dealer.total_wins}")
        print(f" {player.name.upper()}'S WINS: {player.total_wins}")
        self.print_divider_split_sec_pause()

    def determine_winner(self, dealer, player):
        if player.score == 21 and dealer.score == 21:
            self.print_divider_two_sec_pause()
            self.check_dealer_card_reveal(player, dealer)
            # self.present_scores(player, dealer)
            print()
            time.sleep(0.8)
            print(" It's a draw!")
        elif player.score == 21:
            self.print_divider_two_sec_pause()
            self.check_dealer_card_reveal(player, dealer)
            # self.present_scores(player, dealer)
            print()
            time.sleep(0.8)
            print(" You win!")
            player.total_wins += 1
        elif dealer.score == 21:
            self.print_divider_two_sec_pause()
            self.check_dealer_card_reveal(player, dealer)
            # self.present_scores(player, dealer)
            print()
            time.sleep(0.8)
            print(" Dealer wins!")
            dealer.total_wins += 1
        else:
            self.prompt_hit_or_stand(player, dealer)
            if player.score == 21:
                self.print_divider_two_sec_pause()
                self.check_dealer_card_reveal(player, dealer)
                # self.present_scores(player, dealer)
                print()
                time.sleep(0.8)
                print(" You win!")
                player.total_wins += 1
            else:
                self.dealer_hit_loop(player, dealer)
                if dealer.score == 21:
                    self.print_divider_two_sec_pause()
                    self.check_dealer_card_reveal(player, dealer)
                    # self.present_scores(player, dealer)
                    print(" Dealer wins!")
                    dealer.total_wins += 1
                elif dealer.score > 21:
                    if player.score < dealer.score:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        print(" You win!")
                        player.total_wins += 1
                    elif player.score == dealer.score:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        print(" It's a draw!")
                    else:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        dealer.total_wins += 1
                else:
                    if 21 > player.score > dealer.score:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        print(" You win!")
                        player.total_wins += 1
                    elif player.score == dealer.score:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        print(" It's a draw!")
                    else:
                        self.print_divider_two_sec_pause()
                        self.check_dealer_card_reveal(player, dealer)
                        # self.present_scores(player, dealer)
                        print()
                        print(" Dealer wins!")
                        dealer.total_wins += 1

    def hand_values(self, dealer, player):
        player_hand_values = []
        dealer_hand_values = []
        for card in player.hand:
            player_hand_values.append(card.value)
        for card in dealer.hand:
            dealer_hand_values.append(card.value)
        player.score = sum(player_hand_values)
        dealer.score = sum(dealer_hand_values)

    def prompt_hit_or_stand(self, player, dealer):
        player_stand = False
        if (player.score < 21) and (dealer.score < 21) and (player_stand is False):
            while (player.score < 21) and (player_stand is False):
                print()
                time.sleep(0.8)
                player_choice = input(" Hit or stand? ")
                self.print_divider_split_sec_pause()
                if (player_choice.lower() != "hit") and (player_choice.lower() != "stand"):
                    print(" Invalid input. Please only enter 'hit' or 'stand'.")
                elif player_choice.lower() == "hit":
                    self.deck.player_hit(player)
                    print(f" {dealer.name.upper()}'S HAND: ['{dealer.hand[0]}', --------]")
                    player.show_hand()
                    self.hand_values(dealer, player)
                    player.recalculate_ace_values()
                    self.hand_values(dealer, player)
                    self.present_scores_while_dealercard_hidden(player, dealer)
                else:
                    print(f" {player.name} has chosen to stand.")
                    player_stand = True
            if player.score > 21:
                print()
                time.sleep(0.8)
                print(f" {player.name} has busted.")

    def dealer_hit_loop(self, player, dealer):
        while dealer.score < 17:
            self.print_divider_two_sec_pause()
            print(" Dealer's turn.")
            self.deck.dealer_hit(dealer)
            self.hand_values(dealer, player)
            dealer.recalculate_ace_values()
            self.hand_values(dealer, player)
            self.present_scores(player, dealer)
            self.dealer_card_reveal = True

    def present_scores_while_dealercard_hidden(self, player, dealer):
        print()
        time.sleep(0.8)

        print(f" DEALER SCORE: {dealer.hand[0].value} + ?")
        print(f" {player.name.upper()}'S SCORE: {player.score}")

    def present_scores(self, player, dealer):
        print()
        time.sleep(0.8)
        dealer.show_hand()
        player.show_hand()
        print()
        time.sleep(0.8)
        print(f" DEALER SCORE: {dealer.score}")
        print(f" {player.name.upper()}'S SCORE: {player.score}")

    def print_divider_two_sec_pause(self):
        time.sleep(2)
        print()
        print(" - - - - - - - - - - - - - - - - - - - - - -")
        print()

    def print_divider_split_sec_pause(self):
        time.sleep(0.8)
        print()
        print(" - - - - - - - - - - - - - - - - - - - - - -")
        print()

    def check_dealer_card_reveal(self, player, dealer):
        if self.dealer_card_reveal is not True:
            print(" Revealing dealer card...")
            self.present_scores(player, dealer)


class Game:
    def __init__(self):
        self.end_game = False
        self.player = Player()
        self.dealer = Dealer()

    def __str__(self):
        return f"THE PLAYER'S NAME IS {self.player.name}."

    def start(self):
        print()
        time.sleep(0.5)
        print(f" Hello, {self.player.name}.")
        time.sleep(1)
        while not self.end_game:
            GameRound(self.player, self.dealer)
            self.check_end_condition()

    def check_end_condition(self):
        time.sleep(0.8)
        valid_answer = False
        while valid_answer is False:
            answer = input(" Would you like to play another round? y/n: ")
            if answer.lower() == "y" or answer.lower() == "n":
                valid_answer = True
            else:
                time.sleep(0.8)
                print()
                print(" Invalid input. Please only enter 'y' or 'n'.")
                print()
                time.sleep(0.8)
        if answer == "y":
            time.sleep(0.8)
            self.player.reset_hand()
            self.dealer.reset_hand()
            GameRound(self.player, self.dealer)
            self.check_end_condition()
        else:
            time.sleep(0.8)
            print()
            print(" Thank you for playing!")
            time.sleep(0.8)
            self.end_game = True


# =============================================================================
# W H E R E  S H I R T  H A P P E N S
# =============================================================================

game = Game()
game.start()
