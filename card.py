class Card:
    suits = {
        0: "\u2660",
        1: "\u2666",
        2: "\u2663",
        3: "\u2665", 
    }
    values = {
        1: "A", 2: "2", 3: "3", 4: "4",
        5: "5", 6: "6", 7: "7", 8: "8",
        9: "9", 10: "10", 11: "J", 12: "Q",
        13: "K"
    }
    blackjackvalues = {
        1: 1, 2: 2, 3: 3, 4: 4,
        5: 5, 6: 6, 7: 7, 8: 8,
        9: 9, 10: 10, 11: 10, 12: 10,
        13: 10
    }

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.hidden = False
    
    def get_printable(self) -> str:
        return Card.suits.get(self.suit, "") + Card.values.get(self.value, "") if not self.hidden else "??"

    def equals(self, card) -> bool:
        return self.value == card.value
