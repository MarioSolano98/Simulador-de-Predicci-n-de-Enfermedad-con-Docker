Markdown

# Simulador de Predicción de Enfermedad con Docker
## Pipeline de MLOps + Imagen de Docker

Este proyecto es una aplicación web  construida con Flask que simula un modelo básico de predicción de estado de enfermedad basado en datos demográficos y un conjunto limitado de síntomas. La aplicación está diseñada para ser empaquetada y ejecutada utilizando Docker.

**NOTA IMPORTANTE:** La lógica de predicción utilizada en este simulador es **arbitraria y con fines demostrativos únicamente**.

## Objetivo de la Solución

El objetivo principal de este proyecto es demostrar cómo construir una pequeña aplicación web con Flask que exponga una funcionalidad (en este caso, una simulación de predicción) a través de una interfaz web, y cómo contenedorizar esta aplicación utilizando Docker para facilitar su despliegue y ejecución en diferentes entornos.

## Estructura del Proyecto

Para ejecutar este proyecto, necesitas la siguiente estructura de archivos y directorios en la raíz de tu proyecto:
.
```text
├── app.py             # Código fuente de la aplicación Flask
├── Dockerfile         # Instrucciones para construir la imagen Docker
├── requirements.txt   # Dependencias de Python
└── templates
    └── index.html     # Interfaz web básica
```

Estos archivos los podrás encontrar en el repositorio.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:

* [Docker](https://www.docker.com/get-started)

## Docker

Una vez que tengas todos los archivos configurados, puedes construir la imagen Docker y ejecutar el contenedor.

### Construir la Imagen Docker

Abre una terminal en el directorio raíz de tu proyecto (donde se encuentran `app.py`, `Dockerfile`, etc.). Ejecuta el siguiente comando para construir la imagen Docker:

```bash
docker image build -t flask_docker .
```
.: Indica que el Dockerfile y el contexto de construcción se encuentran en el directorio actual.
Este comando leerá el Dockerfile y creará la imagen flask_docker. Este proceso puede tardar unos minutos la primera vez.

### Ejecutar el Contenedor Docker
Una vez que la imagen ha sido construida con éxito, puedes ejecutar un contenedor a partir de ella. Ejecuta el siguiente comando:

```bash
docker run -p 5000:5000 -d 
```

* docker run: El comando para ejecutar un contenedor.
* -d: Ejecuta el contenedor en modo "detached" (en segundo plano), liberando tu terminal.
* -p 5000:5000: Mapea el puerto 5000 del host (tu máquina) al puerto 5000 del contenedor.
* flask_docker: El nombre de la imagen a usar para crear el contenedor.

El contenedor ahora estará corriendo en segundo plano, y la aplicación Flask será accesible a través del puerto mapeado en tu máquina.

### Uso de la Solución

Si has incluido el archivo index.html en la ubicación correcta (templates/index.html) antes de construir la imagen, puedes acceder a la interfaz web abriendo tu navegador en:

http://localhost:5000/

La página index.html mostrará un formulario simple para ingresar los datos demográficos y seleccionar los síntomas. Al hacer clic en el botón el resultado de la predicción será mostrado en la misma página.

![](https://github.com/MarioSolano98/Simulador-de-Predicci-n-de-Enfermedad-con-Docker/blob/567faf1daa72479c9db4a761bc096cb160dfa6b1/Web%20de%20la%20soluci%C3%B3n.png?raw=true)

En caso de datos insuficientes o un error interno, la respuesta contendrá un mensaje de error en la clave prediction.
