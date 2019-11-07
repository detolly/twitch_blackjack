from deck import Deck
from connection import Irc
import threading
from time import sleep
from blackjack import BlackjackGame

channel = "tsparkles"
games = {}


def commands(username, message, irc):
    if ("!blackjack" in message and not username in games.keys()):
        b = BlackjackGame()
        games[username] = b
        irc.sendMessage("Started blackjack game.", channel)
        irc.sendMessage(b.status(), channel)
    elif (username in games.keys()):
        if ("!hit" in message and type(games[username]) is BlackjackGame):
            irc.sendMessage(games[username].playerhit(), channel)
            if games[username].ended:
                games.pop(username)
        if ("!stand" in message and type(games[username]) is BlackjackGame):
            irc.sendMessage(games[username].stand(), channel)
            if games[username].ended:
                games.pop(username)

def main():
    oauth = ""
    with open("password.txt", "r") as f:
        oauth = f.read()
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, "tSparkles", oauth)
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