from dash import Input, Output, State, exceptions, no_update, callback_context as ctx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
from car_view import app
from car_model import not_null, regression


@app.callback(
    Output("xy-graph", "figure"),
    Output("dropdown-y", "invalid"),
    Input("dropdown-x", "value"),
    Input("dropdown-y", "value")
)
def plot_x_y(x, y):
    if x == y:
        return no_update, True
    else:
        df = not_null(x, y)
        fig = px.scatter(df,
                         x=f"{x}",
                         y=f"{y}",
                         trendline="ols",
                         trendline_color_override="#d10373")
        fig.update_traces(marker_color="#9eab05",
                          marker_size=4,
                          line_width=3)
        fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                          height=300,
                          font_size=14,
                          dragmode=False,
                          xaxis_title=x,
                          yaxis_title=y)
        return fig, False


@app.callback(
    Output("fit-graph", "figure"),
    Output("pearson", "children"),
    Output("reg-eq", "children"),
    Output("r-squared", "children"),
    Output("sr-xy", "children"),
    Output("sr-fit", "children"),
    Input("dropdown-x", "value"),
    Input("dropdown-y", "value")
)
def plot_res_v_fitted(x, y):
    if x == y:
        return no_update, no_update, no_update, no_update, no_update, no_update
    else:
        _, params, residuals, fitted, r_sq, r = regression(x, y)
        fig = go.Figure(
            go.Scatter(x=fitted,
                       y=residuals,
                       marker_color="#9eab05",
                       marker_size=4,
                       mode="markers",
                       hoverinfo="skip",
                       showlegend=False))
        fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                          height=300,
                          font_size=14,
                          dragmode=False,
                          xaxis_title="Fitted values",
                          yaxis_title="Residuals")
        zero_line = np.linspace(np.min(fitted), np.max(fitted), 100)
        fig.add_trace(go.Scatter(x=zero_line,
                                 y=[0]*100,
                                 line_width=3,
                                 marker_color="#d10373",
                                 hoverinfo="skip",
                                 showlegend=False))
        intercept = round(params[0], 2)
        slope = round(params[1], 2)
        if intercept < 0:
            equation = f"{y} = {slope} \u00D7 {x} - {abs(intercept)}"
        else:
            equation = f"{y} = {slope} \u00D7 {x} + {intercept}"
        sr_xy = f"Graph of {y} versus {x} with regression line {equation}"
        sr_fit = f"Graph of residuals versus fitted values for {y} versus {x}"
        return fig, f"{r:.3f}", equation, f"{r_sq:.3f}", sr_xy, sr_fit


@app.callback(
    Output("prediction", "children"),
    Output("correct-result", "data"),
    Output("answer", "value"),
    Input("dropdown-x", "value"),
    Input("dropdown-y", "value")
)
def generate_prediction(x, y):
    df = not_null(x, y)
    _, params, _, _, _, _ = regression(x, y)
    num = round(random.uniform(min(df[x]), max(df[x])), 1)
    intercept = round(params[0], 2)
    slope = round(params[1], 2)
    result = round((slope*num) + intercept, 2)
    return f"Use the regression equation to predict the {y} of a student whose {x} is {num}", result, None


@app.callback(
    Output("feedback", "children"),
    Input("submit", "n_clicks"),
    Input("dropdown-x", "value"),
    Input("dropdown-y", "value"),
    State("answer", "value"),
    State("correct-result", "data"),
    prevent_initial_call=True
)
def check_answer(n_clicks, x, y, answer, result):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        trigger = ctx.triggered_id
        if trigger == "submit":
            if answer == result:
                return "Correct"
            else:
                return f"Incorrect - the correct answer is {result}"
        elif trigger == "dropdown-x" or trigger == "dropdown-y":
            return ""


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    # app.run(debug=True)
