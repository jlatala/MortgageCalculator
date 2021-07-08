import unittest
from credit_calculator.src.credit_calculator import CreditCalculator
from credit_calculator.src.declining_credit import DecliningCredit
from credit_calculator.src.fixed_credit import FixedCredit


class TestCreditCalculator(unittest.TestCase):
    def setUp(self):
        self.cc1 = CreditCalculator()

    def new_credit(self, credit_cls):
        fc1 = credit_cls(500_000, 300, 0.04)
        self.cc1.new_credit(fc1)

    def test_fixed_credit(self):
        self.new_credit(FixedCredit)
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 791_755.26)
        self.assertEqual(self.cc1.get_total_principal(), 500_000)
        self.assertEqual(self.cc1.get_total_interest(), 291_755.26)
        self.assertEqual(self.cc1.get_number_of_installments(), 300)

    def test_declining_credit(self):
        self.new_credit(DecliningCredit)
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 750_833.33)
        self.assertEqual(self.cc1.get_total_principal(), 500_000)
        self.assertEqual(self.cc1.get_total_interest(), 250_833.33)
        self.assertEqual(self.cc1.get_number_of_installments(), 300)

    def test_fixed_credit_overpay_decrease_installment(self):
        self.new_credit(FixedCredit)
        overpayments = {36: 50_000, 120: 30_000}
        self.cc1.add_overpayment(overpayments)
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 756548.22)
        self.assertEqual(self.cc1.get_total_principal(), 420_000)
        self.assertEqual(self.cc1.get_total_interest(), 256548.22)
        self.assertEqual(self.cc1.get_number_of_installments(), 300)
        self.assertEqual(self.cc1.get_total_overpayment(), 80_000)

    def test_declining_credit_overpay_decrease_installment(self):
        self.new_credit(DecliningCredit)
        overpayments = {36: 50_000, 120: 30_000}
        self.cc1.add_overpayment(overpayments)
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 719_700)
        self.assertEqual(self.cc1.get_total_principal(), 420_000)
        self.assertEqual(self.cc1.get_total_interest(), 219_700)
        self.assertEqual(self.cc1.get_number_of_installments(), 300)
        self.assertEqual(self.cc1.get_total_overpayment(), 80_000)

    def test_fixed_credit_overpay_decrease_loan_term(self):
        self.new_credit(FixedCredit)
        overpayments = {36: 50_000, 120: 30_000}
        self.cc1.add_overpayment(overpayments, o_type="decrease_loan_term")
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 713402.13)
        self.assertEqual(self.cc1.get_total_principal(), 420_000)
        self.assertEqual(self.cc1.get_total_interest(), 213402.13)
        self.assertEqual(self.cc1.get_number_of_installments(), 240)
        self.assertEqual(self.cc1.get_total_overpayment(), 80_000)

    def test_declining_credit_overpay_decrease_loan_term(self):
        self.new_credit(DecliningCredit)
        overpayments = {36: 50_000, 120: 30_000}
        self.cc1.add_overpayment(overpayments, o_type="decrease_loan_term")
        self.cc1.calculate()

        self.assertEqual(self.cc1.get_total(), 695100)
        self.assertEqual(self.cc1.get_total_principal(), 420_000)
        self.assertEqual(self.cc1.get_total_interest(), 195100)
        self.assertEqual(self.cc1.get_number_of_installments(), 252)
        self.assertEqual(self.cc1.get_total_overpayment(), 80_000)


if __name__ == "__main__":
    unittest.main()
