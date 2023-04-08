# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')        # warning 뜨는 것은 보이지 않도록 한다. 

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()
launch_sites_list = [{"label":site, "value": site} for site in launch_sites]
drop_options = [{'label': 'All Sites', 'value': 'ALL'}]
drop_options.extend(launch_sites_list)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options= drop_options,
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),
                               
                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                marks={0: '0',
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        data = filtered_df['Launch Site'].value_counts()
        fig = px.pie(data, values=data.values, 
        names=data.keys(), 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        data = filtered_df['class'].value_counts()
        fig = px.pie(data, values=data.values, 
        names=data.keys(), 
        title="Total success launches for site {}".format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
                
def get_sccess_payload_scatter(site_dropdown, slider_range):
    low, high = slider_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']<=high)&((spacex_df['Payload Mass (kg)']>=low))]
    if site_dropdown=='ALL':
        fig = px.scatter(filtered_df,
                        x='Payload Mass (kg)',
                        y='class',
                        color="Booster Version Category",
                        title="Correlation between Payload and Success for all sites.")
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == site_dropdown]
        fig = px.scatter(filtered_df,
                        x='Payload Mass (kg)',
                        y='class',
                        color="Booster Version Category",
                        title="Correlation between Payload and Success for {}.".format(site_dropdown))
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()