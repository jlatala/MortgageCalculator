import plotly.express as px
from dash.dependencies import Input, Output, State
from credit_calculator.web.app import app
from credit_calculator.src.credit_calculator import CreditCalculator
from credit_calculator.src.fixed_credit import FixedCredit


cc = CreditCalculator()


@app.callback(
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Input("submit-button", "n_clicks"),
    State("loan", "value"),
    State("years", "value"),
    State("interest_rate", "value"),
)
def callback_a(n_clicks, loan, years, interest_rate):
    credit = FixedCredit(loan, years * 12, interest_rate)
    cc.new_credit(credit)
    cc.add_overpayment({36 + i: 1000 for i in range(24)})
    cc.add_overpayment({100 + i: 1500 for i in range(12)})
    cc.calculate()
    df = cc.credit_df
    bar_fig = px.bar(df, barmode="group")
    bar_fig.update_layout(transition_duration=500)

    pie_fig = px.pie(df.sum(), values=0)
    pie_fig.update_layout(transition_duration=1000)

    return bar_fig, pie_fig