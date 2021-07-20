from typing import Type
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from credit_calculator.web.app import app
from credit_calculator.src.credit_calculator import CreditCalculator
from credit_calculator.src.fixed_credit import FixedCredit
from credit_calculator.src.declining_credit import DecliningCredit


cc = CreditCalculator()


@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("df-table", "data"),
    Input("credit-memory", "data"),
    State("loan-slider", "value"),
    State("loan-term-slider", "value"),
    State("interest-rate-slider", "value"),
)
def update_figures(data, loan, years, interest_rate):
    df = pd.DataFrame(data)

    bar_fig = px.bar(df, barmode="group")
    bar_fig.update_layout(transition_duration=500)

    pie_fig = px.pie(df.sum(), values=0)
    pie_fig.update_layout(transition_duration=1000)

    df["total"] = df.sum(axis=1)

    return bar_fig, pie_fig, df.to_dict(orient="records")


@app.callback(
    Output("loan-text", "children"),
    Input("loan-slider", "drag_value"),
)
def update_loan_amount(loan):

    return f"Loan amount {loan:,}$"


@app.callback(
    Output("loan-term-text", "children"),
    Input("loan-term-slider", "drag_value"),
)
def update_loan_length(years):
    if years == 1:
        return f"Loan lenght {years} year"
    return f"Loan lenght {years} years"


@app.callback(
    Output("interest-rate-text", "children"),
    Input("interest-rate-slider", "drag_value"),
)
def update_interest_rate(rate):
    return f"Interest rate {rate:.1f}%"


@app.callback(
    Output("credit-memory", "data"),
    Input("loan-type-radio", "value"),
    Input("loan-slider", "value"),
    Input("loan-term-slider", "value"),
    Input("interest-rate-slider", "value"),
    Input("monthly-overpayment-input", "value"),
    Input("overpay-behavior-radio", "value"),
    Input("add-overpayment-button", "n_clicks"),
    State("overpay-dates-dropdown", "value"),
    State("single-overpayment-input", "value"),
)
def calculate_mortgage(
    loan_type,
    loan,
    years,
    interest_rate,
    monthly_overpay_amount,
    overpay_type,
    n_clicks,
    single_overpay_month,
    single_overpay_amount,
):
    trigger = dash.callback_context.triggered[0]["prop_id"]
    print(dash.callback_context.triggered)
    if (
        trigger
        in [
            "loan-type-radio.value",
            "loan-slider.value",
            "loan-term-slider.value",
            "interest-rate-slider.value",
        ]
        or cc.credit is None
    ):
        print(1)
        credit = get_new_credit(loan_type, loan, years, interest_rate)
        cc.new_credit(credit)
    else:
        print(2)
        cc.reset_credit()

    if trigger in ["monthly-overpayment-input.value", "overpay-behavior-radio.value"]:
        print(3)
        add_monthly_overpayment(
            cc.credit.n_installments, monthly_overpay_amount, overpay_type
        )
    if trigger == "add-overpayment-button.n_clicks":
        print(4)
        add_single_overpayment(single_overpay_month, single_overpay_amount, overpay_type)

    print(5)
    cc.calculate()

    return cc.credit_df.to_dict()


def get_new_credit(loan_type, loan, years, interest_rate):
    if loan_type == "fixed":
        return FixedCredit(loan, years * 12, interest_rate / 100)
    if loan_type == "declining":
        return DecliningCredit(loan, years * 12, interest_rate / 100)


def add_single_overpayment(month, amount, overpay_type):
    if month is not None:
        cc.add_overpayment({int(month): amount}, overpay_type)


def add_monthly_overpayment(n_months, amount, overpay_type):
    for i in range(n_months):
        cc.add_overpayment({i: amount}, overpay_type)


@app.callback(
    Output("overpay-dates-dropdown", "options"),
    Output("overpay-dates-dropdown", "value"),
    Input("credit-memory", "data"),
)
def fill_in_dropdown_with_dates(data):
    df = pd.DataFrame(data)
    options = [{"label": f"month {int(date)+1}", "value": date} for date in df.index]

    return options, options[0]["value"]
