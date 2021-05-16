
def round_currency(func):
    def rounded(*args, **kwargs):
        return float(round(func(*args, **kwargs), 2))

    return rounded


class Installment:
    def __init__(self, principal, interest):
        self.__principal = principal
        self.__interest = interest

    @round_currency
    def get_principal(self):
        return self.__principal

    @round_currency
    def get_interest(self):
        return self.__interest

    @property
    @round_currency
    def value(self):
        return self.__principal + self.__interest

    @round_currency
    def __add__(self, other):
        return self.value + other.value

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__principal}, {self.__interest})'

    def __str__(self):
        return f'total={self.value:.2f}; principal={self.__principal:.2f}; interest={self.__interest:.2f}'
