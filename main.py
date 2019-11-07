from deck import Deck
from connection import Irc
import threading
from time import sleep
from blackjack import BlackjackGame

channel = "tsparkles"
games = {}


def commands(username, message, irc):
    if ("!blackjack" in message):
        b = BlackjackGame(irc)
        games[username] = b
    if ("!hit" in message and games[username] is BlackjackGame):
        irc.sendMessage(games[username].hit())
    if ("!stand" in message and type(games[username]) is BlackjackGame):
        irc.sendMessage(games[username].stand())


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