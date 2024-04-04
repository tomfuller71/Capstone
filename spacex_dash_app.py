# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("csv_data/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create list of dictionary for site names
sites = [{"label": site, "value": site } for site in spacex_df['Launch Site'].unique().tolist()]
sites = [{"label": "All sites", "value": "ALL"}] + sites

# Min and max payload values for slider defaults
min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df["Payload Mass (kg)"].max()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options= sites,
                                    value="ALL",
                                    placeholder="Select Lauch Site",
                                    searchable=True
                                    ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy()
    if entered_site == 'ALL':
        success_count_by_site = spacex_df.groupby(["Launch Site"]).sum().reset_index()
        success_count_by_site = success_count_by_site[["Launch Site", "class"]]

        fig = px.pie(
            success_count_by_site,
            values='class', 
            names='Launch Site', 
            title='Successful launches by Site'
        )
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_success = filtered_df[filtered_df['Launch Site'] == entered_site]["class"].mean()
        pie_data = pd.DataFrame({"Outcome": ["Success", "Failure"], "pc_rate": [site_success, 1 - site_success]})

        fig = px.pie(
            pie_data,
            values="pc_rate",
            names="Outcome",
            title="Launch Outcome by Site")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, selected_range):
    min_range, max_range = selected_range
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_range, max_range)]
    print(entered_site)
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    return px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category'
    )
    

# Run the app
if __name__ == '__main__':
    # Port for the app
    port = 8050
    # Run on local server
    app.run_server(port=port, debug=True)


# Which site has the largest number of successful launches?
# CCAFS SLC 40
    
# Which site has the highest launch success rate?
# KSC LC 39A
    
# Which payload range(s) has the highest success rate?
# 0-1000 kg
    
# Which payload range(s) has the lowest success rate?
# 6000-7000 kg

# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest success rate?
# FT