import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import json

# Load Excel data into DataFrames
file_path = 'March Job Fair.xlsx'
file_path1 = 'September Job Fair.xlsx'

df = pd.read_excel(file_path)
df1 = pd.read_excel(file_path1)

# Counting male and female applicants in df
df_gender_count = df['Gender'].value_counts()
df1_gender_count = df1['Gender'].value_counts()

# Data for df and df1
df_data = [df.loc[0, 'total company'], df.loc[0, 'Total job']]
df1_data = [df1.loc[0, 'total company'], df1.loc[0, 'Total job']]
# Define the age ranges and colors
bins = [15, 20, 25, 30, 35, 40, 45]
labels = ['15-20', '21-25', '26-30', '31-35', '36-40', '41-45']
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#C71585']
bins1 = [15, 20, 25, 30, 35, 40, 45]
labels1 = ['15-20', '21-25', '26-30', '31-35', '36-40', '41-45']
colors1 = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#C71585', '#FFD700']

# Categorize ages into ranges for df
df['Age Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
df_age_counts = df['Age Range'].value_counts()

# Create pie chart for df with consistent colors and legend
fig_df = go.Figure(data=[go.Pie(labels=df_age_counts.index, values=df_age_counts.values, name='Age Distribution in March', marker=dict(colors=colors))])
fig_df.update_layout(title='Age Distribution in March', showlegend=True)

# Categorize ages into ranges for df1 using the same labels and colors
df1['Age Range'] = pd.cut(df1['Age'], bins=bins1, labels=labels1, right=False)
df1_age_counts = df1['Age Range'].value_counts()

# Create pie chart for df1 with consistent colors and legend
fig_df1 = go.Figure(data=[go.Pie(labels=df1_age_counts.index, values=df1_age_counts.values, name='Age Distribution in September', marker=dict(colors=colors1))])
fig_df1.update_layout(title='Age Distribution in September', showlegend=True)



# Define the experience ranges and colors
exp_bins = [0, 1, 2, 3]
exp_labels = ['0', '1-2', '2-3']
exp_colors = ['#FF9999', '#66B2FF', '#99FF99']

# Categorize experience into ranges for df
df['EXP Range'] = pd.cut(df['EXP'], bins=exp_bins, labels=exp_labels, right=False)
df_exp_counts = df['EXP Range'].value_counts()

# Create pie chart for df with consistent colors and legend
fig_df_exp = go.Figure(data=[go.Pie(labels=df_exp_counts.index, values=df_exp_counts.values, name='Experience Distribution in March', marker=dict(colors=exp_colors))])
fig_df_exp.update_layout(title='Experience Distribution in March', showlegend=True)

# Categorize experience into ranges for df1 using the same labels and colors
df1['EXP Range'] = pd.cut(df1['EXP'], bins=exp_bins, labels=exp_labels, right=False)
df1_exp_counts = df1['EXP Range'].value_counts()

# Create pie chart for df1 with consistent colors and legend
fig_df1_exp = go.Figure(data=[go.Pie(labels=df1_exp_counts.index, values=df1_exp_counts.values, name='Experience Distribution in September', marker=dict(colors=exp_colors))])
fig_df1_exp.update_layout(title='Experience Distribution in September', showlegend=True)



# Concatenate df and df1
merged_df = pd.concat([df, df1])

# Group data by 'Gender' and 'EDULEVEL', count occurrences, and unstack to pivot the 'Gender' index
gender_edu_count = merged_df.groupby(['Gender', 'EDULEVEL']).size().unstack(fill_value=0)

# Create traces for Male and Female
male_trace = go.Bar(x=gender_edu_count.columns, y=gender_edu_count.loc['M'], name='Male')
female_trace = go.Bar(x=gender_edu_count.columns, y=gender_edu_count.loc['F'], name='Female')

# Create the figure
fig = go.Figure(data=[male_trace, female_trace])

# Add annotations for count labels
for trace in fig.data:
    for i, count in enumerate(trace.y):
        fig.add_annotation(
            x=trace.x[i],
            y=count,
            text=str(count),
            showarrow=False,
            font=dict(color='black', size=10),
            xanchor='left',
            yanchor='bottom',
            yshift=8  # Shift the annotation upward
        )

# Update layout
fig.update_layout(barmode='group', xaxis_title='Education Level', yaxis_title='Count', title='Application Count by Education Level and Gender March and September')
# Your data
data = {
    'Division': ['Barishal', 'Chittagong', 'Dhaka', 'Khulna', 'Mymensingh', 'Rajshahi', 'Rangpur', 'Sylhet'],
    'Total Users': [1521, 4354, 54936, 2644, 2036, 3935, 2869, 552]
}

# Load GeoJSON file
with open('bangladesh1.geojson', 'r') as f:
    geojson = json.load(f)

# Create the Scattermapbox plot
fig = go.Figure()

# Add scatter points for divisions with user values
fig.add_trace(go.Scattermapbox(
    lat=[23.5455, 22.3567, 23.8103, 22.8156, 24.7467, 24.3636, 25.7466, 24.8949],  # Latitude of divisions
    lon=[90.4035, 91.7832, 90.4125, 89.5645, 90.4060, 88.6241, 89.2486, 91.8687],  # Longitude of divisions
    mode='markers',
    marker=dict(
        size=[9, 15, 20, 11, 10, 12, 10, 8],  # Size of markers
        color=data['Total Users'],  # Color based on user values
        colorscale='Viridis',
        colorbar=dict(title='User Count'),
        opacity=0.8,
    ),
    text=[f"{division}<br>Total Users: {users}" for division, users in zip(data['Division'], data['Total Users'])],  # Hover text including division and total users
    hoverinfo='text'
))
fig.update_layout(
    height=600,  # Set the height to 600 pixels
    width=800,   # Set the width to 800 pixels
    title='Total Users by Division in Bangladesh',
    mapbox_style="carto-positron",
    mapbox_zoom=5,
    mapbox_center={"lat": 23.685, "lon": 90.3563},
    hovermode='closest'
)


# Calculating percentages
female_shortlist_percent_march = (df['Female Shortlist'][0] / df['Female apply'][0]) * 100 if df['Female apply'][0] > 0 else 0
male_shortlist_percent_march = (df['Male Shortlist'][0] / df['Male apply'][0]) * 100 if df['Male apply'][0] > 0 else 0
female_shortlist_percent_september = (df1['Female Shortlist'][0] / df1['Female apply'][0]) * 100 if df1['Female apply'][0] > 0 else 0
male_shortlist_percent_september = (df1['Male Shortlist'][0] / df1['Male apply'][0]) * 100 if df1['Male apply'][0] > 0 else 0

# Creating the grouped bar chart
fig_percentages = go.Figure()

fig_percentages.add_trace(go.Bar(
    x=['March Female', 'March Male', 'September Female', 'September Male'],
    y=[female_shortlist_percent_march, male_shortlist_percent_march, female_shortlist_percent_september, male_shortlist_percent_september],
    text=[f'{female_shortlist_percent_march:.2f}%', f'{male_shortlist_percent_march:.2f}%', f'{female_shortlist_percent_september:.2f}%', f'{male_shortlist_percent_september:.2f}%'],
    textposition='outside',
    marker_color=['#FF9999', '#66B2FF', '#FFCC99', '#C71585']
))

fig_percentages.update_layout(
    title='Percentage of Shortlisted Candidates by Gender in March and September',
    xaxis={'title': 'Category'},
    yaxis={'title': 'Percentage'},
)

 # Data for the bar chart
total_apply_march = df['TotalJobApply'][0]
shortlisted_march = df['TotalShortList'][0]
total_apply_september = df1['TotalJobApply'][0]
shortlisted_september = df1['TotalShortList'][0]

    # Creating the bar chart
fig_short = go.Figure()
fig_short.add_trace(go.Bar(
    x=['March Total Job Apply', 'March Total Shortlisted', 'September Total Job Apply', 'September Total Shortlisted'],
    y=[total_apply_march, shortlisted_march, total_apply_september, shortlisted_september],
    text=[total_apply_march, shortlisted_march, total_apply_september, shortlisted_september],
    textposition='outside',
    marker_color=['blue', 'orange', 'green', 'red']
))
fig_short.update_layout(
        title='Comparison of Total Job Applications and Shortlisted Candidates in March and September',
        xaxis={'title': 'Category'},
        yaxis={'title': 'Count'},
    )
# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# Define app layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H1("Freshers Job Fair Bangladesh", style={'text-align': 'center', 'margin-bottom': '20px'}),  # Added header for the job fair
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='gender-comparison',
                    figure={
                        'data': [
                            go.Bar(name='March Male', x=['Male'], y=[df_gender_count.get('M', 0)], text=[df_gender_count.get('M', 0)], textposition='outside'),
                            go.Bar(name='March Female', x=['Female'], y=[df_gender_count.get('F', 0)], text=[df_gender_count.get('F', 0)], textposition='outside'),
                            go.Bar(name='September Male', x=['Male'], y=[df1_gender_count.get('M', 0)], text=[df1_gender_count.get('M', 0)], textposition='outside'),
                            go.Bar(name='September Female', x=['Female'], y=[df1_gender_count.get('F', 0)], text=[df1_gender_count.get('F', 0)], textposition='outside')
                        ],
                        'layout': {
                            'title': 'Comparison of Male and Female Applicants in March and September',
                            'barmode': 'group',
                            'xaxis': {'title': 'Gender'},
                            'yaxis': {'title': 'Count'},
                            'bargap': 0.1,  # Adjust the gap between bars
                            'height': 500,  # Adjust the height of the figure
                            'width': 800    # Adjust the width of the figure
                        }
                    }
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id='job-company-comparison',
                    figure={
                        'data': [
                            go.Bar(name='March Total Company', x=['March'], y=[df_data[0]], text=[df_data[0]], textposition='outside'),
                            go.Bar(name='March Total Job', x=['March'], y=[df_data[1]], text=[df_data[1]], textposition='outside'),
                            go.Bar(name='September Total Company ', x=['September'], y=[df1_data[0]], text=[df1_data[0]], textposition='outside'),
                            go.Bar(name='September Total Job', x=['September'], y=[df1_data[1]], text=[df1_data[1]], textposition='outside')
                        ],
                        'layout': {
                            'title': 'Comparison of Total Company and Total Job in March and September',
                            'barmode': 'group',
                            'xaxis': {'title': 'Dataset'},
                            'yaxis': {'title': 'Count'},
                            'height': 500,  # Adjust the height of the figure
                            'width': 800    # Adjust the width of the figure
                        }
                    }
                ),
                width=6
            ),
        ]),
            dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='age-distribution-march',
                    figure=fig_df  # This is the pie chart for March
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id='age-distribution-september',
                    figure=fig_df1  # This is the pie chart for September
                ),
                width=6
            ),
        ]),
      dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='experience-distribution-march',
                    figure=fig_df_exp  # This is the pie chart for March's experience distribution
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id='experience-distribution-september',
                    figure=fig_df1_exp  # This is the pie chart for September's experience distribution
                ),
                width=6
            ),
        ]),
         
        dbc.Row([
    dbc.Col(
        dcc.Graph(
            id='gender-comparison1',
            figure={
                'data': [
                    male_trace,
                    female_trace
                ],
                'layout': {
                    'title': 'Application Count by Education Level and Gender March and September',
                    'barmode': 'group',
                    'xaxis': {'title': 'Education Level'},
                    'yaxis': {'title': 'Count'},
                    'height': 500,
                    'width': 800
                }
            }
        ),
        width=6
    ),
    dbc.Col(
        dcc.Graph(
            id='scatter-map',
            figure=fig
        ),
        width=6
    )
]),
 dbc.Row([
            dbc.Col(
                dcc.Graph(id='total-job-shortlist',figure=fig_short
                          
                          ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id='shortlisted-gender-percentage',
                    figure=fig_percentages
                ),
                width=6
            ),
        ]),
    ]
)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)