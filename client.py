import socket
import random
from Crypto.Util import number
import pickle


class Client(object):

    def __init__(self, secret):
        self.client_socket = socket.socket()  # instantiate
        self.q = number.getPrime(random.randint(500, 600))
        self.k = secret
        self.g = 3
        self.h = 5
        self.x = 2
        self.y1 = pow(self.g, self.x, self.q)
        self.y2 = pow(self.h, self.x, self.q)
        self.challenge = 0
        print(self.k, self.x, self.q, self.g, self.h, self.y1, self.y2)

    def setup_connection(self):
        host = socket.gethostname()  # as both code is running on same pc
        port = 5000  # socket server port number
        self.client_socket.connect((host, port))  # connect to the server
        return

    def server_call(self):
        system_params = []
        system_params.extend((self.q, self.g, self.h, self.y1, self.y2, "System"))
        print(system_params)
        data = pickle.dumps(system_params)
        self.client_socket.send(data)

        return

    def send_commit(self, r1, r2):
        print("Value of random commit/secret is: ", self.k)
        print("Value of commits r1 and r2 is: ", r1, r2)
        commitment = []
        commitment.extend((r1, r2, "Commitment"))
        data = pickle.dumps(commitment)

        while self.challenge == 0:
            self.client_socket.send(data)
            print("Sent commit")
            data = self.client_socket.recv(1024)
            print("received challenge", pickle.loads(data))
            self.challenge = pickle.loads(data)
        return

    def register_commit(self):
        r1 = pow(self.g, self.k, self.q)
        r2 = pow(self.h, self.k, self.q)
        self.send_commit(r1, r2)
        return

    def send_challenge_response(self, k):
        print("Received challenge: ",k)
        s = (k - self.challenge * self.x) % self.q

        if s < 0:
            print("Auth witll fail, low value of secret, please supply higher value")

        verify = []
        verify.extend((s, "Verify"))
        print("The response is sent to server")
        data = pickle.dumps(verify)
        self.client_socket.send(data)
        data = self.client_socket.recv(1024)
        final_response = pickle.loads(data)
        self.client_socket.close()
        return final_response


if __name__ == '__main__':
    k = input("Enter the secret value to commit (atleast 3 digit or higher):  ")
    start = Client(int(k))
    start.setup_connection()
    start.server_call()
    start.register_commit()

    print("Commitment is shared with server")
    k = input("Enter the secret value (one used to register) to authenticate: ")
    response = start.send_challenge_response(int(k))

    if response == "Success":
        print("User Authenticated")
    if response == "Failure":
        print("Authentication Failed")

