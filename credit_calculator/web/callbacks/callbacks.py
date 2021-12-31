from typing import Type
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
from credit_calculator.web.app import app
from credit_calculator.src.credit_calculator import CreditCalculator
from credit_calculator.src.fixed_credit import FixedCredit
from credit_calculator.src.declining_credit import DecliningCredit


COLOR_MAP = {
    "principal": "#1F77B4",
    "interest": "#FF7F0E",
    "overpayment": "#2CA02C",
}


@app.callback(
    Output("summary-heading-text", "children"),
    Input("credit-memory", "data"),
)
def update_summary(data):
    df = pd.DataFrame.from_dict(data)
    df.index = pd.DatetimeIndex(df.index)
    installment = df.iloc[0].sum()
    summary = [f"Your monthly payment {installment:,.2f}$"]

    return summary


@app.callback(
    Output("summary-info-text", "children"),
    Input("credit-memory", "data"),
)
def update_summary(data):
    df = pd.DataFrame.from_dict(data)
    df.index = pd.DatetimeIndex(df.index)
    payoff_date = df.index[-1]
    total_principal = df["principal"].sum() + df["overpayment"].sum()
    total_interest = df["interest"].sum()
    total = sum(df.sum())
    n_payments = len(df.index)
    years = n_payments // 12
    months = n_payments % 12
    duration = f"{years} years" if years else ""
    duration += ", " if years and months else ""
    duration += f"{months} months" if months else ""
    summary = [f"Payoff date {payoff_date:%d-%m-%Y} ({duration})"]
    summary.append(html.Br())
    summary += [f"Total principal paid {round(total_principal):,}$"]
    summary.append(html.Br())
    summary += [f"Total interest paid {round(total_interest):,}$"]
    summary.append(html.Br())
    summary += [f"Total paid {round(total):,}$"]

    return summary


@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Input("credit-memory", "data"),
    State("loan-slider", "value"),
    State("loan-term-slider", "value"),
    State("interest-rate-slider", "value"),
)
def update_figures(data, loan, years, interest_rate):
    df = pd.DataFrame.from_dict(data)
    df.index = pd.DatetimeIndex(df.index)
    df = df[["principal", "interest", "overpayment"]]

    area_fig = px.area(
        df,
        labels={"date": "years", "value": "amount [$]"},
        template="simple_white",
        color_discrete_map=COLOR_MAP,
    )
    area_fig.update_layout(transition_duration=500)
    area_fig.update_xaxes(type="date")
    area_fig.update_yaxes(secondary_y=True)
    area_fig.update_traces(
        hovertemplate="date: %{x} <br>value: %{y:,.2f}$",
    )

    pie_fig = px.pie(
        df.sum().to_frame().transpose(),
        names=df.columns,
        values=df.sum(),
        color=df.columns,
        color_discrete_map=COLOR_MAP,
        opacity=0.7,
        hole=0.6,
    )
    pie_fig.update_layout(transition_duration=1000)
    pie_fig.update_traces(
        hovertemplate="Total: %{value:,.2f}$",
        textinfo="percent+label",
        textfont_size=20,
        marker=dict(line=dict(color="#FFFFFF", width=3)),
    )

    return area_fig, pie_fig


@app.callback(
    Output("df-table", "data"),
    Input("credit-memory", "data"),
)
def update_table(data):
    df = pd.DataFrame.from_dict(data)
    df.index = pd.DatetimeIndex(df.index)
    df["total"] = df.sum(axis=1)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)
    df["date"] = df["date"].dt.strftime("%b %Y")

    return df.to_dict(orient="records")


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
    cc = CreditCalculator()
    trigger = dash.callback_context.triggered[0]["prop_id"]
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
        credit = get_new_credit(loan_type, loan, years, interest_rate)
        cc.new_credit(credit)
    else:
        cc.reset_credit()
    if trigger in ["monthly-overpayment-input.value", "overpay-behavior-radio.value"]:
        add_monthly_overpayment(cc, monthly_overpay_amount, overpay_type)
    if trigger == "add-overpayment-button.n_clicks":
        add_single_overpayment(
            cc, single_overpay_month, single_overpay_amount, overpay_type
        )

    cc.calculate()

    cc.credit_df.reset_index(inplace=True)
    cc.credit_df["date"] = cc.credit_df["date"].apply(str)
    cc.credit_df.set_index("date", inplace=True)

    return cc.credit_df.to_dict()


def get_new_credit(loan_type, loan, years, interest_rate):
    if loan_type == "fixed":
        return FixedCredit(loan, years * 12, interest_rate / 100)
    if loan_type == "declining":
        return DecliningCredit(loan, years * 12, interest_rate / 100)


def add_monthly_overpayment(calculator, amount, overpay_type):
    for i in range(calculator.credit.n_installments):
        calculator.add_overpayment({i: amount}, overpay_type)


def add_single_overpayment(calculator, month, amount, overpay_type):
    if month is not None:
        calculator.add_overpayment({month: amount}, overpay_type)


@app.callback(
    Output("overpay-dates-dropdown", "options"),
    Output("overpay-dates-dropdown", "value"),
    Input("credit-memory", "data"),
    State("overpay-dates-dropdown", "value"),
)
def fill_in_dropdown_with_dates(data, dropdown_value):
    df = pd.DataFrame.from_dict(data)
    df.index = pd.DatetimeIndex(df.index)
    options = [{"label": f"{date:%b %Y}", "value": i} for i, date in enumerate(df.index)]

    if dropdown_value is None:
        return options, options[0]["value"]
    return options, dropdown_value
