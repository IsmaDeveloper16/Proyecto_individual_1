""" Importamos las librerias que estaremos usando para la creacion de la api """
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
import pyarrow.parquet as pq

#Creamos la clase model para definir el tipo de variable seran ano(lo puse asi porque no toma palabras con ñ),item y user
class Model(BaseModel):
    ano: int
    item: int
    user: str

#   Tambien importamos las funciones desde nuestro archivo .py
from Funciones import PlayTimeGenre,UserForGenre,UsersNotRecommend,sentiment_analysis

#   Cargamos los datos para las funciones a las variables
df_steam_games = pd.read_csv('steam_games.csv')
df_items = pq.read_table('items_parquet.parquet').to_pandas()
df_reviews = pd.read_csv('reviews.csv')
games_model = pd.read_csv('games_model.csv')

#   Tambien importamos las funciones desde nuestro archivo .py
from Funciones import PlayTimeGenre,UserForGenre,UsersRecommend,UsersNotRecommend,sentiment_analysis,item_item,user_item


#   Creamos el objeto "app"
app = FastAPI()

#Creamos la ruta principal con un diccionario de direcciones para manejarse entre las rutas que haré:
@app.get("/")
def index():
    return {'Rutas: ':[{'/PlayTimeGenre/':'Inserte genero','/UserForGenre/':'Inserte genero',
                        '/UsersRecommend/':'Inserte año','/UsersNotRecommend/':'Inserte año',
                        '/sentiment_analysis/':'Inserte año'}]}

#Aquí comence las rutas de las Apis:

@app.get("/PlayTimeGenre/{genre}")
def PlayTime(genre):
    return PlayTimeGenre(genre,df_steam_games,df_items)

@app.get("/UserForGenre/{genre}")
def UserGenre(genre):
    return UserForGenre(genre,df_steam_games,df_items)

@app.get("/UsersRecommend/{ano}")
def Recommend(ano:int):
    return UsersRecommend(ano,df_steam_games,df_reviews)

@app.get("/UsersNotRecommend/{ano}")
def NotRecommend(ano:int):
    return UsersNotRecommend(ano,df_steam_games,df_reviews)

@app.get("/sentiment_analysis/{ano}")
def sentiment(ano:int):
    return sentiment_analysis(ano,df_steam_games,df_reviews)

@app.get("/item_recomend/{item}")
def item(item:int):
    return item_item(item,games_model)

@app.get("/user_recomend/{user}")
def user(user):
    return user_item(user,df_items,games_model)