# Api-Flask-Recomendation

Este proyecto contiene la implementación de una API para el laboratorio 8. La API está diseñada para interactuar con los datos y proporcionar diversas funcionalidades.

## Estructura del Proyecto

- `app.py`: Archivo principal que inicia la aplicación.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar la aplicación.
- Otros archivos y directorios relevantes para la implementación de la API.

## Instalación sin Docker

1. Clona este repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Instala las dependencias utilizando el siguiente comando:

    ```sh
    pip install -r requirements.txt
    ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando:

```sh
python app.py
```

## Ejecucion con Docker

Puedes ejecutar el Dockerfile para crear la imagen y luego ejecutarla en un contenedor, pero si no quieres puedes optar por ejecutar una imagen que esta en DockerHub

### Opcion 1: Iniciar el programa con la imagen de DockerHub:
Ejecuta el siguiente comando para iniciar la aplicacion
```sh
docker run -d -p 5000:5000 miguelangel45/my-flask-app:latest
```
Ejemplo de ruta para ve resultados

```url
/recommendations?user_id=1&k=5
```
En este ejemplo, user_id=1 corresponde al usuario para el que se generarán las recomendaciones, y k=5 especifica el número de recomendaciones que deseas recibir.

### Opcion2: Contruir la imagen con el Dockerfile:

1. Clona este repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Contruye la imagen utilizando el siguiente comando:

    ```sh
    docker build -t my-flask-app .
    ```
  Uso
  
  Para iniciar la aplicación, ejecuta el siguiente comando:
  
  ```sh
  docker run -d -p 5000:5000 my-flask-app
```
