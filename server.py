import socket
import pickle
import random


class Server(object):

    def __init__(self):
        self.q = None
        self.g = None
        self.h = None
        self.y1 = None
        self.y2 = None
        self.r1 = None
        self.r2 = None
        self.challenge = None
        self.conn, self.address = self.connect_client()

    def connect_client(self):
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        server_socket.listen(1)
        self.conn, address = server_socket.accept()  # accept new connection
        return self.conn, address

    def assign_system_params(self, data):
        self.q = data[0]
        self.g = data[1]
        self.h = data[2]
        self.y1 = data[3]
        self.y2 = data[4]

    def receive_commitment(self, data):
        self.r1 = data[0]
        self.r2 = data[1]

    def send_challenge(self):
        self.challenge = random.randint(1, 10)
        self.conn.send(pickle.dumps(self.challenge))
        print("Challenge Sent to Client ")

    def verify_response(self, data):
        s = data[0]
        calc1 = (pow(self.g, s, self.q) * pow(self.y1, self.challenge, self.q)) % self.q
        calc2 = (pow(self.h, s, self.q) * pow(self.y2, self.challenge, self.q)) % self.q

        if self.r1 == calc1 and self.r2 == calc2:
            print("Authentication Successful")
            resp = "Success"
        else:
            print("Authentication Un-Successful")
            resp = "Failure"
        self.conn.send(pickle.dumps(resp))

    def respond(self):
        print("Connection from: " + str(self.address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            # g, h, x, y1, y2 = [int(i) for i in conn.recv(2048).decode('utf-8').split('\n')]
            data = self.conn.recv(1024)

            if not data:
                print("Auth Process complete, Closing connection")
                break
            data = pickle.loads(data)

            if data[-1] == "System":
                print("Setting System params")
                self.assign_system_params(data)

            if data[-1] == "Commitment":
                print("Received Commitment")
                self.receive_commitment(data)
                self.send_challenge()

            if data[-1] == "Verify":
                self.verify_response(data)


if __name__ == '__main__':
    print("Starting up the server....")
    server = Server()
    server.respond()

