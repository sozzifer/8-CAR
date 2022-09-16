import math
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.graphics.gofplots import qqplot

# Generate dataframe from csv
car_happy = pd.read_csv("data/car_happy.csv")


# Filter dataframe so only non-null values returned
def not_null(x, y):
    df_not_null = car_happy[(car_happy[x].notnull()) & (car_happy[y].notnull())]
    return df_not_null


# Perform regression and generate residuals/fitted values
def regression(x, y):
    formula = f"{y} ~ {x}"
    model = ols(formula, data=car_happy)
    results = model.fit()
    summary = results.summary()
    params = results.params
    residuals = results.resid
    fitted = results.fittedvalues
    r_sq = results.rsquared
    r = math.sqrt(r_sq)
    intercept = round(params[0], 2)
    slope = round(params[1], 2)
    return summary, residuals, fitted, r_sq, r, intercept, slope


# https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
# model = ols("Weight ~ Height", data=car_happy)
# results = model.fit()

# https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
# summary = results.summary()
# params = results.params
# residuals = results.resid
# fitted = results.fittedvalues
# r_sq = results.rsquared
# conf_int = results.conf_int(0.01)
# print(summary)

# Probability plot?
# qqplot_data = qqplot(residuals, line='s').gca().lines
# fig = go.Figure(go.Scatter(x=qqplot_data[0].get_xdata(),
#                            y=qqplot_data[0].get_ydata(),
#                            mode="markers"))
# fig.add_trace(go.Scatter(x=qqplot_data[1].get_xdata(),
#                          y=qqplot_data[1].get_ydata(),
#                          mode="lines"))
# fig.show()
