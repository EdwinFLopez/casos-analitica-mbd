# casos-analitica-mbd
Repositorio que almacena los casos de analítica del master en bigdata.

## Preparación

1. Antes de iniciar, se debe contar con git, y descargar el código del repositorio github.
2. Se debe iniciar un ambiente virtual de python para instalar las dependencias.
3. Se proporciona un script para descargar el dataset y los archivos de soporte.

## Instalar ambiente virtual

Para ejecutar los scripts, se deben proporcionar las dependencias adecuadas.
Con este propósito debemos crear un ambiente virtual.

### Usando python venv

Se debe entrar en el folder donde se descargó el repo.

```shell
$ git clone git@github.com:EdwinFLopez/casos-analitica-mbd.git
$ cd casos-analitica-mbd
$ python -m venv venv
$ source venv/bin/activate
```

### Instalar dependencias

Una vez creado el ambiente virtual, se deben instalar las dependencias:

```shell
$ pip install -r requirements.txt
```

## Listado de Proyectos

Proyectos realizados en el marco del desarrollo del curso "Analítica de Datos"
del Máster en Big Data 2023-2024

### Caso 01: Notebook "./caso01/caso_analitica_taxis_nyc.ipynb"

Proyecto que realiza un análisis de datos tomados de la página web
de la ciudad de New York. La temática es relacionada con los taxis de la ciudad
y sus viajes geo referenciados. Se realiza un modelo de predicción.

### Caso 02: Notebook "./caso02/caso_analitica_nlp_twitter.ipynb"

El proyecto es acerca del análisis de sentimientos y procesamiento de lenguaje natural (NLP), 
utilizando un dataset proveniente de Twitter.

### Caso 03: Notebooks "./caso03/good_reads_books.ipynb" y ".caso03/good_reads_model.ipynb"

El proyecto analiza los best reads del sitio "GoodReads", utilizando técnicas de webscraping.
Se realiza un modelo de recomendaciones utilizando una matriz de similitud con base en el 
análisis de similitud del coseno.
