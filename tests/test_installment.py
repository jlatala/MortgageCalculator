import unittest
from credit_calculator.src.installment import Installment


class TestInstallment(unittest.TestCase):

    def setUp(self):
        self.i1 = Installment(302.41, 212.01)
        self.i2 = Installment(105, 400.4)

    def test_add(self):
        self.assertEqual(self.i1 + self.i2, 1019.82)

    def test_get_principal(self):
        self.assertEqual(self.i1.get_principal(), 302.41)
        self.assertEqual(self.i2.get_principal(), 105.00)

    def test_get_interest(self):
        self.assertEqual(self.i1.get_interest(), 212.01)
        self.assertEqual(self.i2.get_interest(), 400.40)

    def test_sum(self):
        i_list = [self.i1, self.i2]

        self.assertEqual(sum(i_list), 1019.82)

    def test_repr(self):
        self.assertEqual(repr(self.i1), 'Installment(302.41, 212.01)')

    def test_str(self):
        self.assertEqual(
            str(self.i2), 'total=505.40; principal=105.00; interest=400.40')

    def test_value_property(self):
        self.assertEqual(self.i1.value, 514.42)
        self.assertEqual(self.i2.value, 505.40)

        self.i1.__principal = 999.99
        # should not change the value - private variable
        self.assertEqual(self.i1.value, 514.42)


if __name__ == '__main__':
    unittest.main()
