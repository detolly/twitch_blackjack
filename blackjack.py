from deck import Deck
from card import Card
from connection import Irc

class BlackjackGame:

	def __init__(self, username):
		self.dealer = []
		self.ended = False
		self.player = []
		self.username = username
		self.deck = Deck()
		self.deck.shuffle()
		self.dealer.append(self.deck.get_card())
		self.dealer[0].hidden = True
		self.player.append(self.deck.get_card())
		self.dealer.append(self.deck.get_card())
		self.player.append(self.deck.get_card())

	def status(self) -> str:
		current = "@{}'s hand: ".format(self.username)
		for i in range(len(self.player)):
			current += "[{}]".format(self.player[i].get_printable()) + " "
		current += "({}) ".format(self.sumcards(self.player))
		current += ". Dealer hand: "
		for i in range(len(self.dealer)):
			current += "[{}]".format(self.dealer[i].get_printable()) + " "
		current += "({})".format(self.sumcards(self.dealer))
		current += "."
		return current

	def hit(self, cards) -> bool:
		cards.append(self.deck.get_card())
		if self.is_busted(cards):
			return True
		else:
			return False

	def playerhit(self) -> str:
		a = self.hit(self.player)
		if (a):
			return self.end(a)
		else:
			return self.status()

	def stand(self) -> str:
		self.dealer[0].hidden = False
		while self.sumcards(self.dealer) < self.sumcards(self.player):
			self.hit(self.dealer)
		if not(self.is_busted(self.dealer)) and self.sumcards(self.dealer) > self.sumcards(self.player):
			return self.end(False)
		else:
			return self.end(True)

	def end(self, did_player_win : bool) -> str:
		self.ended = True
		current = "@{} {}! ".format(self.username, "won" if did_player_win else "lost")
		current += self.status()
		return current

	#def double(self):

	def is_busted(self, cards) -> bool:
		sum = self.sumcards(cards)
		return sum > 21

	def sumcards(self, cards) -> int:
		sum = 0
		for i in range(len(cards)):
			if not cards[i].hidden:
				sum += Card.blackjackvalues.get(cards[i].value)
		return sum