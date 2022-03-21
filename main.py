# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
from builders import make_table


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css", 
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = Dash(__name__, external_stylesheets = stylesheets)

server = app.server

bubble_map = px.scatter_geo(
    countries_df, 
    title="Confirmed Cases by Country",
    size = "Confirmed",
    size_max = 40,
    template = "plotly_dark",
    color_continuous_scale = px.colors.sequential.Oryel,
    locations = "Country_Region", 
    locationmode = "country names", 
    color="Confirmed", 
    hover_name = "Country_Region", 
    projection = "natural earth",
    hover_data={
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
        "Country_Region":False
    },

)
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))

bars_graph = px.bar(
    totals_df, 
    x="condition", 
    hover_data={'count':":,"},
    y="count", 
    template = "plotly_dark", 
    title="Total Global Cases",
    labels = {
        "condition":"Condition",
        "count":"Count",
        "color":"Condition"
    }
)

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={ 
        "minHeight":"100vh", 
        "backgroundColor":"#111111", 
        "color":"white",
        "fontFamily":"Open Sans, sans-serif",
        "maxWidth": "100vw"
    },
    children = [
        html.Header(
            style={"textAlign":"center", "paddingTop":"3vh"}, 
            children=[html.H1("Corona Dashboard", style={"fontSize":40})]
        ),
        html.Div(
            style={"display":"grid", "gridTemplateColumns":"repeat(4, 1fr)", "gap":"1vw"},
            children = [
                html.Div(style = {"grid-column": "span 3"}, children=[dcc.Graph(figure=bubble_map)]),
                html.Div(children=[make_table(countries_df)])
            ]
        ),
        html.Div(
            style={"display":"grid", "gridTemplateColumns":"repeat(5, 1fr)", "gap":"1vw", "marginTop":"1vh"},
            children = [
                html.Div(
                    style={"grid-column":"span 2"}, 
                    children=[dcc.Graph(figure=bars_graph)]),
                    html.Div(
                        style = {"grid-column":"span 3"},
                        children=[
                            dcc.Dropdown(
                                style = {"margin":"0 auto", "color":"#111111"},
                                id="country",
                                options=[
                                {"label":country, "value":country} 
                                for country in dropdown_options
                            ]),
                            dcc.Graph(id="country_graph"),
                        ]
                    )
            ]
        )
    ],
)

@app.callback(
    Output("country_graph", "figure"),
    [
        Input("country", "value")
    ]
)

def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

    fig = px.line(df, x="date", y=["confirmed", "deaths", "recovered"], 
              labels = {"value":"Cases", "variable":"Condition", "date":"Date"},
             hover_data = {"value":":,", "variable":None, "date":False},
             template = "plotly_dark",
             color_discrete_map = {
                 "confirmed":"#e74c3c",
                 "deaths":"#8e44ad",
                 "recovered":"#27ae60"
             })
    fig.update_xaxes(rangeslider_visible = True)
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
