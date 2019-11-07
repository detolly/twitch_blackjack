from deck import Deck
from card import Card
from connection import Irc

class BlackjackGame:

	winstrings = {
		False: "lost",
		True: "won",
		None: "tied"
	}

	def __init__(self, username, irc : Irc):
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
		self.player = [Card(0, 1), Card(0, 11)]
		irc.sendMessage("Started blackjack game.", irc.channel)
		irc.sendMessage(self.status(), irc.channel)
		if (self.gethighestpossibleofsummedcards(self.sumcards(self.player)) == 21):
			irc.sendMessage(self.stand(True), irc.channel)

	def status(self, isblackjack=False) -> str:
		current = "@{}'s hand: ".format(self.username)
		for i in range(len(self.player)):
			current += "[{}]".format(self.player[i].get_printable()) + " "
		current += "({}) ".format(self.getformatfromsum(self.sumcards(self.player))) + "Blackjack" if isblackjack else ""
		current += ". Dealer hand: "
		for i in range(len(self.dealer)):
			current += "[{}]".format(self.dealer[i].get_printable()) + " "
		current += "({})".format(self.getformatfromsum(self.sumcards(self.dealer)))
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
			return self.end(not a)
		else:
			return self.status()

	def stand(self, isblackjack=False) -> str:
		self.dealer[0].hidden = False
		while self.gethighestpossibleofsummedcards(self.sumcards(self.dealer)) < self.gethighestpossibleofsummedcards(self.sumcards(self.player)):
			self.hit(self.dealer)
		if not(self.is_busted(self.dealer)) and self.gethighestpossibleofsummedcards(self.sumcards(self.dealer)) > self.gethighestpossibleofsummedcards(self.sumcards(self.player)):
			return self.end(False, isblackjack)
		elif self.gethighestpossibleofsummedcards(self.sumcards(self.dealer)) == self.gethighestpossibleofsummedcards(self.sumcards(self.player)):
			return self.end(None, isblackjack)
		else:
			return self.end(True, isblackjack)

	def end(self, did_player_win : bool, isblackjack=False) -> str:
		self.ended = True
		current = "@{} {}! ".format(self.username, BlackjackGame.winstrings.get(did_player_win, "tied"))
		current += self.status(isblackjack)
		return current

	#def double(self):

	def is_busted(self, cards) -> bool:
		sum = self.sumcards(cards)
		return self.gethighestpossibleofsummedcards(sum) > 21

	def getformatfromsum(self, thesum) -> str:
		if thesum[0] > 21 or thesum[1] > 21:
			return str(self.gethighestpossibleofsummedcards(thesum))
		elif thesum[0] != thesum[1]:
			return str(thesum[0]) + "/" + str(thesum[1])
		else:
			return str(thesum[0])

	def gethighestpossibleofsummedcards(self, thesum) -> int:
		if thesum[0] > thesum[1] and thesum[0] <= 21:
			return thesum[0]
		elif thesum[1] <= 21:
			return thesum[1]
		elif thesum[0] < thesum[1]:
			return thesum[0]
		else:
			return thesum[1]

	def sumcards(self, cards) -> int:
		sum = [0, 0]
		hasaced = False
		for i in range(len(cards)):
			if not cards[i].hidden:
				for k in range(2):
					if (not hasaced and k == 1 and cards[i].value == 1):
						sum[k] += 11
						hasaced = True
					else:
						sum[k] += Card.blackjackvalues.get(cards[i].value)
		return sum