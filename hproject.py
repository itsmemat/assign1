# Echo server program
import socket
import datetime
import threading
import time


import http.server
import socketserver





ftpAttempts = list()

webAttempts = list()

print("----------------------------")

def startFTPthread(name):
    print("Starting FTP server.... port 21")
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 21              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            
            dt = datetime.datetime.now()
            connectionDetails = addr[0]
            print(dt)
            print(connectionDetails)
            
            ftpAttempts.append(dt + " " +connectionDetails)
            
            
            
            while True:
                data = conn.recv(1024)
                print(data)
                if not data: break
                conn.sendall(data)


def startWebServer(name):
    print("starting web server...")
    PORT = 80

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        dt = datetime.datetime.now()
        webAttempts.append(dt)
        httpd.serve_forever()


                
                
x = threading.Thread(target=startFTPthread, args=("Thread 1",))

x.start()


                
x2 = threading.Thread(target=startWebServer, args=("Thread 2",))

x2.start()



# after 5 minutes, save all the outputs
startTime = time.time()
endTime = startTime + 30


    
    

# start second thread...........