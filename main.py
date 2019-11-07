from deck import Deck
from connection import Irc
import threading
from time import sleep
from blackjack import BlackjackGame

channel = "tsparkles"
games = {}


def commands(username, message, irc):
    if ("!blackjack" in message and not username in games.keys()):
        b = BlackjackGame(irc)
        games[username] = b
    if ("!hit" in message and type(games[username]) is BlackjackGame):
        irc.sendMessage(games[username].playerhit(), channel)
        if games[username].ended:
            games.pop(username)
    if ("!stand" in message and type(games[username]) is BlackjackGame):
        irc.sendMessage(games[username].stand(), channel)
        if games[username].ended:
            games.pop(username)
    if ("!double" in message and type(games[username]) is BlackjackGame):
        irc.sendMessage(games[username].stand(), channel)
        if games[username].ended:
            games.pop(username)

def main():
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, "tSparkles", "oauth:kzmnr1s2fvdwwtmqow2p3kudj44x4j")
    irc.connect()
    irc.join(channel)

    sleep(2)
    while 1:
        username, message = irc.get_message()
        if (len(username) > 1):
            commands(username, message, irc)
            print(username + ":", "\t", message)
        sleep(0.01)


main()