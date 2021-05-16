from abc import ABC, abstractmethod


class Credit(ABC):
    def __init__(self, loan_amount, loan_term, interest_rate, pay_back_freq=12, currency="zł"):
        self.loan_amount = loan_amount
        self.loan_term = loan_term
        self.interest_rate = interest_rate
        self.pay_back_freq = pay_back_freq
        self.currency = currency
        self.n_installments = loan_term * pay_back_freq

        self.principal_paid = 0
        self.interest_paid = 0

    @property
    def paid(self):
        return self.principal_paid + self.interest_paid

    @abstractmethod
    def __next__(self):
        ...

    def __iter__(self):
        return self
