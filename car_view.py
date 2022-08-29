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
    # dbc.Row([
    #     html.H1("Correlation and Regression")
    # ]),
    # dbc.Row([
    #     html.P(children=[
    #         "When analysing data, sometimes we want to explore whether the value of one variable depends on another. This allows us to draw a conclusion about whether two variables are associated, and can also allow us to make predictions about future values. ",
    #         html.Span("Correlation", className="bold-p"),
    #         " measures the level of agreement between two variables. ",
    #         html.Span("Regression", className="bold-p"),
    #         " provides a linear formula for that relationship. The higher the correlation, the closer the observed data points will lie to the ",
    #         html.Span("regression line", className="bold-p"),
    #         "."
    #     ], style={"margin-bottom": 10}),
    #     html.P(children=[
    #         "Using the dropdown lists below, explore the correlation between different quantitative variables from the Happy data set. Are there any variables that are particularly strongly associated with each other?"
    #     ], style={"margin-bottom": 10})
    # ]),
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
        ], xs=12, sm=12, md=12, lg=3, xl=3),
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
        ], xs=12, sm=12, md=12, lg=5, xl=5),
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
        ], xs=12, sm=12, md=12, lg=4, xl=4)
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
        ], xs=12, sm=12, md=12, lg=6, xl=6),
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
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ])
], fluid=True)

