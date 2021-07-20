from .credit import Credit


class DecliningCredit(Credit):
    def __init__(self, loan_amount, loan_term, interest_rate, currency="$"):
        super().__init__(loan_amount, loan_term, interest_rate, currency)

    def get_principal_and_interest(self, capital):
        principal = self.loan_amount / self.n_installments
        interest = (self.loan_amount - capital) * self.interest_rate / self.pay_back_freq

        if principal > self.loan_amount - capital:
            principal = self.loan_amount - capital

        return principal, interest

    def __copy__(self):
        return DecliningCredit(self.loan_amount, self.n_installments, self.interest_rate, self.currency)