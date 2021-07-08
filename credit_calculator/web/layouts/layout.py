import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable, FormatTemplate

NAVBAR_STYLE = {"font-size": "40px"}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 70,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

navbar = dbc.NavbarSimple(
    brand="Mortgage Calculator",
    brand_href="#",
    brand_style=NAVBAR_STYLE,
    color="primary",
    dark=True,
    sticky="top",
)

sidebar = html.Div(
    [
        html.P(id="loan-text", className="lead"),
        dcc.Slider(
            id="loan-slider",
            min=50_000,
            max=1_500_000,
            step=50_000,
            value=300_000,
            marks={50_000: "50k", 500_000: "500k", 1_000_000: "1M", 1_500_000: "1.5M"},
        ),
        html.Hr(),
        html.P(id="loan-term-text", className="lead"),
        dcc.Slider(
            id="loan-term-slider",
            min=1,
            max=40,
            step=1,
            value=20,
            marks={x: str(x) for x in [1, 10, 20, 30, 40]},
        ),
        html.Hr(),
        html.P(id="interest-rate-text", className="lead"),
        dcc.Input(
            id="interest-rate",
            type="number",
            min=0,
            max=100,
            step=0.01,
            value=5,
            placeholder="interest rate",
        ),
        html.Hr(),
        html.Button(id="submit-button", n_clicks=0, children="Submit"),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

money_format = FormatTemplate.money(2)

content.children = [
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="pie-chart"),
    DataTable(
        id="df-table",
        columns=[
            {"name": col, "id": col, "type": "numeric", "format": money_format}
            for col in ["principal", "interest", "overpayment", "total"]
        ],
    ),
]


def get_layout():
    layout = html.Div(
        children=[
            navbar,
            sidebar,
            content,
        ],
    )

    return layout
