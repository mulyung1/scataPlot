from dash import Dash, dcc, html, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px

#connect to the data
df=pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

#initialize the app
app=Dash(__name__)
server=app.server

markdownText='''
## QUESTION: Does the amount of electrical power consumed affect the energy output in an economy?

Are the two indicators correlated. i.e., does the occurence of one(x) influence the occurence of another(y)??


   >_Select the variable for X axis from the LHS input panels_


   >_Select the variable for Y axis from the RHS input panels_
'''
#define the app layout
app.layout=html.Div([
    html.Div([
        html.Div([
            html.H1('Does X affect Y?'),
            html.Hr(),
            dcc.Markdown(children=markdownText)
        ]),
        html.Br(),
        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),
                'Electric power consumption (kWh per capita)',
                id='drpdwn1'),
            dcc.RadioItems(
                ['Linear','Log'],
                'Log',
                id='baton1',
                inline=True)
        ], style={'width':'48%','display':'inline-Block'}),
        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),
                'Energy use (kg of oil equivalent per capita)',
                id='drpdwn2'),
            dcc.RadioItems(
                ['Linear','Log'],
                'Log',
                id='baton2',
                inline=True)
        ], style={'width':'48%','float':'right','display':'inline-Block'})
    ]),
    html.Br(),
    html.Div([
        dcc.Graph(id='graf'),
        dcc.Slider(
            df['Year'].min(),
            df['Year'].max(),
            step=None,
            #value=df['Year'].min(),
            value=1977,
            marks={str(Year):str(Year) for Year in df['Year'].unique()},
            id='slida')
    ]),
    html.Br(),
    html.Hr(),
    html.Div([
        html.H2('Data Used'),
        dash_table.DataTable(data=df.to_dict('records'),page_size=10, style_table={'overflowX':'auto'})
    ])
])

#callback decorator to connect between the data(input) and the figure(output)
@callback(
    Output('graf','figure'),
    Input('drpdwn1','value'),
    Input('drpdwn2','value'),
    Input('baton1','value'),
    Input('baton2','value'),
    Input('slida','value')
)

#callback function-called everytime an input components property changes
def updateApp(independentVar, dependentVar, type_x, type_y, time):

    dff=df[df['Year']==time]
    fig=px.scatter(
        x=dff[dff['Indicator Name']==independentVar]['Value'],
        y=dff[dff['Indicator Name']==dependentVar]['Value'],
        hover_name=dff[dff['Indicator Name']==dependentVar]['Country Name'])
    fig.update_layout(margin={'l':40,'b':40,'t':10,'r':0}, hovermode='closest')
    fig.update_xaxes(
        title=independentVar,
        type='log' if type_x== 'Log' else 'linear')
    fig.update_yaxes(
        title=dependentVar, 
        type='log' if type_y=='Log' else 'linear')
    return fig

#run the app
if __name__ == '__main__':
    app.run(debug=True)
