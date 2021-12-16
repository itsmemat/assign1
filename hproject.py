#!/usr/bin/env python3

from os import error
from datetime import datetime
import socket
import pickle
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


ftpAttempts = list()
webAttempts = list()

class ClientThread(threading.Thread):
    def __init__(self, channel, details):
        self.channel = channel
        self.details = details
        threading.Thread.__init__ ( self )

    def run(self):
        print('Received connection:', self.details[0], self.details[1])
        request = self.channel.recv(1024)
        ftpAttempts.append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " " + str(self.details[0]) + ":" + str(self.details[1]) )
        self.channel.send(b"<h1>We see You !</h1>")
        self.channel.close()
        print('Closed connection:', self.details [ 0 ])
        print('List of FTP Connection Attempts', ftpAttempts)

class HoneyPotWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Found You</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is a Honey Pot</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))



def startFTPServer(name):   
    host = '127.0.0.1'
    port = 80
    print('Starting a Honey Pot FTP Server on %s:%s\n'%(host, port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while True:
        channel, details = s.accept()
        ClientThread(channel, details).start()


def startWebServer(name):
    host = "localhost"
    port = 8080
    print('Honey Pot Webserver is up on http://%s:%s\n'%(host, port))
    webServer = HTTPServer((host, port), HoneyPotWebServer)
    webServer.serve_forever()

def report_gen():
    print(ftpAttempts)

def menu():

    print("------------------MENU-------------------")
    print("Press 1 to Start and Monitor a FTP Server")
    print("Press 2 to Start and Monitor a Web Server")
    print("Press 3 to View Report")

    choice = int(input())

    if choice == 1:
        x = threading.Thread(target=startFTPServer, args=("FTP Server",))
        x.start()

      
    elif choice == 2:
        x2 = threading.Thread(target=startWebServer, args=("Web Server",))
        x2.start()


    elif choice == 3:
        x3 = threading.Thread(target=report_gen, args=("Honeypot Access Report",))
        x3.start()

    else:
        menu()

if __name__ == '__main__':
    menu()
