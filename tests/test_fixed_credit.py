import unittest
from collections.abc import Iterator
from credit_calculator.src.fixed_credit import FixedCredit


class TestFixedCredit(unittest.TestCase):
    def setUp(self):
        self.c1 = FixedCredit(300_000, 360, 0.04)

    def test_all_totals(self):
        self.assertEqual(
            [i.get_rounded_total() for i in self.c1], [1432.25 for _ in range(360)]
        )

    def test_paid(self):
        total_sum = sum([i.total for i in self.c1])
        total_sum = round(total_sum, 2)
        self.assertEqual(total_sum, self.c1.paid)

    def test_fixed_credit_is_iterator(self):
        self.assertIsInstance(self.c1, Iterator)

    def test_number_of_installments(self):
        for i, _ in enumerate(self.c1):
            pass

        self.assertEqual(i, 359)
        with self.assertRaises(StopIteration):
            next(self.c1)

    def test_single_installment(self):
        self.assertEqual(next(self.c1).get_rounded_total(), 1432.25)
        # should not change over next payments
        self.assertEqual(next(self.c1).get_rounded_total(), 1432.25)


if __name__ == "__main__":
    unittest.main()
