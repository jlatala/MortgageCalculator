from credit_calculator.src.credit import Credit
from credit_calculator.src.installment import Installment


class DecliningCredit(Credit):
    def __init__(self, loan_amount, loan_term, interest_rate, pay_back_freq=12, currency="zł"):
        super().__init__(loan_amount, loan_term, interest_rate, pay_back_freq, currency)

    def __next__(self):
        if self.loan_amount - self.principal_paid < 0.01:
            raise StopIteration

        principal = self.loan_amount / self.n_installments
        interest = (self.loan_amount - self.principal_paid) * \
            self.interest_rate / self.pay_back_freq

        self.principal_paid += principal
        self.interest_paid += interest

        return Installment(principal, interest)
