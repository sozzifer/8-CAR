from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from car_model import car_happy

app = Dash(__name__,
           title="Correlation and Regression",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Independent variable (x axis)",
                          className="label",
                          html_for="dropdown-x"),
                dbc.Select(id="dropdown-x",
                           options=[{"label": x, "value": x}
                                    for x in car_happy.columns[0:7]],
                           value="Height")
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Label("Dependent variable (y axis)",
                          className="label",
                          html_for="dropdown-y"),
                dbc.Select(id="dropdown-y",
                           options=[{"label": x, "value": x}
                                    for x in car_happy.columns[0:7]],
                           value="Weight"),
                dbc.FormFeedback(
                    "Dependent variable must be different to independent variable",
                    type="invalid")
            ], **{"aria-live": "polite"}),
            html.Br()
        ], xs=12, lg=3),
        dbc.Col([
            html.H4("Results"),
            html.Div([
                html.P(children=[
                    html.Span("Correlation coefficient (r): ", className="bold-p"),
                    html.Span(id="pearson")
                ]),
                html.P(children=[
                    html.Span("R-squared value: ", className="bold-p"),
                    html.Span(id="r-squared")
                ]),
                html.Br(),
                html.P("Regression equation: ", className="bold-p"),
                html.P(id="reg-eq"),
                html.Br()
            ], **{"aria-live": "polite"})
        ], xs=12, lg=5),
        dbc.Col([
            html.H4("Prediction"),
            html.P(id="prediction"),
            dcc.Store(id="correct-result"),
            html.Br(),
            dbc.Input(id="answer",
                      type="number",
                      placeholder="Enter answer to 2dp"),
            html.Div([
                dbc.Button(id="submit",
                           n_clicks=0,
                           children="Check answer",
                           class_name="button",
                           style={"width": "40%"}),
                html.P(id="feedback",
                       className="bold-p",
                       style={"width": "60%", "margin": "auto 0"},
                       **{"aria-live": "polite"})
            ], className="d-flex")
        ], xs=12, lg=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="xy-graph",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img"),
            html.Div(id="sr-xy",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, lg=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="fit-graph",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img"),
            html.Div(id="sr-fit",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, lg=6)
    ])
], fluid=True)

