import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dash_table import DataTable, FormatTemplate


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
    value="basic-tab",
    children=[
        html.P(children="Installment type", className="lead", id="credit-type-text"),
        dcc.RadioItems(
            id="loan-type-radio",
            labelClassName="label-loan-type-radio",
            options=[
                {"label": "fixed", "value": "fixed"},
                {"label": "declining", "value": "declining"},
            ],
            value="fixed",
        ),
        html.Hr(),
        html.P(id="loan-text", className="lead", style={"margin-left": "1rem"}),
        dcc.Slider(
            id="loan-slider",
            min=50_000,
            max=1_500_000,
            step=50_000,
            value=300_000,
            marks={50_000: "50k", 500_000: "500k", 1_000_000: "1M", 1_500_000: "1.5M"},
        ),
        html.Hr(),
        html.P(id="loan-term-text", className="lead", style={"margin-left": "1rem"}),
        dcc.Slider(
            id="loan-term-slider",
            min=1,
            max=40,
            step=1,
            value=20,
            marks={x: str(x) for x in [1, 10, 20, 30, 40]},
        ),
        html.Hr(),
        html.P(
            id="interest-rate-text", className="lead", style={"margin-left": "1rem"}
        ),
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
    value="advanced-tab",
    children=[
        html.P(
            children="Overpayments decrease", className="lead", id="overpayments-text"
        ),
        dcc.RadioItems(
            id="overpay-behavior-radio",
            options=[
                {"label": "loan term", "value": "decrease_loan_term"},
                {"label": "installment", "value": "decrease_installment"},
            ],
            value="decrease_loan_term",
        ),
        html.Hr(),
        html.Div(
            className="lead",
            style={"display": "flex", "margin-left": "1rem"},
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
            value="basic-tab",
            children=[
                basic_tab,
                advanced_tab,
            ],
            className="tabs",
        ),
    ],
    className="sidebar",
)


datatable_columns = [{"name": "date", "id": "date", "type": "text"}]
datatable_columns.extend(
    [
        {
            "name": col,
            "id": col,
            "type": "numeric",
            "format": FormatTemplate.money(2),
        }
        for col in ["principal", "interest", "overpayment", "total"]
    ]
)

summary_tab = dcc.Tab(
    label="Summary",
    value="summary-tab",
    children=[
        html.H2(
            id="summary-heading-text",
            # className="lead",
            # style={"margin-left": "0px"},
        ),
        html.P(
            id="summary-info-text",
            className="lead",
            style={"margin-left": "1.5rem"},
        ),
    ],
    className="tab",
)

chart_tab = dcc.Tab(
    label="Charts",
    value="chart-tab",
    children=[
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="pie-chart"),
    ],
    className="tab",
)

table_tab = dcc.Tab(
    label="Schedule",
    value="table-tab",
    children=[
        DataTable(
            id="df-table",
            columns=datatable_columns,
            # style_as_list_view=True,
        ),
    ],
    className="tab",
)

content = html.Div(
    [
        dcc.Tabs(
            id="content-tabs",
            value="summary-tab",
            children=[
                summary_tab,
                chart_tab,
                table_tab,
            ],
            className="tabs",
        ),
        dcc.Store(id="credit-memory"),
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
