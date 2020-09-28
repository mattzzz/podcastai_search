
import pandas as pd
import dash
# import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import os
import plotly.graph_objs as go


podcast_data = {
    'JRE804' : [
        'https://www.youtube.com/watch?v=RJ5_hAEsLkU',
        'https://podscribe.app/feeds/http-joeroganexpjoeroganlibsynprocom-rss/episodes/d5987a72c245f7cce405a504b63dd3be'
    ],
    'JRE1169' : [
        'https://www.youtube.com/watch?v=ycPr5-27vSI',
        'https://podscribe.app/feeds/http-joeroganexpjoeroganlibsynprocom-rss/episodes/964caf3227b64117b20a82a574742edf'
    ]
}

podcast_choices = {
    'JOE ROGAN EXPERIENCE #804 WITH SAM HARRIS' : 'JRE804',
    'JOE ROGAN EXPERIENCE #1169 WITH ELON MUSK' : 'JRE1169',
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, url_base_pathname='/podcastai/', external_stylesheets=external_stylesheets)#[dbc.themes.BOOTSTRAP])
app.title = 'PodcastAI Search'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'textAlign': 'center',
}



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # html.Img(src=app.get_asset_url('banner-desktop.png')),
    html.Div([dcc.Dropdown(id='podcast-select', 
                            options=[{'label': k, 'value': v} for k,v in podcast_choices.items()],
                            value='JRE1169', 
                            style={'width': '100%',
                            'fontSize' : 24,
                            })
    ]),
    html.Div([
        dcc.Input(
            id = 'term1',
            placeholder='Input goes here...',
            type='Search Term 1',
            value='', debounce=True),
        dcc.Input(
            id = 'term2',
            placeholder='Input goes here...',
            type='Search Term 2',
            value='', debounce=True),
        dcc.Input(
            id = 'term3',
            placeholder='Input goes here...',
            type='Search Term 3',
            value='', debounce=True),
    ]),

    html.Div(id = 'youtube_link'),
    dcc.Graph(id='similarities-graph'),
    dcc.Graph(id='topic-areas-graph'),
], className="embed-responsive")

@app.callback(
    Output('youtube_link', 'children'),
    [Input('podcast-select', 'value')]
)
def update_youtube(podcast):
    print('update_youtube:', podcast)

    video_url = podcast_data[podcast][0]
    video_id = video_url.split('=')[1]
    # embed_url = "https://www.youtube.com/embed/RJ5_hAEsLkU?start=1287"
    embed_url = "https://www.youtube.com/embed/%s"%video_id

    return html.Iframe(src=embed_url, width=560, height=315)
    


@app.callback(
    [Output('similarities-graph', 'figure'),
    Output('topic-areas-graph', 'figure')],
    [Input('term1', 'value'),
    Input('term2', 'value'),
    Input('term3', 'value')],
)

def update_graph(token1, token2, token3):
    print('update_graph:', token1, token2, token3)
    
    fig_data = []
    if token1:
        df = pd.read_csv('first.csv')
        y = df['prob'].rolling(10).mean()
        fig_data.append({'x': df['time'], 'y': y, 'name': token1})
    if token2:
        df = pd.read_csv('second.csv')
        y = df['prob'].rolling(10).mean()
        fig_data.append({'x': df['time'], 'y': y, 'name': token2})
    if token3:
        df = pd.read_csv('third.csv')
        fig_data.append({'x': df['time'], 'y': df['prob'], 'name': token3})

    # fig = go.Figure(data=[go.Scatter(x=df['time'], y=df['prob'])])
    fig = go.Figure(data=fig_data, layout={'title': 'Similarities'})
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig2 = go.Figure(data=[], layout={'title': 'Topic Areas'})
    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return fig, fig2
    

if __name__ == '__main__':
    app.run_server(debug=False)#, port=8888)


    
