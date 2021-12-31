import unittest
from credit_calculator.src.installment import Installment


class TestInstallment(unittest.TestCase):
    def setUp(self):
        self.i1 = Installment(302.41, 212.01)
        self.i2 = Installment(105, 400.4, 100.0)
        self.i3 = Installment(9999.99, 0)

    def test_add(self):
        self.assertEqual(self.i1 + self.i2, 1119.82)

    def test_get_principal(self):
        self.assertEqual(self.i1.get_principal(), 302.41)
        self.assertEqual(self.i2.get_principal(), 105.00)

    def test_get_interest(self):
        self.assertEqual(self.i1.get_interest(), 212.01)
        self.assertEqual(self.i2.get_interest(), 400.40)

    def test_sum(self):
        i_list = [self.i1, self.i2, self.i3]

        self.assertEqual(sum(i_list[:2]), 1119.82)
        self.assertEqual(sum(i_list), 11119.81)

    def test_repr(self):
        self.assertEqual(repr(self.i1), "Installment(302.41, 212.01, 0.0)")

    def test_str(self):
        self.assertEqual(str(self.i2), "total=605.40; principal=105.00; interest=400.40; overpayment=100.00")

    def test_total_property(self):
        self.assertEqual(self.i1.get_rounded_total(), 514.42)
        self.assertEqual(self.i2.get_rounded_total(), 605.40)


if __name__ == "__main__":
    unittest.main()
