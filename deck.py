from card import *
from random import shuffle

class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for value in range(1, 13+1):
                if not (value >= 2 and value <= 6):
                    self.cards.append(Card(suit, value))
        self.ocards = self.cards.copy()
    
    def shuffle(self):
        shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()