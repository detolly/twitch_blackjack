from deck import Deck
from connection import Irc
import threading
from time import sleep

channel = "tsparkles"


def commands(username, message, irc):
    if ("!givemeacard" in message):
        d = Deck()
        d.shuffle()
        c = d.get_card()
        irc.sendMessage(c.get_printable(), channel)


def main():
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, "tSparkles", "oauth:kzmnr1s2fvdwwtmqow2p3kudj44x4j")
    irc.connect()
    irc.join(channel)

    while 1:
        username, message = irc.get_message()
        if (len(username) > 1):
            commands(username, message, irc)
            print(username + ":", "\t", message)
        sleep(0.01)


main()