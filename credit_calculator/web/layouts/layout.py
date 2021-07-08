import dash_core_components as dcc
import dash_html_components as html


def get_layout():
    layout = html.Div(
        children=[
            html.H1(children="Mortgage Calculator", style={"textAlign": "center"}),
            html.Div(
                children="Web Aplication - Mortgage Calculator",
                style={"textAlign": "center"},
            ),
            dcc.Input(id="loan", type="number", value=300_000),
            dcc.Input(id="years", type="number", value=20),
            dcc.Input(id="interest_rate", type="number", value=0.05),
            html.Button(id="submit-button", n_clicks=0, children="Submit"),
            dcc.Graph(id="bar-chart"),
            dcc.Graph(id="pie-chart"),
        ],
    )

    return layout
