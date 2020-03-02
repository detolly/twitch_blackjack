import socket, string, time
from time import sleep
import re

class Irc:
    def __init__(self, ip : str, port : int, username : str, oauth : str):
        self.connection : socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.username = username
        self.oauth = oauth
        self.messages = []
        with open("channels.txt", "w+") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                print(lines[i])

    def encode(self, text):
        return text.encode("utf-8")

    def connect(self):
        self.connection.connect((self.ip, self.port))
        sleep(0.25)
        self.connection.send(self.encode("PASS " + self.oauth +    "\r\n"))
        sleep(0.25)
        self.connection.send(self.encode("NICK " + self.username.lower() + "\r\n"))
        sleep(0.15)
        self.connection.send(self.encode("JOIN #" + self.username.lower() + "\r\n"))
        with open("channels.txt", "r+") as f:
            lines = f.readlines()
            for line in lines:
                self.join(line)

    def join(self, channel):
        self.channel = channel
        self.connection.send(self.encode("JOIN #" + channel.lower() + "\r\n"))

    def part(self, channel):
        self.connection.send(self.encode("PART #" + channel.lower() + "\r\n"))

    def sendMessage(self, message, channel):
        self.connection.send(self.encode("PRIVMSG #{} :{}\r\n".format(channel, message)))

    def sendRaw(self, raw):
        self.connection.send(self.encode(raw))

    def download_from_socket(self):
        raw = self.connection.recv(61440).decode("utf-8")
        arr = raw.split("\r\n")
        for i in range(len(arr)):
            if (len(arr[i]) > 0):
                if ("PRIVMSG" in arr[i]):
                    self.messages.append(arr[i])
                elif ("PING :tmi.twitch.tv" in arr[i]):
                    self.sendRaw("PONG :tmi.twitch.tv\r\n")

    def get_message(self):
        self.download_from_socket()
        while (len(self.messages) > 0):
            response = self.messages.pop(0)
            username = re.search(r"\w+", response).group(0)
            mask = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
            message = mask.sub("", response)
            channel = response[response.index("#")+1:response.index(":", response.index("#")+1)-1]
            return username, message, channel
        return "", "", ""
