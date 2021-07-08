import plotly.express as px
from dash.dependencies import Input, Output, State
from credit_calculator.web.app import app
from credit_calculator.src.credit_calculator import CreditCalculator
from credit_calculator.src.fixed_credit import FixedCredit


cc = CreditCalculator()


@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("df-table", "data"),
    Input("submit-button", "n_clicks"),
    Input("interest-rate", "n_submit"),
    State("loan-slider", "value"),
    State("loan-term-slider", "value"),
    State("interest-rate", "value"),
)
def update_figures(n_clicks, n_submit, loan, years, interest_rate):

    credit = FixedCredit(loan, years * 12, interest_rate / 100)
    cc.new_credit(credit)
    # cc.add_overpayment({36 + i: 1000 for i in range(24)})
    # cc.add_overpayment({100 + i: 1500 for i in range(12)})
    cc.calculate()

    df = cc.credit_df

    bar_fig = px.bar(df, barmode="group")
    bar_fig.update_layout(transition_duration=500)

    pie_fig = px.pie(df.sum(), values=0)
    pie_fig.update_layout(transition_duration=1000)

    df["total"] = df.sum(axis=1)

    return bar_fig, pie_fig, df.to_dict(orient="records")


@app.callback(
    Output("loan-text", "children"),
    Input("loan-slider", "value"),
)
def update_loan_amount(loan):
    return f"Loan amount {loan:,}$"


@app.callback(
    Output("loan-term-text", "children"),
    Input("loan-term-slider", "value"),
)
def update_loan_length(years):
    if years == 1:
        return f"{years} year"
    return f"{years} years"
