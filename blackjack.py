from deck import Deck
from card import Card
from connection import Irc

class BlackjackGame:

	def __init__(self, irc : Irc):
		self.dealer = []
		self.irc = irc
		self.player = []
		self.deck = Deck()
		self.deck.shuffle()
		irc.sendMessage("Started blackjack game.", irc.channel)
		self.dealer.append(self.deck.get_card())
		self.dealer[0].hidden = True
		self.player.append(self.deck.get_card())
		self.dealer.append(self.deck.get_card())
		self.player.append(self.deck.get_card())
		irc.sendMessage(self.status(), irc.channel)

	def status(self) -> str:
		current = "Current player hand: "
		for i in range(len(self.player)):
			current += self.player[i].get_printable() + " "
		current += "({}) ".format(self.sumcards(self.player))
		current += " and the dealer has "
		for i in range(len(self.dealer)):
			current += self.dealer[i].get_printable() + " "
		current += "({})".format(self.sumcards(self.dealer))
		current += "."
		return current

	def hit(self, cards) -> str:
		cards.append(self.deck.get_card())
		if self.is_busted(cards):
			return "busted"
		else:
			return self.status()

	def stand(self) -> str:
		while self.sumcards(self.dealer) < 17:
			self.hit(self.dealer)
		if not(self.is_busted(self.dealer)) and sum(self.dealer) > sum(self.player):
			print("player lost")
		else:
			print("player won")

	#def double(self):

	def is_busted(self, cards) -> bool:
		sum = self.sumcards(cards)
		return sum > 21

	def sumcards(self, cards) -> int:
		sum = 0
		for i in range(len(cards)):
			sum += Card.blackjackvalues.get(cards[i].value)
		return sum