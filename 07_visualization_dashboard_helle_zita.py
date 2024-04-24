# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:\Zita\___Letoltesek\___melo\python\_capstone\spacex_launch_dash.csv")
spacex_df["class_label"] = spacex_df["class"].replace({0: "failure", 1: "success"})
min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df["Payload Mass (kg)"].max()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([html.H1("SpaceX Launch Records Dashboard",
                               style = {"textAlign": "center", "color": "#503D36", "font-size": 40}),

                      html.Br(),

                      dcc.Dropdown(id = "site-dropdown",
                                   options = [{"label": "All Sites", "value": "ALL"},
                                              {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                              {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                              {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                                              {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"}],
                                   value = "ALL",
                                   placeholder="Select a Launch Site",
                                   searchable = True),

                      html.Br(),

                      # TASK 2: Add a pie chart to show the total successful launches count for all sites
                      # If a specific launch site was selected, show the Success vs. Failed counts for the site
                      html.Div(dcc.Graph(id = "success-pie-chart")),

                      html.Br(),

                      html.P("Payload range (Kg):"),
                      # TASK 3: Add a slider to select payload range

                      dcc.RangeSlider(id = "payload-slider", min = 0, max = 10000, step = 1000,
                                      value = [min_payload, max_payload]),

                      html.Br(),

                      # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                      html.Div(dcc.Graph(id="success-payload-scatter-chart")),
                      ])

# TASK 2:

@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        figure = px.pie(spacex_df, values = 'class', names = 'Launch Site', title = 'Total Success Launches by Site')
        return figure
    else:
        spacex_df_site = spacex_df[spacex_df["Launch Site"] == entered_site].copy()
        figure = px.pie(spacex_df_site, values = spacex_df_site.value_counts().values, names = 'class_label', title = 'Total Launches for Site {}'.format(entered_site))
        return figure

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value'),
     Input(component_id = 'payload-slider', component_property = 'value')])

def get_scatter_chart(entered_site, entered_payload):
    if entered_site == 'ALL':
        spacex_df_payload = spacex_df[spacex_df["Payload Mass (kg)"].between(entered_payload[0], entered_payload[1])].copy()
        figure = px.scatter(spacex_df_payload, x = 'Payload Mass (kg)', y = 'class', color = "Booster Version Category", title = 'Correlation between Payload and Success for all Sites')
        return figure
    else:
        spacex_df_site_payload = spacex_df[(spacex_df["Launch Site"] == entered_site) & (spacex_df["Payload Mass (kg)"].between(entered_payload[0], entered_payload[1]))].copy()
        figure = px.scatter(spacex_df_site_payload, x = 'Payload Mass (kg)', y = 'class', color = "Booster Version Category", title = 'Correlation between Payload and Success for Site {}'.format(entered_site))
        return figure
    

# Run the app
if __name__ == "__main__":
    app.run_server()