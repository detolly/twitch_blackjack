#!/usr/bin/python3.6

from deck import Deck
from connection import Irc
import threading
from time import sleep
from blackjack import BlackjackGame
import os

games = {}
lines = []
bot_username = ""
oauth = ""

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
    global bot_username
    if ("!join" in message and channel == bot_username):
        if (join(username, irc)):
            irc.sendMessage("Will now join " + username + "\'s channel.", channel)
    elif("!part" in message and channel == username):
        if (part(username, irc)):
            irc.sendMessage("Leaving " + username + "\'s channel.", channel)


def part(chn, irc):
    global lines
    if not chn in lines:
        irc.part(chn)
        with open("channels.txt", "r") as f:
            lines = f.readlines()
        with open("channels.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != chn:
                    f.write(line)
        return True
    return False

def join(chn, irc):
    global lines
    with open("channels.txt", "a+") as f:
        lines = f.readlines()
        if not chn in lines:
            f.write(chn + "\n")
            irc.join(chn)
        return True
    return False

def main():
    #username = os.environ["blackjack_username"]
    global bot_username, oauth
    bot_username = "theblackjackbot"
    #oauth = os.environ["blackjack_oauth"]
    with open("password.txt", "r") as f:
        oauth = f.read()
    irc : Irc = Irc("irc.chat.twitch.tv", 6667, bot_username, oauth)
    irc.connect()

    sleep(2)
    while 1:
        username, message, channel = irc.get_message()
        if (len(username) > 1):
            game(username, message, channel, irc)
            commands(username, message, channel, irc)
            print(username + ":", "\t", message)
        sleep(0.01)

main()
