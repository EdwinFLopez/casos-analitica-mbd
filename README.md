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
$ cd mbd-datamining-p01
$ python -m venv venv
$ source venv/bin/activate
```

### Instalar dependencias

Una vez creado el ambiente virtual, se deben instalar las dependencias:

```shell
$ pip install -r requirements.txt
```

## Ejecutar sitio

El aplicativo es un app web usando [streamlit](https://streamlit.io).
Para ejecutarlo, se debe usar cualquiera de los siguientes comando:

```shell
# Running
python -m streamlit run main.py

# Equivalent a:
streamlit run main.py
```

Una vez ejecutado el comando de inicio, aparece el siguiente mensaje:
```shell
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.129:8501
```
