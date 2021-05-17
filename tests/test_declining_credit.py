import unittest
from collections.abc import Iterator
from credit_calculator.src.declining_credit import DecliningCredit


class TestDecliningCredit(unittest.TestCase):

    def setUp(self):
        self.c1 = DecliningCredit(300_000, 30, 0.04)

    def test_first_installment(self):
        self.assertEqual(next(self.c1).value, 1833.33)

    def test_fixed_credit_is_iterator(self):
        self.assertIsInstance(self.c1, Iterator)

    def test_last_installment(self):
        last = None
        for last in self.c1:
            pass

        self.assertEqual(last.value, 836.11)

    def test_number_of_installments(self):
        for i, _ in enumerate(self.c1):
            pass

        self.assertEqual(i, 359)
        with self.assertRaises(StopIteration):
            next(self.c1)


if __name__ == '__main__':
    unittest.main()
