import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable, FormatTemplate


NAVBAR_STYLE = {"font-size": "40px"}

navbar = dbc.NavbarSimple(
    brand="Mortgage Calculator",
    brand_href="#",
    brand_style=NAVBAR_STYLE,
    color="#004d40",
    dark=True,
    sticky="top",
)

basic_tab = dcc.Tab(
    label="Basic",
    value="tab-basic",
    children=[
        html.P(children="Credit type", className="lead", id="credit-type-text"),
        dcc.RadioItems(
            id="loan-type-radio",
            options=[
                {"label": " fixed installment", "value": "fixed"},
                {"label": " declining installment", "value": "declining"},
            ],
            value="fixed",
        ),
        html.Hr(),
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
        dcc.Slider(
            id="interest-rate-slider",
            min=0.1,
            max=20,
            step=0.1,
            value=5,
            marks={x: f"{x}%" for x in [0.1, 5, 10, 15, 20]},
        ),
    ],
    className="tab",
)

advanced_tab = dcc.Tab(
    label="Advanced",
    value="tab-advanced",
    children=[
        html.P(children="Overpayments", className="lead", id="overpayments-text"),
        dcc.RadioItems(
            id="overpay-behavior-radio",
            options=[
                {"label": " decrease loan term", "value": "decrease_loan_term"},
                {"label": " decrease installment", "value": "decrease_installment"},
            ],
            value="decrease_loan_term",
        ),
        html.Hr(),
        html.Div(
            className="lead",
            style={"display": "flex"},
            children=[
                html.P(children="Pay extra", className="lead"),
                dcc.Input(
                    id="monthly-overpayment-input",
                    type="number",
                    min=0,
                    max=1_000_000,
                    step=1,
                    value=0,
                    debounce=True,
                ),
                html.P(
                    children="$ monthly", className="lead", style={"margin-left": "5px"}
                ),
            ],
        ),
        html.Hr(),
        html.Div(
            className="row",
            style={"display": "flex", "margin-left": "1rem"},
            children=[
                html.P(
                    children="Single overpayment",
                    className="lead",
                    style={"margin-left": "0px"},
                ),
                dcc.Input(
                    id="single-overpayment-input",
                    type="number",
                    min=0,
                    max=1_000_000,
                    step=1,
                    value=0,
                    debounce=True,
                ),
                html.P(children="$", className="lead", style={"margin-left": "5px"}),
            ],
        ),
        html.Div(
            className="row",
            style={"display": "flex", "margin-left": "1rem"},
            children=[
                dcc.Dropdown(id="overpay-dates-dropdown", style={"width": "120px"}),
                html.Button("Add", id="add-overpayment-button", n_clicks=0),
            ],
        ),
    ],
)

sidebar = html.Div(
    [
        dcc.Tabs(
            id="settings-tabs",
            value="tab-basic",
            children=[
                basic_tab,
                advanced_tab,
            ],
            className="tabs",
        ),
    ],
    className="sidebar",
)


content = html.Div(
    [
        dcc.Store(id="credit-memory"),
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="pie-chart"),
        DataTable(
            id="df-table",
            columns=[
                {
                    "name": col,
                    "id": col,
                    "type": "numeric",
                    "format": FormatTemplate.money(2),
                }
                for col in ["principal", "interest", "overpayment", "total"]
            ],
        ),
    ],
    className="content",
)


def get_layout():
    layout = html.Div(
        children=[
            navbar,
            sidebar,
            content,
        ],
    )

    return layout
