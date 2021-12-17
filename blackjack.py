# =============================================================================
# N O T E S
# =============================================================================

# ON DECK:
    # Keep same deck through multiple rounds until it's empty, then create new deck.

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
    # Rearrange attributes and methods so they're in more sensible classes (a lot got dumped into GameRound) (i.e. is a method being done to a class? Then it should be within the class it's being done to.)
    # check that I'm not using more parameters than needed for my methods--prune where possible.
    # Make any mentions of a card's pips, suits, ranks, values, etc. consistent (i.e. in some areas the card's pip is referred to as its rank, which is wording I started out using but moved on from midway through)
    # Docstrings! Doc! Strings!
    # Break up GameRound __init__ into smaller functions where sensible
        # SUB-WISH: Create formatting method to gather all the dividing lines and empty lines, maybe even the pauses, etc.

# WISHLIST
    # Keep same deck through multiple rounds until it's empty, then create new deck.

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

SUITS = ["♦️ ", "♠️ ", "♣️ ", "♥️ "]
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
        """
        Creates instance of Player class with attributes name, hand, score, and
        total_wins.
        """
        self.name = name
        self.hand = []
        self.score = 0
        self.total_wins = 0

    def __str__(self):
        """
        Overrides default __str__ method of the Player class by returning its
        name attribute.
        """
        return self.name

    def recalculate_ace_values(self, game, dealer, player):
        """
        Calculates the current total value of each hand via game.hand_values,
        then for each ace in the hand, determines whether the ace's value
        should equal 1 or 11 at that given point in the game. Once determined
        and updated, the total value of each hand is recalculated
        """
        game.hand_values(dealer, player)
        for card in self.hand:
            if card.pip == "Ace":
                if (card.value == 1) and (self.score + 10 <= 21):
                    card.value = 11
                elif (card.value == 11) and (self.score > 21):
                    card.value = 1
        game.hand_values(dealer, player)

    def show_hand(self):
        """
        Prints the contents of the instance's hand.
        """
        print(f" {self.name.upper()}'S HAND: ", [f"{card}" for card in self.hand])

    def reset_hand(self):
        """
        Resets the hand to an empty list.
        """
        self.hand = []


class Dealer(Player):
    def __init__(self, name="Dealer"):
        """
        Creates instance of Dealer class, inheriting from the Player class
        which contains the attributes name, hand, score, and total_wins.
        """
        super().__init__(name)


class Deck:
    def __init__(self):
        """
        Creates instance of Deck class with a deck attribute.
        """
        self.deck = self.build(SUITS, PIPS)

    def __str__(self):
        """
        Overrides default __str__ method of the Deck class by returning its
        deck attribute.
        """
        return str(self.deck)

    def build(self, suits, pips):
        """
        Populates the deck with cards while simultaneously creating all card
        instances, then shuffles the deck.
        """
        deck = []
        for suit in suits:
            for pip in pips:
                card_value = VALUES[pip]
                card = Card(suit, pip, card_value)
                deck.append(card)
        random.shuffle(deck)
        return deck

    def deal(self, dealer, player):
        """
        Pops four cards from the deck and places 2 each in the dealer's and
        player's hands, then prints the contents of both hands, excluding the
        dealer's second card.
        """
        dealer_tuple = (self.deck.pop(), self.deck.pop())
        player_tuple = (self.deck.pop(), self.deck.pop())
        for card in dealer_tuple:
            dealer.hand.append(card)
        for card in player_tuple:
            player.hand.append(card)
        print(f" {dealer.name.upper()}'S HAND: ['{dealer.hand[0]}', --------]")
        player.show_hand()

    def hit(self, player_or_dealer):
        """
        Pops a card from the deck and adds that card to the hand of whoever has
        hit.
        """
        popped_card = self.deck.pop()
        player_or_dealer.hand.append(popped_card)


class Card:
    def __init__(self, suit, pip, value):
        """
        Creates instance of Card class with attributes suit, pip, and value.
        """
        self.suit = suit
        self.pip = pip
        self.value = value

    def __str__(self):
        """
        Overrides default __str__ method of the Card class by returning a
        string that reveals the pip and suit of the card.
        """
        return f"{self.pip} of {self.suit}"


class GameRound:
    def __init__(self, player, dealer):
        """
        Creates instance of GameRound class with the attributes deck and
        dealer_card_reveal. Also calls GameRound's play_a_round method.
        """
        self.deck = Deck()
        self.dealer_card_reveal = False

        self.play_a_round(player, dealer)

    def __str__(self):
        """
        Overrides default __str__ method of the GameRound class by returning a
        string referencing the Treachery of Images. (Read: Ariel didn't know
        what to put here.)
        """
        return "Ceci n'est pas une Game. (Ou est-ce?)"

    def play_a_round(self, player, dealer):
        """
        Calls methods to prompt the dealing of cards, recalculating of ace
        values, presenting the initial hands, the determining of winners
        (including hit loops for both player and dealer), and printing of the
        running tallies of player and dealer wins across multiple game rounds.
        """
        print()
        print(" ============================================")
        print(" ============================================")
        print()
        print(" Dealing cards...")
        print()
        time.sleep(1)

        self.deck.deal(dealer, player)
        dealer.recalculate_ace_values(self, dealer, player)
        player.recalculate_ace_values(self, dealer, player)
        self.present_scores_while_dealercard_hidden(player, dealer)

        self.determine_winner(dealer, player)

        print()
        time.sleep(0.8)
        print(f" DEALER'S WINS: {dealer.total_wins}")
        print(f" {player.name.upper()}'S WINS: {player.total_wins}")
        self.print_divider_split_sec_pause()

    def determine_winner(self, dealer, player):
        """
        Checks to see if dealer and/or player scores are at 21--win/lose/draw
        declarations are made if so, otherwise the player is entered into their
        hit loop. If the player's score hits 21 precisely at this time, they
        win. Otherwise, the dealer_hit_loop method is called, after which
        point, final win/loss/draw determinations are made. Tallies are added
        accordingly to player and dealer total_wins attributes.
        """
        if player.score == 21 and dealer.score == 21:
            self.final_score_display(player, dealer)
            print(" It's a draw!")
        elif player.score == 21:
            self.final_score_display(player, dealer)
            print(" You win!")
            player.total_wins += 1
        elif dealer.score == 21:
            self.final_score_display(player, dealer)
            print(" Dealer wins!")
            dealer.total_wins += 1
        else:
            self.prompt_hit_or_stand(player, dealer)
            if player.score == 21:
                self.final_score_display(player, dealer)
                print(" You win!")
                player.total_wins += 1
            else:
                self.dealer_hit_loop(player, dealer)
                if dealer.score == 21:
                    self.final_score_display(player, dealer)
                    print(" Dealer wins!")
                    dealer.total_wins += 1
                elif dealer.score > 21:
                    if player.score < dealer.score:
                        self.final_score_display(player, dealer)
                        print(" You win!")
                        player.total_wins += 1
                    elif player.score == dealer.score:
                        self.final_score_display(player, dealer)
                        print(" It's a draw!")
                    else:
                        self.final_score_display(player, dealer)
                        dealer.total_wins += 1
                        print(" Dealer wins!")
                else:
                    if 21 > player.score > dealer.score:
                        self.final_score_display(player, dealer)
                        print(" You win!")
                        player.total_wins += 1
                    elif player.score == dealer.score:
                        self.final_score_display(player, dealer)
                        print(" It's a draw!")
                    else:
                        self.final_score_display(player, dealer)
                        print(" Dealer wins!")
                        dealer.total_wins += 1

    def hand_values(self, dealer, player):
        """
        Calculates the total current value of dealer and player hands by
        placing all values for the player's hand into one list and all values
        for the dealer's hand into another, and then running sum() on each of
        the two lists and updating player.score and dealer.score accordingly.
        """
        player_hand_values = []
        dealer_hand_values = []
        for card in player.hand:
            player_hand_values.append(card.value)
        for card in dealer.hand:
            dealer_hand_values.append(card.value)
        player.score = sum(player_hand_values)
        dealer.score = sum(dealer_hand_values)

    def prompt_hit_or_stand(self, player, dealer):
        """
        Starts the loop as long as the dealer's score is less than 21. In the
        loop, for as long as the player's score is less than 21 and the player
        hasn't opted to stand, player is asked whether they'd like to hit. If
        invalid input is entered, inform and reprompt them. If they opt to hit,
        hit them, print current dealer and player hands and scores. Else if
        they opt to stand, reaffirm this has been done. If the player busts
        (goes over 21), reaffirm this.
        """
        player_stand = False
        if (dealer.score < 21):
            while (player.score < 21) and (player_stand is False):
                print()
                time.sleep(0.8)
                player_choice = input(" Would you like to hit? y/n: ")
                self.print_divider_split_sec_pause()
                if (player_choice.lower() != "y") and (player_choice.lower() != "n"):
                    print(" Invalid input. Please only enter 'y' or 'n'.")
                elif player_choice.lower() == "y":
                    self.deck.hit(player)
                    print(f" {dealer.name.upper()}'S HAND: ['{dealer.hand[0]}', --------]")
                    player.show_hand()
                    player.recalculate_ace_values(self, dealer, player)
                    self.present_scores_while_dealercard_hidden(player, dealer)
                else:
                    print(f" {player.name} has chosen to stand.")
                    player_stand = True
            if player.score > 21:
                print()
                time.sleep(0.8)
                print(f" {player.name} has busted.")

    def dealer_hit_loop(self, player, dealer):
        """
        As long as the dealer's score is less than 17, hit the dealer,
        recalculate ace values, and print the scores. Lather, rinse, repeat.
        """
        while dealer.score < 17:
            self.print_divider_two_sec_pause()
            print(" Dealer's turn.")
            self.deck.hit(dealer)
            dealer.recalculate_ace_values(self, dealer, player)
            self.present_scores(player, dealer)
            self.dealer_card_reveal = True

    def present_scores_while_dealercard_hidden(self, player, dealer):
        """
        For presenting scores and hands during times when it's still desirable
        to reveal only one of the dealer's cards and score. (Bonus: Additional
        formatting thrown in.)
        """
        print()
        time.sleep(0.8)

        print(f" DEALER SCORE: {dealer.hand[0].value} + ?")
        print(f" {player.name.upper()}'S SCORE: {player.score}")

    def present_scores(self, player, dealer):
        """
        For presenting scores and hands during times when you'd like to show
        the dealer's whole hand and score. (Bonus: Additional formatting thrown
        in.)
        """
        print()
        time.sleep(0.8)
        dealer.show_hand()
        player.show_hand()
        print()
        time.sleep(0.8)
        print(f" DEALER SCORE: {dealer.score}")
        print(f" {player.name.upper()}'S SCORE: {player.score}")
        print()
        time.sleep(0.8)

    def print_divider_two_sec_pause(self):
        """
        Formatting! For printing a divider when a two-second pause is desired.
        """
        time.sleep(2)
        print()
        print(" - - - - - - - - - - - - - - - - - - - - - -")
        print()

    def print_divider_split_sec_pause(self):
        """
        Formatting! For printing a divider when a 0.8-second pause is desired.
        """
        time.sleep(0.8)
        print()
        print(" - - - - - - - - - - - - - - - - - - - - - -")
        print()

    def check_dealer_card_reveal(self, player, dealer):
        """
        If the dealer's hand hasn't yet been revealed in full, this will print
        " Revealing dealer card..." and print dealer and player scores and
        hands in their entirety.
        """
        if self.dealer_card_reveal is not True:
            print(" Revealing dealer card...")
            self.present_scores(player, dealer)

    def final_score_display(self, player, dealer):
        """
        Prints a divider with a two-second pause and runs the
        check_dealer_card_reveal method.
        """
        self.print_divider_two_sec_pause()
        self.check_dealer_card_reveal(player, dealer)


class Game:
    def __init__(self):
        """
        Creates instance of Game class with attributes end_game, player, and
        dealer.
        """
        self.end_game = False
        self.player = Player()
        self.dealer = Dealer()

    def __str__(self):
        """
        Overrides default __str__ method of the Game class by returning a
        string indicating the current state of the end_game attribute.
        """
        return f"PLAYER HAS EXPRESSED DESIRE TO END THE GAME: {self.end_game}"

    def start(self):
        """
        Greets the player. For as long as the player hasn't opted to end the
        game, run the game, then check to see if the player wants to end the game.
        """
        print()
        time.sleep(0.5)
        print(f" Hello, {self.player.name}.")
        time.sleep(1)
        while not self.end_game:
            GameRound(self.player, self.dealer)
            self.check_end_condition()

    def check_end_condition(self):
        """
        Prompt the player as to whether or not they want to play another round.
        If they enter invalid input, tell them so. Otherwise if they want to
        play another round, play another round, then check condition again
        (recursive). If they don't, thank them for playing, then change the
        end_game attribute to True.
        """
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
