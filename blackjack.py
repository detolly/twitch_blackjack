from deck import Deck
from card import Card
from connection import Irc

class BlackjackGame:

	def __init__(self, irc : Irc):
		self.dealer = []
		self.irc = irc
		self.ended = False
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
		current = "Player hand: "
		for i in range(len(self.player)):
			current += self.player[i].get_printable() + " "
		current += "({}) ".format(self.sumcards(self.player))
		current += ". Dealer hand: "
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

	def playerhit(self) -> str:
		return self.hit(self.player)

	def stand(self) -> str:
		self.dealer[0].hidden = False
		while self.sumcards(self.dealer) < 17:
			self.hit(self.dealer)
		if not(self.is_busted(self.dealer)) and self.sumcards(self.dealer) > self.sumcards(self.player):
			return self.end(False)
		else:
			return self.end(True)

	def end(self, did_player_win : bool) -> str:
		self.ended = True
		current = "Player won! " if did_player_win else "Player lost. "
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