import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/M3d0u/dataForCollab/main/IMDb_DataFrame_Final.csv')

columns_to_display = ['title', 'year', 'genre', 'country', 'avg_vote']

ds ='https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css'

app = dash.Dash(__name__,external_stylesheets=[ds])

server = app.server

#------------------Algo reco------------------

def get_important_data(data):
    important_features=[]
    for i in range(0, data.shape[0]):
        important_features.append(data['genre'].iloc[i]+ ' '+
                                 data['country'].iloc[i]+ ' '+
                                 data['director'].iloc[i]+ ' '+
                                 data['writer'].iloc[i]+ ' '+
                                 data['actors'].iloc[i]+ ' '+
                                 data['description'].iloc[i])
    return important_features

#Création de la colonne contenat les string combinés
df['combined_features']=get_important_data(df)

#Convertir le text en matrice de "token counts"
cm = CountVectorizer().fit_transform(df['combined_features'])

#-------------------Dash----------------------

app.layout = html.Div([
    html.H1(["#BetterThanNetflix"], style = {"textAlign":"center", 'color': 'red', 'marginTop': 25, 'marginBottom': 25}),
    html.H2("Select movies within our database:", style = {'marginTop': 25, 'marginBottom': 25}),
    html.P(['Custom the year range/interval :']),
    dcc.RangeSlider(
        id='year_slidebar',
        min=1913,
        max=2020,
        updatemode="mouseup",
        value=[1913, 2020],
        marks={
        1913:'1913',
        1950: '1950',
        1970:'1970',
        1980:'1980',
        1990:'1990',
        2000:'2000',
        2010:'2010',
        2020:'2020',    
        }
    ),
    html.Div(id='year_selected', style = {'marginTop': 25, 'marginBottom': 25}),
    html.P(['Choose your favorite genre(s):'], style = {'marginTop': 25, 'marginBottom': 25}),
    dcc.Dropdown(id="slct_genre",
                 options=[{"label":"All genres", "value":""},
                     {"label": "Action", "value": "Action"},
                     {"label": "Adventure", "value": "Adventure"},
                     {"label": "Animation", "value": "Animation"},
                     {"label": "Biography", "value": "Biography"},
                     {"label": "Comedy", "value": "Comedy"},
                     {"label": "Crime", "value": "Crime"},
                     {"label": "Documentary", "value": "Documentary"},
                     {"label": "Drama", "value": "Drama"},
                     {"label": "Family", "value": "Family"},
                     {"label": "Fantasy", "value": "Fantasy"},
                     {"label": "FilmNoir", "value": "FilmNoir"},
                     {"label": "History", "value": "History"},
                     {"label": "Horror", "value": "Horror"},
                     {"label": "Music", "value": "Music"},
                     {"label": "Musical", "value": "Musical"},
                     {"label": "Mystery", "value": "Mystery"},
                     {"label": "Romance", "value": "Romance"},
                     {"label": "Sci-Fi", "value": "Sci-Fi"},
                     {"label": "ShortFilm", "value": "ShortFilm"},
                     {"label": "Sport", "value": "Sport"},
                     {"label": "Superhero", "value": "Superhero"},
                     {"label": "Thriller", "value": "Thriller"},
                     {"label": "War", "value": "War"},
                     {"label": "Western", "value": "Western"}],
                 multi=True,
                 value = "",
                 style={'width': "40%"}
                 ),
    html.P(['Or even search by title for a specific film :'], style = {'marginTop': 25, 'marginBottom': 25}),
        dcc.Input(
            id='my-id',
            value='Type your movie',
            type='text'
    ),
    html.P(['Here is our movies corresponding to your criterias:'], style = {'marginTop': 25, 'marginBottom': 25}),
    dash_table.DataTable(
    id='movies_selection',
    columns= [{"name": i, "id": i} for i in columns_to_display],
    data=df.to_dict('records'),
        css=[{
        'selector': '.dash-spreadsheet td div',
        'rule': '''
            line-height: 15px;
            max-height: 30px; min-height: 30px; height: 30px;
            display: block;
            overflow-y: hidden;
        '''
    }],
    style_cell=
    {
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'textAlign': 'left',
        'whiteSpace': 'normal',
        'height': 'auto'
        
    },
    style_as_list_view=True, # STYLE DU DF SANS LES BORDURES
    style_header={ # Custom style du header uniquement
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'textAlign': 'left'
    },
      style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
    page_current=0,
    page_size=7,
    editable=True),
    html.H2("Use our advanced algorithm to get a movie recommendation:", style = {'marginTop': 25, 'marginBottom': 25}),
    html.P(['type the movie you want a recommendation from:']),
    dcc.Input(
            id='input_reco',
            type='text',
            value='Type your movie', 
            style = {'width' : 500}),
    html.Div(id='movie_reco', style={'marginTop': 25}),
    html.Div(id='movie_1'),
    html.Div(id='movie_2'),
    html.Div(id='movie_3')
], style = {"marginLeft": '10px'})

#callback années sélectionnées
@app.callback(dash.dependencies.Output('year_selected', 'children'),
              dash.dependencies.Input('year_slidebar', 'value'))

def update_sentence(yearChoosen):
    return 'You have selected the following years {}'.format(yearChoosen)

#Callback màj talbeau
@app.callback(dash.dependencies.Output('movies_selection', 'data'),
              [dash.dependencies.Input('year_slidebar', 'value'),
              dash.dependencies.Input('slct_genre', 'value'),
              dash.dependencies.Input('my-id', 'value')])

def update_table(yearChoosen,genreSelected,titleSelected):
    #Prise en compte du genre
    if len(genreSelected)==0:
        df_temp1 = df
    elif len(genreSelected)==1:
        df_temp1 = df[df['genre'].str.contains(genreSelected[0])]
    elif len(genreSelected)==2:
        df_temp1 = df[(df['genre'].str.contains(genreSelected[0]))&(df['genre'].str.contains(genreSelected[1]))]
    elif len(genreSelected)==3:
        df_temp1 = df[(df['genre'].str.contains(genreSelected[0]))&(df['genre'].str.contains(genreSelected[1]))&(df['genre'].str.contains(genreSelected[2]))]
     #Prise en compte des années   
    df_temp2 = df_temp1[((df_temp1['year']>=yearChoosen[0])&(df_temp1['year']<=yearChoosen[1]))]
    #Prise en compte input utilisateur
    if titleSelected=='Type your movie':
        df_temp3=df_temp2
    else:
        df_temp3 = df_temp2[df_temp2['title'].str.contains(titleSelected)]
        
    data = df_temp3.to_dict('rows')
    return data

#callback recommendation
@app.callback([dash.dependencies.Output('movie_reco', 'children'),
              dash.dependencies.Output('movie_1', 'children'),
              dash.dependencies.Output('movie_2', 'children'),
              dash.dependencies.Output('movie_3', 'children')],
              dash.dependencies.Input('input_reco', 'value'),
              )

def get_movie_reco(movie_input):
    if movie_input == None:
        return
    else:
        #index du film
        movie_id=df[df['title']==movie_input].index.values[0]
        #cosine similarity de la matrice précédente pour le film sélectionné
        cs = cosine_similarity(cm[movie_id], cm)
        #Create a list of enumerations for the similarity score
        scores = list(enumerate(cs[0]))
        #Sort the list to get the higher score first
        sorted_scores = sorted(scores, key= lambda x: x[1], reverse= True)
        film1 = df.loc[sorted_scores[1][0]]['title']
        film2 = df.loc[sorted_scores[2][0]]['title']
        film3 = df.loc[sorted_scores[3][0]]['title']
        return ('Here is 3 movies that we would recommend you:'), (' - {}'.format(film1)), (' - {}'.format(film2)), (' - {}'.format(film3))

if __name__ == '__main__':
    app.run_server(debug=True)