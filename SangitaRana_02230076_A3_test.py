import unittest
from SangitaRana_02230076_A3 import BankAccount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc1 = BankAccount("12345", "Alice", "1111", 1000)
        self.acc2 = BankAccount("54321", "Bob", "2222", 500)

    def test_deposit_positive(self):
        self.acc1.deposit(200)
        self.assertEqual(self.acc1.balance, 1200)
        self.assertIn("Deposited Nu.200.00", self.acc1.transactions[-1])

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.acc1.deposit(-100)

    def test_withdraw_success(self):
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.balance, 700)
        self.assertIn("Withdrew Nu.300.00", self.acc1.transactions[-1])

    def test_withdraw_insufficient(self):
        with self.assertRaises(ValueError):
            self.acc2.withdraw(600)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.acc1.withdraw(-10)

    def test_transfer_success(self):
        self.acc1.transfer(400, self.acc2)
        self.assertEqual(self.acc1.balance, 600)
        self.assertEqual(self.acc2.balance, 900)
        self.assertIn("Sent Nu.400.00 to Bob", self.acc1.transactions[-1])
        self.assertIn("Received Nu.400.00 from Alice", self.acc2.transactions[-1])

    def test_transfer_to_self(self):
        with self.assertRaises(ValueError):
            self.acc1.transfer(100, self.acc1)

    def test_transfer_insufficient(self):
        with self.assertRaises(ValueError):
            self.acc2.transfer(1000, self.acc1)

    def test_transfer_negative(self):
        with self.assertRaises(ValueError):
            self.acc1.transfer(-50, self.acc2)

    def test_mobile_topup_success(self):
        self.acc1.mobile_topup(100, "17123456")
        self.assertEqual(self.acc1.balance, 900)
        self.assertIn("Mobile top-up Nu.100.00 to 17123456", self.acc1.transactions[-1])

    def test_mobile_topup_insufficient(self):
        with self.assertRaises(ValueError):
            self.acc2.mobile_topup(1000, "17123456")

    def test_mobile_topup_negative(self):
        with self.assertRaises(ValueError):
            self.acc1.mobile_topup(-10, "17123456")

if __name__ == "__main__":
    unittest.main()