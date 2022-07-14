#!/usr/bin/env python

""" The server program for chatroom application using socket programming."""

import socket
import time
from threading import Thread

# listen on all IPv4 interfaces 
HOST = "0.0.0.0"
# port to listen on (non-privileged ports are > 1023)
PORT = 6000 

# parameters passed to socket() are constants. AF_INET is the internet family address for IPv4
# and SOCK_STREAM is the socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # make the port reusable
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    connection, address = s.accept()

    with connection:
        print("Connected by {}".format(address))
        while True:
            # read at most 1024 bytes blockingly
            data = connection.recv(1024)
            if not data:
                break
            # unlike send(), sendall() will continue to send data 
            # from bytes until either all data has been sent 
            # or an error occured
            connection.sendall(data)

class Server():
    
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.STREAM)
        self.server_address = ("0.0.0.0", 6000)
        self.bind(self.server_address)
        self.socket.listen()

        self.format = "utf-8"
        # length of message used for sending message length
        self.header_length = 10
        # maximum length of messages
        self.max_length = 1024
        self.commands = {disconnect: "/disconnect", people: "/people", private: "/private"}
        # {connection: {"username": username, "address": address, "join_time": join_time}}
        self.clients = {}
        # {"username": {"sent": [(time, "message")], "received": [(time, "message")]}}
        self.messages = {}
        self.colors = {
            purple = '\033[95m'
            cyan = '\033[96m'
            darkcyan = '\033[36m'
            blue = '\033[94m'
            green = '\033[92m'
            yellow = '\033[93m'
            red = '\033[91m'
            bold = '\033[1m'
            underline = '\033[4m'
            end = '\033[0m'
                }
       
        timestamp = self.timestamp()
        print("{} Server started on {}:{}".format(timestamp, *self.server_address))
        self.start_accepting()

    def timestamp(self, formatted=True):
        now = time.strftime("%Y-%m-%d %H:%M")
        if formatted:
            formatted_now = self.colors["cyan"] + "[" + now + "]" + self.colors["end"]
            return formatted_now
        else:
            return now

    def start_accepting(self):
        while True:
            connection, address = self.socket.accept()
            timestamp = self.timestamp(formatted=False)
            thread = Thread(target=self.handle_client, args=[connection, address, timestamp])
            thread.start()

    def handle_client(self, connection, address, timestamp):
        username = receive_message(connection)
        self.clients[connection] = {"username": username, "address": address, "join_time": timestamp}
        timestamp = self.now()
        print("{} [NEW CONNECTION] {} connected.".format(timestamp, username))

        self.send_message(connection, "{} Connected to server with username: {}".format(timestamp, self.clients[connection]["username"]))

        # send previous messages to the newly connected user
        len_messages = len(self.messages)
        self.send_message(connection, str(len_messages)
        for i in range(len_messages):
            self.send_message(connection, self.messages[i]["sent"])


    def receive_message(self, connection):
        while True:
            message_length = connection.recv(self.header_length).decode(self.format)
            message = connection.recv(int(message_length)).decode(self.format)
        return message

    def send_message(self, connection, message):
        try:
            connection.sendall(bytes())







