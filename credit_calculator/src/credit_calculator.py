from .utils import round_currency


class CreditCalculator:
    def __init__(self):
        self.__credit = None
        self.__overpayments = {}
        self.__installments = None
        self.__overpayment_type = None

    def new_credit(self, credit):
        self.__credit = credit
        self.__installments = []

    def add_overpayment(self, overpayment, o_type='decrease_installment'):
        self.__overpayments.update(overpayment)
        self.__overpayment_type = o_type

    def calculate(self, init_month=1):
        for month, installment in enumerate(self.__credit, start=init_month):
            self.__installments.append(installment)
            if month in self.__overpayments:
                amount = self.__overpayments[month]
                self.__credit = self.__credit.overpay(
                    amount, self.__overpayment_type)
                self.calculate(month + 1)
                break

    def get_installments(self):
        return self.__installments[:]

    @round_currency
    def get_total(self):
        return sum(self.__installments) + self.get_total_overpayment()

    @round_currency
    def get_total_principal(self):
        return sum([i.principal for i in self.__installments])

    @round_currency
    def get_total_interest(self):
        return sum([i.interest for i in self.__installments])

    def get_total_overpayment(self):
        return sum(self.__overpayments.values())
