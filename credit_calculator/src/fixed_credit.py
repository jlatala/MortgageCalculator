from .credit import Credit


class FixedCredit(Credit):
    def __init__(self, loan_amount, loan_term, interest_rate, currency="$"):
        super().__init__(loan_amount, loan_term, interest_rate, currency)

    def get_principal_and_interest(self, capital):
        # installment = S * q^n * (q-1)/(q^n-1)
        q = 1 + (self.interest_rate / self.pay_back_freq)
        qn = q ** self.n_installments
        total = self.loan_amount * qn * (q - 1) / (qn - 1)
        interest = (self.loan_amount - capital) * \
            self.interest_rate / self.pay_back_freq
        principal = total - interest
        if self.loan_amount - capital - principal < 0.01:
            principal += self.loan_amount - capital - principal

        return principal, interest
