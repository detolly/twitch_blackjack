from deck import Deck
from connection import Irc
import threading
from time import sleep

def main():
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, "tSparkles", "oauth:kzmnr1s2fvdwwtmqow2p3kudj44x4j")
    irc.connect()
    irc.join("bagel4k")

    while 1:
        username, message = irc.get_message()
        print(username + ":", "\t\t", message)
        sleep(0.01)

main()