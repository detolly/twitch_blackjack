from card import *
from random import shuffle

class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for value in range(1, 13+1):
                self.cards.append(Card(suit, value))
    
    def shuffle(self, r=10):
        for i in range(r):
            shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()