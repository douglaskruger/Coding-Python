import random

# Card setup
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8,
          "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []  # Empty list to store the cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def __str__(self):
        deck_str = "Deck contains:\n"
        for card in self.cards:
            deck_str += '\t' + card.__str__() + '\n'
        return deck_str

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Track aces for flexible valuation

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If the total value exceeds 21 and there's an ace, reduce its value from 11 to 1
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry, please provide an integer.")
        else:
            if chips.bet > chips.total:
                print("Not enough chips! You have:", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal_card())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # To control the game loop

    while True:
        choice = input("Hit or Stand? Enter 'h' or 's': ").lower()
        if choice[0] == 'h':
            hit(deck, hand)
        elif choice[0] == 's':
            print("Player stands, Dealer's turn.")
            playing = False
        else:
            print("Invalid input, please try again.")
            continue
        break

# Game Functions
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <Hidden Card>")
    print(dealer.cards[1])

    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand Value =", player.value)


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand Value =", dealer.value)

    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand Value =", player.value)


def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()


def push():
    print("It's a tie!")


# Main Game Loop
while True:
    print("Welcome to Blackjack!")

    # Create & shuffle the deck, deal two cards each
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Setup player's chips
    player_chips = Chips()

    # Prompt for the bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    playing = True  # Game in progress

    while playing:
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 or busts
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        # Check win scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    # Inform Player of their chips total
    print(f"\nPlayer's total chips: {player_chips.total}")

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n': ")
    if new_game[0].lower() == 'y':
        continue
    else:
        print("Thanks for playing!")
        break