#!/usr/bin/env python3

from os import error
from datetime import datetime
import time
import socket
import pickle
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import report
from report import access_report_gen
import csv


ftpAttempt=[]
ftpAttemptArray =[]
webAttempts = list()

class ClientThread(threading.Thread):
    def __init__(self, host, port, channel, details, id):
        self.host= host
        self.port=port
        self.channel = channel
        self.details = details
        self.id = id
        threading.Thread.__init__ ( self )

    def run(self):
            print('Received connection:', self.details[0], self.details[1] , self.id)
            request = self.channel.recv(1024)
            ftpAttempt.append(datetime.now().strftime("%m/%d/%Y"))
            ftpAttempt.append(datetime.now().strftime("%H:%M:%S"))
            ftpAttempt.append(str(self.details[0]))
            ftpAttempt.append(str(self.details[1]))
            ftpAttempt.append(str(self.host)) 
            ftpAttempt.append(str(self.port))  
            write_csv(ftpAttempt)
            ftpAttempt.clear()
            self.channel.send(b"<h1>We see You !</h1>")
            self.channel.close()
            print('Closed connection:', self.details [ 0 ])
   


class HoneyPotWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Found You</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is a Honey Pot</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

def write_csv(rowdata):
    with open('ftp_report.csv','a',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(rowdata)

def startFTPServer(name,timeout):  
    host = '127.0.0.1'
    port = 80
    id = 0
    print('Starting a Honey Pot FTP Server on %s:%s\n'%(host, port))
    header_row=['Date', 'Time','Source Host', 'Source Port', 'Target Host', 'Target Port']
    with open('ftp_report.csv','w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header_row)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    timeout = time.time() + int(timeout)*1
    while True:
        channel, details = s.accept()
        if time.time() > timeout:
            menu()
            break
        ClientThread(host,port,channel, details, id).start()
        id +=1
    print('Shutting Down the Honey Pot FTP Server on %s:%s\n'%(host, port))
    
def startWebServer(name):
    host = "localhost"
    port = 8080
    print('Honey Pot Webserver is up on http://%s:%s\n'%(host, port))
    webServer = HTTPServer((host, port), HoneyPotWebServer)
    webServer.serve_forever()

def report_gen(name):
    
    #print(ftpAttempts)
    access_report_gen()
    

def menu():

    print("------------------MENU-------------------")
    print("Press 1 to Start and Monitor a FTP Server")
    print("Press 2 to Start and Monitor a Web Server")
    print("Press 3 to Generate Access Report")
    print("------------------MENU-------------------")

    choice = int(input())

    if choice == 1:
        timeout = input("How long would you like the Server to be up ? (Time in Seconds)")
        x = threading.Thread(target=startFTPServer, args=("FTP Server",timeout,))
        x.start()
        #menu()
              
    elif choice == 2:
        x2 = threading.Thread(target=startWebServer, args=("Web Server",))
        x2.start()
        menu()

    elif choice == 3:
        x3 = threading.Thread(target=report_gen, args=("Honeypot Access Report",))
        x3.start()
        menu()
        
    else:
        menu()

if __name__ == '__main__':
    menu()
