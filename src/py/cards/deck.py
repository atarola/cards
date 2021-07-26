import itertools
import random

#
# Represents a deck of cards
#

class Deck(object):

    def __init__(self):
        self.cards = [Card(*pair) for pair in itertools.product(FACES, SUITS)]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

#
# Represents a single card
#

class Card(object):

    def __init__(self, face, suit):
        self.face = face
        self.suit = suit

    def to_value(self):
        if self.face is None:
            return 0

        return FACES.index(self.face) + 2

    def to_dict(self):
        return {"face": self.face, "suit": self.suit}

    def __repr__(self):
        return f"Card({self.face}, {self.suit})"


FACES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
SUITS = ["clubs", "diamonds", "hearts", "spades"]
