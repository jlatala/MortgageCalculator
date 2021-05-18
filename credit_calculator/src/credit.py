from abc import ABC, abstractmethod
from .installment import Installment
from .utils import round_currency


class Credit(ABC):
    pay_back_freq = 12

    def __init__(self, loan_amount, loan_term, interest_rate, currency="$"):
        self.loan_amount = loan_amount
        self.n_installments = loan_term
        self.interest_rate = interest_rate
        self.currency = currency

        self.total_principal = 0
        self.total_interest = 0
        self.total_overpayment = {
            'decrease_installment': 0,
            'decrease_loan_term': 0
        }
        self._overpayment = 0
        self.i_month = 0

    @property
    @round_currency
    def paid(self):
        return self.total_principal + self.total_interest + sum(self.total_overpayment.values())

    def __next__(self):
        overp = self.total_overpayment['decrease_loan_term']
        capital = self.total_principal + overp
        if self.loan_amount - capital < 0.01:
            raise StopIteration

        self.i_month += 1

        principal, interest = self.get_principal_and_interest(capital)

        self.total_principal += principal
        self.total_interest += interest

        return Installment(principal, interest)

    @abstractmethod
    def get_principal_and_interest(self, capital):
        ...

    def __iter__(self):
        return self

    def overpay(self, amount, o_type='decrease_installment'):
        self.total_overpayment[o_type] += amount

        if o_type == 'decrease_loan_term':
            return self

        loan_amount = self.loan_amount - self.total_principal - amount
        loan_term = self.n_installments - self.i_month
        interest_rate = self.interest_rate
        currency = self.currency

        cls = self.__class__

        return cls(loan_amount, loan_term, interest_rate, currency)
