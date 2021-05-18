from .utils import round_currency


class Installment:
    def __init__(self, principal, interest):
        self.principal = principal
        self.interest = interest

    @round_currency
    def get_principal(self):
        return self.principal

    @round_currency
    def get_interest(self):
        return self.interest

    @property
    def total(self):
        return self.principal + self.interest

    @round_currency
    def get_rounded_total(self):
        return self.total

    def __add__(self, other):
        try:
            return self.total + other.total
        except AttributeError:
            return self.total + other

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.principal}, {self.interest})'

    def __str__(self):
        return f'total={self.get_rounded_total():.2f}; principal={self.principal:.2f}; interest={self.interest:.2f}'
