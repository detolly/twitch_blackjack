from deck import Deck
from connection import Irc
import threading
from time import sleep
from blackjack import BlackjackGame
import os

channelstojoin = [
    "tsparkles", "avatarinator_", "loweffortstream"
]
games = {}

def game(username, message, channel, irc):
    if (channel not in games.keys()):
        games[channel] = {}
    if ("!blackjack" in message and not username in games[channel].keys()):
        b = BlackjackGame(username, irc, channel)
        games[channel][username] = b
        if (games[channel][username]).ended:
            games[channel].pop(username)
    elif (username in games[channel].keys()):
        if ("!hit" in message and type(games[channel][username]) is BlackjackGame):
            irc.sendMessage(games[channel][username].playerhit(), channel)
            if games[channel][username].ended:
                games[channel].pop(username)
        if ("!stand" in message and type(games[channel][username]) is BlackjackGame):
            irc.sendMessage(games[channel][username].stand(), channel)
            if games[channel][username].ended:
                games[channel].pop(username)
        if ("!status" in message and type(games[channel][username]) is BlackjackGame):
            irc.sendMessage(games[channel][username].status(), channel)

def commands(username, message, channel, irc):
    if ("!join" in message and channel == os.environ["username"]):
        join(username, irc)
    elif("!part" in message and channel == username):
        part(username, irc)

def part(chn, irc):
    irc.part(chn)
    with open("channels.txt", "r") as f:
        lines = f.readlines()
    with open("channels.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != chn:
                f.write(line)

def join(chn, irc):
    irc.join(chn)
    with open("channels.txt", "a+") as f:
        f.write(chn + "\n")

def main():
    #oauth = ""
    #with open("password.txt", "r") as f:
    #    oauth = f.read()
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, os.environ["username"], os.environ["oauth"])
    irc.connect()

    for i in range(len(channelstojoin)):
        irc.join(channelstojoin[i])

    sleep(2)
    while 1:
        username, message, channel = irc.get_message()
        if (len(username) > 1):
            game(username, message, channel, irc)
            commands(username, message, channel, irc)
            print(username + ":", "\t", message)
        sleep(0.01)


main()