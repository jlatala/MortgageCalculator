import pandas as pd
from copy import copy
from datetime import date
from dateutil.relativedelta import relativedelta
from .utils import round_currency


class CreditCalculator:
    def __init__(self):
        self.credit = None
        self.__overpayments = {}
        self.__overpayment_type = None

    def new_credit(self, credit):
        self.credit = credit
        self.credit_df = pd.DataFrame(columns=["principal", "interest", "overpayment"])

    def reset_credit(self):
        credit = copy(self.credit)
        self.new_credit(credit)

    def add_overpayment(self, overpayment, o_type="decrease_installment"):
        self.__overpayments.update(overpayment)
        self.__overpayment_type = o_type

    def calculate(self, init_month=1):
        for month, installment in enumerate(self.credit, start=init_month):
            self.credit_df = self.credit_df.append(installment, ignore_index=True)
            if month in self.__overpayments:
                amount = self.__overpayments[month]
                self.credit_df.iloc[-1]["overpayment"] = amount
                self.credit = self.credit.overpay(amount, self.__overpayment_type)
                self.calculate(month + 1)
                break

        self.set_dates_as_index()

    def set_dates_as_index(self, start_date=None):
        if start_date is None:
            start_date = date.today()

        n_rows = len(self.credit_df)
        self.credit_df["date"] = [
            start_date + relativedelta(months=+i) for i in range(n_rows)
        ]
        self.credit_df = self.credit_df.set_index("date")

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
