import pandas as pd
from .utils import round_currency


class CreditCalculator:
    def __init__(self):
        self.__credit = None
        self.__overpayments = {}
        self.__overpayment_type = None

    def new_credit(self, credit):
        self.__credit = credit
        self.credit_df = pd.DataFrame(columns=["principal", "interest", "overpayment"])

    def add_overpayment(self, overpayment, o_type="decrease_installment"):
        self.__overpayments.update(overpayment)
        self.__overpayment_type = o_type

    def calculate(self, init_month=1):
        for month, installment in enumerate(self.__credit, start=init_month):
            self.credit_df = self.credit_df.append(installment, ignore_index=True)
            if month in self.__overpayments:
                amount = self.__overpayments[month]
                self.credit_df.iloc[-1]["overpayment"] = amount
                self.__credit = self.__credit.overpay(amount, self.__overpayment_type)
                self.calculate(month + 1)
                break

    def get_number_of_installments(self):
        return len(self.credit_df)

    @round_currency
    def get_total(self):
        return sum(self.credit_df.sum())

    @round_currency
    def get_total_principal(self):
        return self.credit_df["principal"].sum()

    @round_currency
    def get_total_interest(self):
        return self.credit_df["interest"].sum()

    def get_total_overpayment(self):
        return self.credit_df["overpayment"].sum()
