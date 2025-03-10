# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

# <h2 align=center>**`Sistema de recomendación de películas`**</h2>

<p align="center">
<img src="imagenes\palabras.png" height=200>
</p>

## DATOS

Dataset movies y credits de https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5 y se realizaron las siguientes transformaciones:

## ETL


+ Se eliminan las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**. Además se eliminan otras columnas: **`belong_to_colection`** (por tener muchos faltantes), **`production_companies`** (por ser irrelevante), **`spoken_languajes`** (por ser redundante con la columna original_language) y **`tagline`** (por tener muchos faltantes e irrelevante)"


<p align="center">
<img src="imagenes/nulos.png" height=400>
</p>


+ Las fechas se pusieron en el formato **`AAAA-mm-dd`** y se creó **`release_year`** donde extrae el año de la fecha de estreno.

+ Se eliminan los valores nulos del campo **`release date`**.

+ Se crea la columna con el retorno de inversión **`return`** con los campos **`revenue`** y **`budget`**. Después de rellenar por el número **`0`** los valores nulos de los campos **`revenue`**, **`budget`** .

+ Los campos anidados se analizan y se extraen. Pensando en la necesidad posterior se extraen solo los géneros de **`genres`**, solo los iso_3166_1 de **`production_countries`**, solo los tres primeros actores de **`cast`** y solo el director de **`crew`**.

De esta forma se realiza el merge de las dos tablas y se obtiene el dataframe **movies_df.csv**.

## EDA

### Del dataframe conseguido:

Primero se analizan los datos faltantes que quedaron, los duplicados, los tipos de datos y otros detalles básicos.
Luego se analizan por separado las variables cuantitativas y cualitativas. Por ejemplo en las variables cuantitativas se analiza la utilidad de la columna **`popularity`**:

<p align="center">
<img src="imagenes\popularity.png" height=400>
</p>

Y en las variables cualitativas se ven las cantidades de repeticiones, por ejemplo de la columna **`genres`**:

<p align="center">
<img src="imagenes\genero.png" height=300>
</p>

## API
Se crearon las 6 funciones para los endpoints que se consumirán en la API:

<p align="center">
<img src="imagenes\consultas.png" height=400>
</p>

+ def **cantidad_filmaciones_mes( *`Mes`* )**

<p align="center">
<img src="imagenes\mes.png" height=500>
</p>

+ def **cantidad_filmaciones_dia( *`Dia`* )**

<p align="center">
<img src="imagenes\dia.png" height=500>
</p>

+ def **score_titulo( *`titulo_de_la_filmación`* )**

<p align="center">
<img src="imagenes\tituloscore.png" height=500>
</p>

+ def **votos_titulo( *`titulo_de_la_filmación`* )**

<p align="center">
<img src="imagenes\tituloano.png" height=500>
</p>

+ def **get_actor( *`nombre_actor`* )**

<p align="center">
<img src="imagenes\actor.png" height=500>
</p>

+ def **get_director( *`nombre_director`* )**

<p align="center">
<img src="imagenes\director.png" height=500>
</p>

## RECOMENDACIÓN

El algoritmo de recomendación se realiza con la *`cosine_similarity`*. Para esto se debe crear una nueva tabla donde se extraen las características más representativas y útiles de las columnas preprocesadas y se juntan en una sola columna llamada **`tags`** que contiene registros como:

<p align="center">
<img src="imagenes\tag.png" height=100>
</p>

Y la tabla final es:

<p align="center">
<img src="imagenes\recomendacion_df.png" height=250>
</p>

Y el endpoint en la API se ve como:

<p align="center">
<img src="imagenes\recomendacion.png" height=500>
</p>

## DEPLOYMENT

Se cargan los documentos locales a Github y se genera el deployment con [Render](https://render.com/docs/free#free-web-services) siguiendo el [tutorial de Render](https://github.com/HX-FNegrete/render-fastapi-tutorial).

<p align="center">
<img src="imagenes\deploy.png" height=500>
</p>

# <h1 align=center>**[API PI01_Henry en Render](https://pi01-henry-r85z.onrender.com/docs)**</h1>
