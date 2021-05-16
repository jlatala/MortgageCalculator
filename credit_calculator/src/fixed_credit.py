from credit_calculator.src.credit import Credit
from credit_calculator.src.installment import Installment


class FixedCredit(Credit):
    def __init__(self, loan_amount, loan_term, interest_rate, pay_back_freq=12, currency="zł"):
        super().__init__(loan_amount, loan_term, interest_rate, pay_back_freq, currency)

    def __next__(self):
        if self.loan_amount - self.principal_paid < 0.01:
            raise StopIteration

        # installment = S * q^n * (q-1)/(q^n-1)
        q = 1 + (self.interest_rate / self.pay_back_freq)
        qn = q ** self.n_installments
        total = self.loan_amount * qn * (q - 1) / (qn - 1)
        interest = (self.loan_amount - self.principal_paid) * \
            self.interest_rate / self.pay_back_freq
        principal = total - interest

        self.principal_paid += principal
        self.interest_paid += interest

        return Installment(principal, interest)
