El proyecto fue diseñado usando Python 3.8 usando el framework de Flask.

En el archivo requirements.txt están todos los complementos que deben ser instalados para su ejecución, por lo tanto es necesario antes de todo ejecutar el comando "pip install -r requirements.txt".

Adicional a esto se encuentra un archivo sql llamado "api_voters.sql" el cual solo es necesario ser importado en un motor de base de datos MySQL, el script contiene la creación de la base de datos, tablas y relaciones.

Una vez instaladaas las dependencias del archivo de requirements y cargada la base de datos, dentro de la carpeta corremos el archivo app.py con el siguiente comando
"python app.py", el cual ejecutará en la dirección localhost del puerto 3000 "http://localhost:3000". 

Luego de esto se puede abrir el archivo "Api Voters.postman_colleccion.json" en el programa de Postman donde están la colleccion de los programas
