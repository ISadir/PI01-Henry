from fastapi import FastAPI, Depends
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies_df.csv")


app = FastAPI(
    title = "Consultas y recomendaciones de películas", 
    description = "API que permite realizar consultas sobre películas del dataset movies_df"
)


# ____________________________________________cantidad_filmaciones_mes___________________________________________________________________
@app.get('/por_mes/{mes}')
async def cantidad_filmaciones_mes( mes:str, df=Depends(lambda: df)):
	"""
    Se ingresa un mes en idioma Español. 
    Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado.\n 
    :param mes: Mes para el cual se quiere obtener la cantidad de películas\n 
    :param df: Dataframe movies_df de donde se obtienen los datos\n 
    :return: Mensaje con la cantidad de películas\n 
    """
	meses_año = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                 "septiembre", "octubre", "noviembre", "diciembre"]
	mesnorm = mes.lower()
	if mesnorm in meses_año:
		df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d') 
		meses = df['release_date'].dt.month
		numero = meses_año.index(mesnorm) + 1
		conteo = (meses == numero).sum()
		return (f'{conteo} es cantidad de películas fueron estrenadas en el mes de {mesnorm.capitalize()}.')
	else:
		return (f'"{mes}" no es un mes en el idioma Español, verifique la ortografía e intentelo nuevamente')


# ________________________________________________cantidad_filmaciones_dia____________________________________________________
@app.get('/por_dia/{dia}')
async def cantidad_filmaciones_mes( dia:str, df=Depends(lambda: df)):
	"""
    Se ingresa un día de la semana en idioma Español. 
    Debe devolver la cantidad de películas que fueron estrenadas en el día consultado.\n 
    :param dia: Día de la semana para el cual se quiere obtener la cantidad de películas\n 
    :param df: Dataframe movies_df de donde se obtienen los datos\n 
    :return: Mensaje con la cantidad de películas\n 
	"""
	dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'] 
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	dianorm = dia.lower()
	if dianorm in dias:
		df['dia_semana'] = df['release_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%A'))
		numero = dias.index(dianorm)
		conteos = df['dia_semana'].value_counts()
		conteo = conteos[days[numero]]
		return (f'{conteo} es cantidad de películas fueron estrenadas en los días {dianorm.capitalize()}.')
	else:
		return (f'"{dia}" no es un dia de la semana en el idioma Español, verifique la ortografía e intentelo nuevamente')

# _________________________________________________________score_titulo_____________________________________________________
@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo:str, df=Depends(lambda: df)):
	"""
    Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.\n 
    :param titulo: Título de la pelicula buscada\n 
    :param df: Dataframe movies_df de donde se obtienen los datos\n 
    :return: Mensaje con el título de la película, año de estreno y score\n 
    """
	df['title'] = df['title'].str.lower()
	titulonorm = titulo.lower()
	pelicula = df[df['title'].str.contains(titulonorm)]
	if not pelicula.empty:
		año = pelicula['release_year'].iloc[0]
		score=pelicula['vote_average'].iloc[0]
		return(f'La película "{titulonorm.capitalize()}" fue estrenada en el año {año} con un score de {score:.2f} puntos.')
	else:
		return(f'El la película titulada "{titulo}" no se pudo encontrar, controle la ortografía o pruebe nuevamente con otro título.')
	
# __________________________________________________________________________votos_titulo____________________________________________________
@app.get('/votos_titulo/{titulov}')
async def votos_titulo(titulo:str, df=Depends(lambda: df)):
	"""
    Se ingresa el título de una filmación esperando como respuesta el título, 
	la cantidad de votos y el valor promedio de las votaciones. Caso de que la película no cuente con 2000 valoraciones,
	devuelve un mensaje avisando que no cumple esta condición.\n 
    :param titulo: Título de la pelicula buscada\n 
    :param df: Dataframe movies_df de donde se obtienen los datos\n 
    :return: Mensaje con el título de la película, año de estreno, cantidad de valoraciones y su promedio\n 
    """

	df['title'] = df['title'].str.lower()
	titulonorm = titulo.lower()
	pelicula = df[df['title'].str.contains(titulonorm)]
	if not pelicula.empty:
		voto = pelicula['vote_average'].iloc[0]
		cantidad =pelicula['vote_count'].iloc[0]
		año = pelicula['release_year'].iloc[0]
		if cantidad > 2000:
			return(f'La película "{titulonorm.capitalize()}" fue estrenada en el año {año}. La misma cuenta con un total de {cantidad} valoraciones, con un promedio de {voto}.')
		else:
			return(f'El la película titulada "{titulo.capitalize()}" no tiene la cantidad necesaria de valoraciones (2000), prueve nuevamente con otro título.')
	else:
		return(f'El la película titulada "{titulo}" no se pudo encontrar, controle la ortografía o pruebe nuevamente con otro título.')

# ________________________________________________________get_actor____________________________________________________________________
@app.get('/actor/{actor}')
async def get_actor(nombre:str, df=Depends(lambda: df)):
	"""
	Se ingresa el nombre de un actor que se encuentre dentro de un dataset y devuelve el éxito del mismo medido 
	a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno.\n 
	:param nombre: Nombre del director\n 
	:param df: Dataframe movies_df de donde se obtienen los datos\n 
	:return: Mensaje describiendo que tan exitosa es la carrera del actor, cuantas películas hizo y cual es el promedio de retorno\n 
	"""
	df ['cast'] = df['cast'].str.lower()
	df['director'] = df['director'].str.lower()
	nombrenorm = nombre.lower()
	actor = df[df['cast'].str.contains(nombrenorm)]
	actor = actor[actor['director'] != nombrenorm]
	cantidad = actor.shape[0]
	cantidad
	if cantidad:
		retornos = actor['return']
		promedio = retornos.mean()
		retorno = retornos.sum()
		if cantidad > 1:
			return(f'El actor/actriz {nombre.title()} ha participado en {cantidad} filmaciones, el mismo ha conseguido un retorno de {retorno:.5} con un promendio de {promedio:.2} por filmación.')
		else:
			return(f'El actor/actriz {nombre.title()} ha participado en {cantidad} filmación, el mismo ha conseguido un retorno de {retorno:.5}.')
	else:
		return(f'El actor o actriz "{nombre}" no se pudo encontrar, controle la ortografía o pruebe nuevamente con otro nombre.')


# ___________________________________________________________get_director______________________________________________________________________________
@app.get('/director/{director}')
async def get_director(nombre:str, df=Depends(lambda: df)):
	"""
    Se ingresa el nombre de un director que se encuentre dentro de un dataset y devuelve el éxito del mismo medido 
	a través del retorno. Además, sus películas con la fecha de lanzamiento, retorno individual, costo y ganancia de cada una.\n 
    :param nombre: Nombre del director\n 
    :param df: Dataframe movies_df de donde se obtienen los datos\n 
    :return: Mensaje describiendo que tan exitosa es la carrera del actor, cuantas películas hizo y cual es el promedio de retorno\n 
    """
	df_filtrado = df.copy()
	df_filtrado = df_filtrado.dropna(subset=['director'])
	df_filtrado ['director'] = df_filtrado['director'].str.lower()
	exitos = {1:"no tan exitosa", 2:"levemente exitosa", 3:"bastante exitosa", 4:"extremadamente exitosa"}
	nombrenorm = nombre.lower()
	director = df_filtrado[df_filtrado['director'].str.contains(nombrenorm)]
	cantidad = director.shape[0]
	if cantidad:
		retornos = director['return']
		promedio = retornos.mean()
		exito = exitos[1 if promedio<1 else 2 if promedio< 1.5 else 3 if promedio < 3 else 4]
		lista_peliculas = ' \n '.join([f"{row['title']} del {row['release_date']} cuyo retorno fue {row['return']:.1f} (con un costo inicial de {row['budget']:.1f} y ganancia de {row['revenue']})." for index, row in director.iterrows()])
		if cantidad > 1:
			return(f'"{nombre.title()}" tiene una carrera en el cine {exito}, el promedio de retorno entre sus {cantidad} películas registradas es {promedio:.2} veces la inversión.\n Y sus peliculas son:\n {lista_peliculas}' )
		else:
	
			return(f'{nombre.title()} tiene una carrera en el cine {exito}, el retorno su única películas registrada {director["title"].iloc[0]} del {director["release_date"].iloc[0]} es {promedio:.2} veces la inversión (con un costo inicial de {director["budget"].iloc[0]:.1f} y ganancia de {director["revenue"].iloc[0]}).')

	else:
		return(f'El director o directora "{nombre}" no se pudo encontrar, controle la ortografía o pruebe nuevamente con otro nombre.')



#____________________________________________________ Sistema de recomendación ________________________________________________________
@app.get('/recomendacion/{title}')
async def recomendar(title: str):
	"""
    Se ingresa el título de una película que se encuentre dentro de un dataset y devuelve 5 otros títulos similares.\n 
    :param title: Título de pélicula\n 
    :param df: Dataframe recomendacion_df de donde se obtienen los datos\n 
    :return: Mensaje con 5 títulos de películas similares\n 
    """
	df2 = pd.read_csv("recomendacion_df.csv")

	cv = CountVectorizer(max_features=5000, stop_words="english")
	vectors = cv.fit_transform(df2["tags"]).toarray()
	simil = cosine_similarity(vectors)
	
	df2['title1'] = df2['title'].str.lower()
	title1 = title.lower()
	if title1 in df2['title1'].values:
		movie_index = df2[df2["title1"] == title1].index[0] 
		distances = simil[movie_index]
		movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
		pel = []
		for i in movie_list:
			list_pel = df.iloc[i[0]].title
			pel.append(list_pel)
		pel_string = ", ".join(pel)
		return pel_string
	else:
		return(f'La película "{title}" no se encuentra en la base de datos, pruebe nuevamente con otro título')



