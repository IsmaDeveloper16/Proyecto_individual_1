
""" 
            Aqui comenzare con las funciones para importar y ejecutarlas en mi API
"""

import pandas as pd

#Primera funcion:

def PlayTimeGenre(genre,df_steam_games,df_items):
    juegos_genero_steam = df_steam_games[df_steam_games['genres'].str.lower().str.contains(genre)]
    juegos_genero_items = df_items[df_items['game_name'].isin(juegos_genero_steam['game_name'])]

    df_combinado = pd.merge(juegos_genero_items, juegos_genero_steam[['game_name', 'release_date']], on='game_name')

    playtime_por_año = df_combinado.groupby('release_date')['playtime_forever'].sum()
    año = playtime_por_año.idxmax()
    return('el año de lanzamiento con más horas jugadas para el genero:',(genre),'es:',int(año))


#Segunda funcion:

def UserForGenre(genre,df_steam_games,df_items):
    juegos_genero_steam = df_steam_games[df_steam_games['genres'].str.lower().str.contains(genre)]
    juegos_genero_items = df_items[df_items['game_name'].isin(juegos_genero_steam['game_name'])]

    df_combinado = pd.merge(juegos_genero_items, juegos_genero_steam[['game_name', 'release_date']], on='game_name')

    playtime_por_año_jugador = df_combinado.groupby(['user_id','release_date','playtime_forever'])['playtime_forever'].sum()

    pw = playtime_por_año_jugador.idxmax()

    return (f"El usuario con más horas jugadas para Género{genre} es {pw[0]} con {int(pw[2])} horas jugadas en el año {pw[1]}")

#Tercera funcion:

def UsersRecommend(año,df_steam_games,df_reviews):

    reviews_año = df_reviews[df_reviews['posted'] == año]

    re_año_recom = reviews_año[(reviews_año['recommend'] == 1) & (reviews_año['sentiment analysis'] >= 1)]

    juegos_recomendados = pd.merge(re_año_recom[['id_game','recommend']],df_steam_games[['id_game','game_name']],on='id_game')

    games_recom_sum = juegos_recomendados.groupby('game_name')['recommend'].sum()

    top_3 = games_recom_sum.nlargest(3).index

    return(f'este es el top 3 juegos mas recomendados de steam: Puesto1: {top_3[0]}, Puesto2: {top_3[1]}, Puesto3: {top_3[2]}')

#Cuarta funcion:

def UsersNotRecommend(año,df_steam_games,df_reviews):
    reviews_año = df_reviews[df_reviews['posted'] == año]

    re_año_recom = reviews_año[(reviews_año['recommend'] == 0) & (reviews_año['sentiment analysis'] == 0)]

    juegos_recomendados = pd.merge(re_año_recom[['id_game','recommend']],df_steam_games[['id_game','game_name']],on='id_game')

    juegos_recomendados['recommend'] = juegos_recomendados['recommend'].replace({0:1})

    games_recom_sum = juegos_recomendados.groupby('game_name')['recommend'].sum()

    top_3 = games_recom_sum.nlargest(3).index

    return(f'este es el top 3 juegos menos recomendados de steam: Puesto1: {top_3[0]}, Puesto2: {top_3[1]}, Puesto3: {top_3[2]}')

#Quinta funcion:

def sentiment_analysis(año,df_steam_games,df_reviews):
    año_games = df_steam_games[df_steam_games['release_date'] == año]

    año_games_re = pd.merge(año_games[['game_name','id_game']],df_reviews[['id_game','sentiment analysis']],on='id_game')
    if año_games_re['sentiment analysis'].value_counts().sum() == 0:
        return (f'El año {año} no tiene reseñas de ninguna clase')
    else:
        se = año_games_re['sentiment analysis'].value_counts()
        return (f'Las reviews del año {año} son: Positivas: {se[2]}, Neutras:{se[1]}, Negativas: {se[0]}')

#Sistema de recomendación:

#item-item:
def item_item(id_game,games):
    #aquí copiare el dataframe games para utilizarlo en el modelo ML
    games_co = games.copy()

    #dropeamos las columnas:
    games_co.drop(['game_name','id_game'],axis=1,inplace=True)

    # importamos la funcion cosine_similarity, cargamos el resultado en games_coceno y convertimos en dataframe.
    from sklearn.metrics.pairwise import cosine_similarity
    games_co = cosine_similarity(games_co)
    games_co = pd.DataFrame(games_co)
    #Conseguimos el indice del juego que usaremos para ubicarnos en el coceno
    index = games[games['id_game'] == id_game].index[0]
    #Con ese indice obtenemos los juegos recomendados
    recomend = games_co[index].sort_values(ascending=False).iloc[1:6].index
    # filtramos en el dataframe games los indices obtenidos para tener los valores de los ids y los nombres.
    recomend = games.loc[recomend, ['id_game','game_name']].values

    return(f'estos son los juegos recomendados con sus ids y nombres: 1 id:{int(recomend[0][0])} name: {recomend[0][1]}, 2 id:{int(recomend[1][0])} name: {recomend[1][1]}, 3 id:{int(recomend[2][0])} name: {recomend[2][1]}, 4 id:{int(recomend[3][0])} name: {recomend[3][1]}, 5 id:{int(recomend[4][0])} name: {recomend[4][1]}.')

#user-item
def user_item(user,items,games):
    # filtramos los usuarios para traer todos los juegos jugados por el.
    items = items[items['user_id'] == str(user)]
    #traeré el id del juego mas jugado por ese usuario.
    max = items['playtime_forever'].idxmax()
    id_game = items['id_game'].iloc[max]
    #Usaré el id del juego y lo metemos a la función que habia creado antes para encontrar los 5 juegos recomendados
    return item_item(id_game,games)