import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
import pycountry

df_c = pd.read_csv('output_data/20230805_SIGCOMM_country',index_col=0)
df_c['country_iso'] = df_c['country'].apply(lambda x: pycountry.countries.lookup(x).alpha_3)


for i in ['Organizing','Program']:
    df_test = df_c[(df_c['committee']==i)]
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
    fig.update_layout(title_text = "SIGCOMM {} committee region distribution - year wise data".format(i))
    fig.show()

