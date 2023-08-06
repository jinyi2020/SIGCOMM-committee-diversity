import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
import pycountry

from dash import Dash, dcc, html, Input, Output

df_c = pd.read_csv('output_data/20230805_SIGCOMM_country',index_col=0)
df_c['country_iso'] = df_c['country'].apply(lambda x: pycountry.countries.lookup(x).alpha_3)


app = Dash(__name__)


app.layout = html.Div([
    html.H4('SIGCOMM committee members region distribution - year wise data'),
    html.P("Select committee:"),
    dcc.RadioItems(
        id='candidate', 
        options=["Organizing", "Program"],
        value="Organizing",
        inline=True
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))




def display_choropleth(candidate):
    df_test = df_c[(df_c['committee']==candidate)]
    df_test_count = df_test.groupby(['year','country_iso','country'])['country_iso'].count()
    df_test_count = df_test_count.to_frame().rename(columns={'country_iso': 'count'})
    df_test_count = df_test_count.reset_index()
    df_test_count.sort_values('year', ascending=True, inplace=True)

    fig = px.choropleth(df_test_count, locations="country_iso",
                        locationmode='ISO-3',
                        color='count',
                        hover_name="country",
                        color_continuous_scale=px.colors.sequential.Rainbow,
                        animation_frame="year")
    #fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
    #fig.show()

app.run_server(debug=True)
