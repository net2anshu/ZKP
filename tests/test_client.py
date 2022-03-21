import unittest
from client import *
from server import *

class MyTestCase(unittest.TestCase):
    def test_system_params(self):
        test = Client(int(999))
        test.q = 1837344378622726836945768474310130710390713910791487165163532323013178013938467343
        self.assertEqual(test.g, 3)
        self.assertEqual(test.h, 5)
        self.assertEqual(test.x, 2)
        self.assertEqual(test.k, 999)
        self.assertEqual(test.y1, 9)
        self.assertEqual(test.y2, 25)

    def test_register_commit(self):
        test = Client(int(999))
        test.q = 1837344378622726836945768474310130710390713910791487165163532323013178013938467343
        r1 = pow(test.g, test.k, test.q)
        r2 = pow(test.h, test.k, test.q)
        self.assertEqual(r1, 91046711555789170144244732759386889269112755980918723068568132802884365841330451)
        self.assertEqual(r2, 926989929529272575857454939610394323902617612436596596108344177373302188750312697)

    def test_send_challenge_response(self):
        test = Client(int(999))
        test.q = 1837344378622726836945768474310130710390713910791487165163532323013178013938467343
        test.challenge = 10
        response = (test.k - test.challenge * test.x) % test.q
        self.assertEqual(response, 979)

    def test_server_side(self):
        test = Client(int(999))
        test.q = 1837344378622726836945768474310130710390713910791487165163532323013178013938467343
        test.challenge = 10
        resp = (test.k - test.challenge * test.x) % test.q
        self.assertEqual(resp, 979)


if __name__ == '__main__':
    unittest.main()
